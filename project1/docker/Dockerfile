# Use the official Ubuntu as the base image
FROM ubuntu:20.04

# Install the AWS CLI
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install awscli

# Set up the AWS CLI configuration (Optional)
RUN aws configure set default.region us-east-1

# Copy your script to the container
COPY worker.sh /app/worker.sh

# Set the working directory
WORKDIR /app

# Run your script when the container starts
CMD ["/bin/bash", "worker.sh"]
