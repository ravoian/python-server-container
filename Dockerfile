# syntax=docker/dockerfile:1.2
# Use small container image base
FROM python:3.9-alpine3.16

# Set environment variables
ENV fileShare=/fileshare/
ENV mountPoint=/mnt/
ENV serverIP=0.0.0.0

# Store port from argument
ARG defaultPort=443
ENV serverPort=${defaultPort}

# Copy Python scripts
COPY FSMount.py /
COPY HTTPServer.py /

# Setup for mounting
RUN apk add cifs-utils
RUN mkdir -p ${mountPoint}

# Setup for cron jobs
RUN echo ' *  *  *  *  * echo cron: Running minute jobs' >> /etc/crontabs/root
RUN echo ' *  *  *  *  * python3 -u /FSMount.py --fshare ${fileShare} --mpoint ${mountPoint}' >> /etc/crontabs/root
RUN echo ' *  *  *  *  * sleep 4; python3 -u /HTTPServer.py --port ${serverPort} --bind ${serverIP} --dir ${mountPoint}' >> /etc/crontabs/root

# Run single process
CMD ["/usr/sbin/crond", "-f"]
