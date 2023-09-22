FROM mysql:5.7

# Copy the script into the container
COPY query.sh /usr/local/bin/query.sh

# Make the script executable
RUN chmod +x /usr/local/bin/query.sh

# Copy the entry script into the container
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Make the entry script executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Use the entry script as the CMD
CMD ["/usr/local/bin/entrypoint.sh"]
