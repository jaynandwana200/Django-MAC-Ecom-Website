echo "Build Start"
python -m pip install django
python -m pip install -r requirements.txt
python manage.py manage.py makemigrations --noinput --clear
python manage.py manage.py migrate --noinput --clear
python manage.py collectstatic --noinput --clear
ech0 "Build End"