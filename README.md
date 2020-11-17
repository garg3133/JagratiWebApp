# Jagrati
Jagrati is an initiative by the students of **IIITDM Jabalpur** to teach poor and under-privileged children of villages surrounding our institute, completely free of cost. 

Currently, we teach around 100 children from 5 villages in the vicinity of our institute, namely, Gadheri, Amanala, Chanditola, Mehgawan and Suarkol. Apart from providing basic education to the students of class 1 through 10 in regular classes , **we also prepare the students of 4th and 5th grade for the prestigious Navodaya Vidyalaya** and other similar institutions which provides quality education to students, completely free of cost.

Apart from teaching the children, we also do many other things like **organizing Blood Donation Camps, Tree Plantation Drives, Cloth Donation, Stationery Distribution, Campaigns to spread awareness in villages, etc.**

**Our Achievements:**
- 1 student cracked Navodaya Examination in 2018.
- 1 student cracked Navodaya Examination in 2019.
- 2 students cracked Navodaya Examination in 2020.
- 4 students cracked entrance examination for Eklavya Model Residential School (EMRS) in 2020.
- 4 students cracked entrance examination for Gyanodaya Vidyalaya in 2020.

(Like Navodaya Vidyalaya, both EMRS and Gyanodaya Vidyalaya provide free quality education to students from class 6 to 12).

Currently, we are operating in online mode to prepare students of class 5 for Navodaya Examination, 2021.

## About JagratiWebApp
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
  * Create a new file in root folder of repository (`JagratiWebApp`) with name `.env` and add the following content in it:
    ```
    EMAIL_HOST_USER = 'your-email@domain.com'
    EMAIL_HOST_PASSWORD = 'your-password'

    SENDER_EMAIL = 'Jagrati <your-email@domain.com>'
    ADMINS_EMAIL = ['email-address-of-admin@domain.com']
    ```
    where, 
    * `EMAIL_HOST_USER` and `SENDER_EMAIL` is the email address of your Gmail account from which you want to send emails (By default, Django will output email contents in console. To actually send emails to real users, comment line 27 and uncomment line 28 in `Jagrati/settings/development.py`).
    * `EMAIL_HOST_PASSWORD` is the password for that Gmail account.
    * `ADMINS_EMAIL` is a list of email addresses of Admins of the site (who will recieve important updates from the site like when a new user joins in).

    **Note:** All the changes mentioned above in the `.env` template are *optional* and you do not need to change anything if you want all the email contents to be printed in the console itself. The above changes are required only if you wish to send out real emails to real people.
  * Make migrations `$ python manage.py makemigrations`
  * Migrate the changes to the database `$ python manage.py migrate`
  * Create admin `$ python manage.py createsuperuser`
  * Run the server `$ python manage.py runserver`
 

## Contributing  
  * Create a new branch with a related name of the motive i.e. bug/refactor/feature  
  * Create an issue before actually starting to code  
  * Send a pull request anytime :)  
