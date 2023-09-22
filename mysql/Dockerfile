FROM mysql:5.7

# Copy the script into the container
COPY query.sh /usr/local/bin/query.sh

# Make the script executable
RUN chmod +x /usr/local/bin/query.sh

# Run the script when the container starts
CMD sleep 30 && /usr/local/bin/query.sh
