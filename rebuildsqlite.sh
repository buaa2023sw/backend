rm -f db.sqlite3
rm -rf myApp/migrations/*
touch myApp/migrations/__init__.py
python manage.py makemigrations
python manage.py migrate
python manage.py rebuilddb
