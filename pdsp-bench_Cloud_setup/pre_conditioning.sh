# Install python 3.10, java 11 openjdk
sudo mkdir /home/playground 
sudo /usr/local/etc/emulab/mkextrafs.pl -f /home/playground
sudo mkdir /home/playground/kafka-logs
sudo mkdir /home/playground/zip
sudo mkdir ~/.kaggle
cp /local/repository/kaggle.json ~/.kaggle
chmod 600 ~/.kaggle/kaggle.json
# EXPORT variables for custom producer
sudo update-locale LC_ALL=C.UTF-8
sudo update-locale LANG=C.UTF-8
# Install python3.10 and pip3
sudo apt update && sudo apt upgrade --yes
sudo apt autoremove --yes
sudo dpkg --configure -a --force-depends --yes
sudo apt-get -f install --yes
sudo apt install software-properties-common --yes
sudo add-apt-repository ppa:deadsnakes/ppa --yes
sudo apt install  python3.10 --yes
sudo apt-get install python3-pip --yes 
sudo apt install unzip --yes
# Install java
sudo apt-get install openjdk-11-jdk --yes 
# Install setuptools
sudo pip3 install -U setuptools
# Upgrade pip3
sudo pip3 install --upgrade pip
# Install kafka-producer dependencies 
# Install click
yes | pip3 install click
# Install openpyxl
yes | pip3 install openpyxl
# Install confluent kafka
yes | pip install confluent-kafka 
# Install pandas
yes | pip3 install pandas
# Install Kaggle
yes | pip3 install kaggle
