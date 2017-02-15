if [ -z "$project_name" ]; then
    echo "Please enter site name (ex: lucky_all): "
    read project_name
fi

echo "---------------------------"
echo "-----Start Server-----"
echo "---------------------------"


##
# emperor
##


if [ ! -d "/etc/uwsgi" ]
  then 
    sudo mkdir /etc/uwsgi  
fi

if [ ! -d "/etc/uwsgi/vassals" ]
  then 
    sudo mkdir /etc/uwsgi/vassals
fi

sudo ln -sf /var/www/$project_name/config/$project_name.uwsgi.ini /etc/uwsgi/vassals/
sudo uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data &

##
# nginx
##

sudo ln -sf /var/www/$project_name/config/$project_name.nginx.conf /etc/nginx/sites-enabled/
sudo service nginx start
sudo service nginx restart

#####
# Nginx communicate with uwsgi over socket file.
# File uwsgi.ini, is pointing to the .wsgi inside the Django file.
#####
