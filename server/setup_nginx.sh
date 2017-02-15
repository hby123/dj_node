echo "---------------------------"
echo "-----Setup Nginx-----"
echo "---------------------------"

if [ -z "$project_name" ]; then
    echo "Please enter site name (ex: lucky_all): "
    read project_name
fi

sudo chmod -R 777 /var/www/$project_name
sudo chmod -R 777 /var/www/$project_name/config/


sudo cat > /var/www/$project_name/config/$project_name.nginx.conf <<EOL

upstream django {
    server unix:////var/www/$project_name/config/$project_name.sock; # for a file socket
    #server 127.0.0.1:8000; # for a web port socket (we will use this first)
}

server {
    listen 8002 default_server;
    listen [::]:8002 default_server;
    server_name localhost;

    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /media  {
        alias  /var/www/$project_name/media;  # your Django project  media files - amend as required
    }

    location /static {
        alias  /var/www/$project_name/static; # your Django project  static files - amend as required
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /var/www/$project_name/config/$project_name.uwsgi_params; # the uwsgi_params file you installed
    }
}

server {
    listen 443;
    server_name localhost;

    ssl on;
    ssl_certificate  /var/www/$project_name/config/$project_name.nginx.crt;
    ssl_certificate_key  /var/www/$project_name/config/$project_name.nginx.key;

    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /media  {
        alias  /var/www/$project_name/media;  # your Django project  media files - amend as required
    }

    location /static {
        alias  /var/www/$project_name/static; # your Django project  static files - amend as required
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /var/www/$project_name/config/$project_name.uwsgi_params; # the uwsgi_params file you installed
    }
}


EOL