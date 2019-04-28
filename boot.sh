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

python3 create_user.py
python3 enter_domains.py
exec gunicorn -b :16084 --access-logfile - --error-logfile - app:app