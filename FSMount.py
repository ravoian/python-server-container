# !/usr/local/bin/python3
# See bottom of file for command examples

# 3rd Party Modules
import os
import sys
import argparse

# Use simple std logging 
class log:
    def info(msg):
        print(f'mount.py: {msg}', file=sys.stdout)
    def error(msg):
        print(f'mount.py: {msg}', file=sys.stderr)

def _ParseArguments() -> (bool, argparse.Namespace):
    # Generate our parser
    parser = argparse.ArgumentParser()
    # Service configuration
    parser.add_argument('--fshare', dest="fileShare", required=True, action='store', help='What file share to use')
    parser.add_argument('--mpoint', dest="mountPoint", required=True, action='store', help='What mount point to use')
    # Parse what we got
    parsedArguments = parser.parse_args()
    return (True, parsedArguments)

def _EntryPointAsScript() -> int:
    # Parse the arguments
    operationSuccess, parsedArguments = _ParseArguments()
    if not operationSuccess:
        log.error('Failed to parse command line arguments')
        return -1
    fileShare = parsedArguments.fileShare
    mountPoint = parsedArguments.mountPoint

    # Run the mount and return the exit code
    log.info('Starting mounting')
    mountExit = os.popen(f'mount -t cifs {fileShare} {mountPoint} -osec=ntlmv2,username=username,password=password 2> /dev/null; echo $?').read()
    mountStatus = int(mountExit)

    # Log human readable based on exit status
    if mountStatus == 0:
        log.info(f'Mounted {fileShare} to {mountPoint}')
    elif mountStatus == 1:
        log.error('Insufficient privileges for mounting')
    elif mountStatus == 32:
        log.info('Already mounted')
    elif mountStatus == 255:
        log.error('File share not found')
    else:
        log.error(f'Encountered unknown status code: {mountStatus}')
    return mountStatus 

# Since we are running as a script; go ahead and run the entry point
if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise Exception("Script requires Python3")   
    exitCode = _EntryPointAsScript()
    
# Example usage
# python3 FSMount.py --fshare /fileshare/ --mpoint /mnt/