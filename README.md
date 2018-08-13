# todoapp
Todo App based on Python Django.
API's written using TastyPie.
Minimalistic Frontend using AngularJs.
Celery task for deleting old objects in db using redis.

PostgreSql as Database

Create a virtual environment.
And then clone the repo using git clone https://github.com/Sreeharis25/todoapp/.
Then install the requirements using 'pip install -r requirements.txt'
Make sure postgres is installed.
Then migrate the database changes use python manage.py migrate
Celery tasks are using redis as broker so make sure redis is installed.
