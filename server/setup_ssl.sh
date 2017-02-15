#!/bin/bash

#Required
if [ -z "$project_name" ]; then
    echo "Please enter site name (ex: lucky_all): "
    read domain
fi

sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /var/www/$project_name/config/$project_name.nginx.key -out /var/www/$project_name/config/$project_name.nginx.crt

