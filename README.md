# primero descarga el proyecto 
git clone "url del proyecto"

# instala las librerias necesarios
pipenv install -r requirements.txt

# luego hacer migraciones 
py manage.py migrate

# si da error hacer makemigrations

# iniciar proyecto
python manage.py runserver


