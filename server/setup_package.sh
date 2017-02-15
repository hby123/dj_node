#!/bin/bash

echo "---------------------------"
echo "-----Setup Package-----"
echo "---------------------------"

echo "Need to install packages? (ex: Y/N): "
read install_package

echo "Need to install MySQL? Existing data will be lost. (ex: Y/N): "
read install_mysql

echo "Need to install django? (ex: Y/N): "
read install_django

###
# install packages
###

if [ "$install_package" == "Y" ]
  then
    sudo apt-get -y update
    sudo apt-get -y install emacs
    sudo apt-get -y install lynx
    sudo apt-get -y install python-setuptools
    sudo apt-get -y install git
    sudo apt-get -y install build-essential
    sudo apt-get -y install python-dev
    sudo apt-get -y install libjpeg-dev
    sudo apt-get -y install libfreetype6-dev
    sudo apt-get -y install zlib1g-dev
    sudo apt-get -y install python2.7-dev
    sudo apt-get -y install python-pip
    sudo apt-get -y install nginx

    sudo easy_install pip
    sudo pip install uwsgi
    sudo pip install pillow
fi

###
# install mysql
###

if [ "$install_mysql" == "Y" ] 
  then
    sudo apt-get  --assume-yes install mysql-server
    sudo apt-get  --assume-yes install mysql-client
    sudo apt-get  --assume-yes install libmysqlclient-dev

    sudo pip install MySQL-python
fi


###
# install django
###

if [ "$install_django" == "Y" ]
 then
    cd /
    sudo mkdir /django_install
    cd django_install
    export DJ_URL=https://www.djangoproject.com/m/releases/1.8/Django-1.8.4.tar.gz
    sudo wget $DJ_URL
    sudo tar -xvf Django-1.8.4.tar.gz
    cd D*.4
    sudo python setup.py install
fi