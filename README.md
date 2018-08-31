# todoapp
Todo App based on Python Django.
API's written using TastyPie.
Minimalistic Frontend using AngularJs.
Celery task for deleting old objects in db using redis.

PostgreSql as Database

Follow through these steps to setup.

    Create a virtual environment.

    Clone the repo using git clone https://github.com/Sreeharis25/todoapp/.

    Install the requirements using 'pip install -r requirements.txt'.

    Make sure postgres is installed. If not

For ubuntu users.
    
    Run "sudo apt-get install postgresql" for installing latest PostgreSql version.
    
    After installation for setting up root credentials.
    
    Login to Postgres shell using the command "sudo -u postgres psql". 
    
    Then set root user credentials using command "ALTER USER postgres PASSWORD 'newpassword';". 
    
    You can exit the shell using the command "quit".
    
If postgres is there then
   
    Create db user using the db credentials in settings module.
    
    Then migrate the database changes use "python manage.py migrate".

    Celery tasks are using redis as broker so make sure redis is installed.

Fire up the server and you are all set!
