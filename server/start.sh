###
#   Prompt the project name
###

if [ -z "$project_name" ]; then
    echo "Please enter site name (ex: lucky_all): "
    read project_name
fi

export project_name

./setup_wsgi.sh
./setup_nginx.sh
./setup_launch.sh


