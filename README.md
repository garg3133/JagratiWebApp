# Jagrati
Official WebApp of Jagrati - An Initiative of IIITians

## Requirements

Python 3.7  
Django 2.2.6  
And additional requirements are in **requirements.txt**  


## How to run it?

  * Download and install Python 3.7
  * Download and install Git.
  * Fork the Repository.
  * Clone the repository to your local machine `$ git clone https://github.com/<your-github-username>/JagratiWebApp.git`
  * Change directory to JagratiWebApp `$ cd JagratiWebApp`
  * Install virtualenv `$ pip3 install virtualenv`
  * Create a virtual environment `$ virtualenv env -p python3.7`  
  * Activate the env: `$ source env/bin/activate` (for linux) `> ./env/Scripts/activate` (for Windows PowerShell)
  * Install the requirements: `$ pip install -r requirements.txt`
  * Create a new file in `JagratiWebApp/Jagrati` folder with name `.env` and add the following content in it:
    ```
    PRODUCTION = False

    EMAIL_HOST_USER = 'your-email@domain.com'
    EMAIL_HOST_PASSWORD = 'your-password'

    SENDER_EMAIL = 'Jagrati <your-email@domain.com>'
    ADMINS_EMAIL = ['email-address-of-admin@domain.com']
    ```
    where, 
    * `EMAIL_HOST_USER` and `SENDER_EMAIL` is the email address of your Gmail account from which you want to send emails (By default, Django will output email contents in console. To actually send emails, comment line 27 and uncomment line 28 in `Jagrati/dev_settings.py`).
    * `EMAIL_HOST_PASSWORD` is the password for that Gmail account.
    * `ADMINS_EMAIL` is a list of email addresses of Admins of the site (who will recieve important updates from the site like when a new user joins in).
    **Note:** All the changes mentioned above in the `.env` template are *optional* and you do not need to change anything if you want all the email contents to be printed in the console itself. The above changes are required only if you wish to send out real emails to real people.
  * Make migrations `$ python manage.py makemigrations`
  * Make migrations for other apps `$ python manage.py makemigrations volunteers students feedbacks misc`
  * Migrate the changes to the database `$ python manage.py migrate`
  * Create admin `$ python manage.py createsuperuser`
  * Run the server `$ python manage.py runserver`
 

## Contributing  
  * Create a new branch with a related name of the motive i.e. bug/refactor/feature  
  * Create an issue before actually starting to code  
  * Send a pull request anytime :)  
