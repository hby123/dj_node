echo "---------------------------"
echo "-----Crontab Setup -----"
echo "---------------------------"

if [ -z "$project_name" ]; then
    echo "Please enter site name (ex: lucky_all): "
    read project_name
else
       print "skip...."
fi

if [ ! -d "/backup" ]
    then
        sudo mkdir /backup
fi

if [ ! -d "/backup/db" ]
    then
        sudo mkdir /backup/db
fi

(crontab -l 2>/dev/null; echo "00 02 * * * * python /var/www/$project_name/config/fastmojo/cconfig/server/db_backup.py") | crontab -



