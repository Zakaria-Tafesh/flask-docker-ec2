FROM mysql:5.7

# Copy the script into the container
COPY query.sh /usr/local/bin/query.sh

# Make the script executable
RUN chmod +x /usr/local/bin/query.sh

# Set the entrypoint to run the script
ENTRYPOINT ["/usr/local/bin/query.sh"]
