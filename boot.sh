#!/bin/sh

source venv/bin/activate

flask db init
flask db migrate

while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done

python3 create_admin.py
python3 enter_domains.py
exec gunicorn -b :5000 --access-logfile - --error-logfile - victoria:app