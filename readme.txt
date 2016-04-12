Instruction to install TickTock:

1: go to AWS to apply for a simple linux machine, which is free.
2: run python debug_online_v3.py will start the server which corr
3: make sure you installed apache php, move the webpage/a.php, d.php,TickTock.php to your installed directory, usually it is /var/www/html, TickTock.html is the corresponding client.
4: make sure to install all the needed python libraries, such as nltk:)

Simply execute the script below:

#!/bin/bash
sudo apt-get install git
mkdir ticktock
cd ticktock
git clone https://github.com/echoyuzhou/ticktock_text_api.git
cd ticktock_text_api
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
sudo pip install -U nltk
sudo apt-get install gcc
sudo apt-get install python-dev
sudo easy_install numpy
sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran
sudo pip install -U scipy
sudo easy_install gensim
sudo pip install zmq
sudo python -m nltk.downloader treebank
sudo python -m nltk.downloader wordnet
sudo python -m nltk.downloader stopwords
sudo python -m nltk.downloader maxent_ne_chunker
sudo python -m nltk.downloader maxent_treebank_pos_tagger
sudo python -m nltk.downloader averaged_perceptron_tagger
sudo python -m nltk.downloader words
sudo python -m nltk.downloader punkt
sudo python prepare_data.py
cd word2vec
sudo python word2vec.py
cd ..
sudo apt-get install apache2
sudo apt-get install php5-common libapache2-mod-php5 php5-cli
/etc/init.d/apache2 start
sudo apt-get install php5-mysql php5-curl
sudo cp webpages/* /var/www/html/
sudo python debug_online_v4_turk.py

Data Collected: The conversations collectd using TickTock 1.0 is in rating_log/v1, and uisng TickTock 2.0 is in rating_log/v2

A live demo : http://www.cs.cmu.edu/~zhouyu/TickTock.html
