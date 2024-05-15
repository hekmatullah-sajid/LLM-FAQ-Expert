FROM docker.elastic.co/elasticsearch/elasticsearch:8.4.3

# Set environment variables
ENV discovery.type=single-node \
    xpack.security.enabled=false

# Expose ports
EXPOSE 9200 9300