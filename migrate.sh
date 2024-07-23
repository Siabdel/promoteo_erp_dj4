## delete db
rm db.sqlite3
## delete migrations files
find . -name migrations -exec rm -r {} ;
### makemigrate 
./manage.py makemigrations taxonomy widgets core filebrowser menus 
## product customer invoice  project 
## migrate 
#./manage.py migrate
##
#./manage.py createsuperuser
