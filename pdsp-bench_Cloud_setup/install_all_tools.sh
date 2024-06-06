# Copy custom_producer.py
cp /local/repository/custom_producer.py /home/playground/

# Downloading flink 
curl -0 https://archive.apache.org/dist/flink/flink-1.16.2/flink-1.16.2-bin-scala_2.12.tgz --output /home/playground/zip/flink.tgz
# Unzip flink to playgrounds directory
tar zxf /home/playground/zip/flink.tgz -C /home/playground/

# Copy oshi,jna and jna_platform
cp /local/repository/jna-platform-5.10.0.jar /home/playground/flink-1.16.2/lib
cp /local/repository/jna-5.10.0.jar /home/playground/flink-1.16.2/lib
cp /local/repository/oshi-core-6.1.5.jar /home/playground/flink-1.16.2/lib

# Copy dsp_jobs files
cp /local/repository/dsp_jobs-1.0-SNAPSHOT.jar /home/playground/flink-1.16.2/bin

# Copy roads.geojson file to flink/bin

cp /local/repository/roads.geojson /home/playground/flink-1.16.2/bin 

# Downloading prometheus 
curl -L https://github.com/prometheus/prometheus/releases/download/v2.42.0/prometheus-2.42.0.linux-amd64.tar.gz > /home/playground/zip/prometheus.tar.gz
# Unzip prometheus to playgrounds directory
tar zxf /home/playground/zip/prometheus.tar.gz -C /home/playground/

# Download grafana
curl -L https://dl.grafana.com/enterprise/release/grafana-enterprise-9.3.6.linux-amd64.tar.gz > /home/playground/zip/grafana.tar.gz
# Unzip grafana to playgrounds directory
tar zxf /home/playground/zip/grafana.tar.gz -C /home/playground/


# Download kafka
curl -L https://downloads.apache.org/kafka/3.4.1/kafka_2.12-3.4.1.tgz > /home/playground/zip/kafka.tgz

# Unzip kafka to playgrounds directory
tar zxf /home/playground/zip/kafka.tgz -C /home/playground/

# removing default kafka property
rm /home/playground/kafka_2.12-3.4.1/config/server.properties

# Copying the server.properties to /home/playground
cp /local/repository/server.properties /home/playground/kafka_2.12-3.4.1/config

#rm -r /local/repository

sudo rm -r /home/playground/zip

