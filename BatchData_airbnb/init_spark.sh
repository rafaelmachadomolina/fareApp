# Script to install Spark and its dependencies in the working directory.

echo "Start script at " "$(date)" > setup.log

echo "Initialising script..."

echo "Removing previous Spark packages if found..."

echo "Attempting to remove existing Spark packages: " "$(date)" >> setup.log

rm -dr spark* 2>> setup.log

echo "Installing Java and Spark..."

echo "Installing Java and Spark: " "$(date)" >> setup.log

sudo apt-get install openjdk-8-jdk-headless -qq > /dev/null
wget -q https://downloads.apache.org/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz
tar xf spark-3.2.1-bin-hadoop3.2.tgz

echo "Installing pyspark packages..."

echo "pip install pyspark: " "$(date)" >> setup.log

pip install -q findspark
pip install pyspark

echo "Downloading PostgreSQL driver..."
wget -q wget https://jdbc.postgresql.org/download/postgresql-42.3.2.jar

echo "Downloaded PostgreSQL driver: " "$(date)" >> setup.log

echo "Creating env variables..."

echo "Creating enviroment variables: " "$(date)" >> setup.log

export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export SPARK_HOME=./spark-3.2.1-bin-hadoop3.2

echo "Versions: " "$(date)" >> setup.log

java -version >> setup.log
python --version >> setup.log

echo "End of script: " "$(date)" >>setup.log

echo "End of script!"
