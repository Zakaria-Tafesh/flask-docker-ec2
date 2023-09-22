FROM mysql:5.7

# Copy the script into the container
COPY query.sh /usr/local/bin/query.sh
#COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Make the script executable
RUN chmod +x /usr/local/bin/query.sh
#RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint to run the script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
