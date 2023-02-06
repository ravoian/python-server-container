# !/usr/local/bin/python3
# See bottom of file for command examples

# 3rd Party Modules
import os
import sys
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler

#Directory to serve static content from
serveDirectory = '/mnt/'

# Use simple std logging for basic DataDog collection 
class log:
    scriptName = os.path.basename(sys.argv[0])
    def info(msg):
        print(f'{log.scriptName}: {msg}', file=sys.stdout)
    def error(msg):
        print(f'{log.scriptName}: {msg}', file=sys.stderr)

# Create new handler class for configuration
class Handler(SimpleHTTPRequestHandler):
    # Apply serveDirectory value
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=serveDirectory, **kwargs)
    # Use stdout for log message
    def log_message(self, format, *args):
        message = format % args
        log.info("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          message.translate(self._control_char_table)))
    # Use stderr for log error
    def log_error(self, format, *args):
        message = format % args
        log.error("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          message.translate(self._control_char_table)))

def _ParseArguments() -> (bool, argparse.Namespace):
    # Generate our parser
    parser = argparse.ArgumentParser()
    # Service configuration
    parser.add_argument('--port', dest="serverPort", required=True, action='store', help='What file share to use')
    parser.add_argument('--bind', dest="serverBind", required=True, action='store', help='What file share to use')
    parser.add_argument('--dir', dest="serverDirectory", required=True, action='store', help='What mount point to use')
    # Parse what we got
    parsedArguments = parser.parse_args()
    return (True, parsedArguments)

def _EntryPointAsScript():
    # Parse the arguments
    operationSuccess, parsedArguments = _ParseArguments()
    if not operationSuccess:
        log.error('Failed to parse command line arguments')
        return -1
    serverPort = parsedArguments.serverPort
    serverBind = parsedArguments.serverBind

    global serverDirectory
    serverDirectory = parsedArguments.serverDirectory

    # Run the server and handle the output
    log.info('Starting HTTP server')
    try:
        #Run the server
        serverAddress = (serverBind, int(serverPort))
        httpd = HTTPServer(serverAddress, Handler)
        log.info(f'Serving {serveDirectory}')
        httpd.serve_forever()
    except Exception as e:
        if str(e) == "[Errno 98] Address in use":
            log.info(f'Already running')
        else:
            log.error(f'{e}')

# Since we are running as a script; go ahead and run the entry point
if __name__ == '__main__':
    if sys.version_info.major < 3:
        log.error(f'Script requires Python3') 
    exitCode = _EntryPointAsScript()
    
# Example usage
# python3 HTTPServer.py --port 443 --bind 0.0.0.0 --dir /mnt/ 