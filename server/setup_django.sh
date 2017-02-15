echo "---------------------------"
echo "--------Setup Django--------"
echo "---------------------------"

if [ -z "$project_name" ]; then
    echo "Please enter site name (ex: lucky_all): "
    read project_name
else
       print "skip...."
fi

cd /

if [ ! -d "/var/www" ]
    then
        sudo mkdir /var/www
fi

if [ ! -d "/var/www" ]
    then
        sudo mkdir /var/www
fi

cd /var/www

if [ ! -d "/var/www/$project_name" ]
    then
        sudo django-admin.py startproject $project_name
fi



