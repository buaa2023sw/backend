rm -f db.sqlite3
rm -f myApp/migrations/*_initial.py
python manage.py makemigrations
python manage.py migrate
python manage.py rebuilddb
