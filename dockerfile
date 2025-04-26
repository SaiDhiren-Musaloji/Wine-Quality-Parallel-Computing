FROM bitnami/spark:3.4.0

# Switch to root for package installation
USER root

# Install Python pip and necessary Python dependencies
RUN install_packages python3-pip && \
    pip3 install --no-cache-dir boto3 pandas

# Add required Hadoop dependencies for S3
RUN install_packages wget && \
    wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.6/hadoop-aws-3.3.6.jar -P /opt/bitnami/spark/jars/ && \
    wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.569/aws-java-sdk-bundle-1.12.569.jar -P /opt/bitnami/spark/jars/

# Set the working directory
WORKDIR /app

# Copy your Spark application to the container
COPY wine_quality_prediction.py /app/wine_quality_prediction.py

# Remove the default ENTRYPOINT
# ENTRYPOINT ["spark-submit", "/app/predict.py"]   <-- Comment this out

# Use CMD instead, so the script can be passed dynamically via the docker run command
CMD ["spark-submit", "/app/wine_quality_prediction.py"]
