echo "---------------------------"
echo "-----Start Server-----"
echo "---------------------------"

sudo touch /var/www/$project_name/config/$project_name.sock
sudo chmod -R 777 /var/www/$project_name
sudo chmod -R 777 /var/www/$project_name/config/

##
# emperor
##
if [ -z "$project_name" ]; then
    echo "Please enter site name (ex: lucky_all): "
    read project_name
fi

if [ ! -d "/etc/uwsgi" ]
  then 
    sudo mkdir /etc/uwsgi  
fi

if [ ! -d "/etc/uwsgi/vassals" ]
  then 
    sudo mkdir /etc/uwsgi/vassals
fi

killall uwsgi
sudo ln -s /var/www/$project_name/config/$project_name.uwsgi.ini /etc/uwsgi/vassals/
sudo uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data &

##
# nginx
##

sudo ln -s /var/www/$project_name/config/$project_name.nginx.conf /etc/nginx/sites-enabled/
sudo service nginx start
sudo service nginx restart

#####
# Nginx communicate with uwsgi over socket file.
# File uwsgi.ini, is pointing to the .wsgi inside the Django file.
#####
