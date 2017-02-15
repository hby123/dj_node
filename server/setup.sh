# You might want to configure a superuser as follow
#  >>  sudo passwd user
#  >> sudo visudo, and append to file: USERNAME  ALL=(ALL:ALL) ALL
#  >> sudo nano /etc/ssh/sshd_config, change PasswordAuthentication no to PasswordAuthentication yes
#  >> sudo /etc/init.d/ssh restart
#  >> sudo reboot

# You might need to update the file permissions
# cd dj_node/server/
# find /var/www/dj_node/server -type f -exec dos2unix {} \;
# chmod 755 *



###
#   Prompt the project name
###

if [ -z "$project_name" ]; then
    echo "Please enter site name (ex: lucky_all): "
    read project_name
fi

export project_name


###
# need chmod the following files for executation
###

./setup_package.sh
./setup_django.sh
./setup_ssl.sh
./setup_wsgi.sh
./setup_nginx.sh
./setup_cron.sh
./setup_start.sh


