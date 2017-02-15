echo "---------------------------"
echo "-----Setup WSGI-----"
echo "---------------------------"

###
# uwsgi.ini
###

sudo chmod -R 777 /var/www/$project_name
sudo chmod -R 777 /var/www/$project_name/config/

if [ -z "$project_name" ]; then
    echo "Please enter site name (ex: lucky_all): "
    read project_name
fi

sudo cat > /var/www/$project_name/config/$project_name.uwsgi.ini  <<EOL

# uwsgi.ini file
[uwsgi]

# Django-related settings
# the base directory (full path)
chdir           = /var/www/$project_name
# Djangos wsgi file
module          = $project_name.wsgi

# the virtualenv (full path)
#---> home            = /path/to/virtualenv

# process-related settings
# master
master          = true

# maximum number of worker processes
processes       = 10

# the socket (use the full path to be safe
socket          = /var/www/$project_name/config/$project_name.sock
#http           = 0.0.0.0:8001 #use this for debug only

# ... with appropriate permissions - may be needed

chmod-socket    = 666

# clear environment on exit
vacuum          = true
EOL


###
# uwsgi_params
###

sudo cat >  /var/www/$project_name/config/$project_name.uwsgi_params <<EOL
uwsgi_param  QUERY_STRING       \$query_string;
uwsgi_param  REQUEST_METHOD     \$request_method;
uwsgi_param  CONTENT_TYPE       \$content_type;
uwsgi_param  CONTENT_LENGTH     \$content_length;

uwsgi_param  REQUEST_URI        \$request_uri;
uwsgi_param  PATH_INFO          \$document_uri;
uwsgi_param  DOCUMENT_ROOT      \$document_root;
uwsgi_param  SERVER_PROTOCOL    \$server_protocol;
uwsgi_param  REQUEST_SCHEME     \$scheme;

uwsgi_param  HTTPS              \$https if_not_empty;

uwsgi_param  REMOTE_ADDR        \$remote_addr;
uwsgi_param  REMOTE_PORT        \$remote_port;
uwsgi_param  SERVER_PORT        \$server_port;
uwsgi_param  SERVER_NAME        \$server_name;
EOL