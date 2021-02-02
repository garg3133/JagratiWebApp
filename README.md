<p align="center">
    <a href="https://jagrati.herokuapp.com">
        <img src="static/logo.png" width="20%">
    </a>
</p>

<h1 align="center"> 
    Jagrati - An initiative of IIITians
</h1>

Jagrati is an initiative by the students of **IIITDM Jabalpur** to provide free and quality education to the poor and under-privileged children of villages surrounding our institute. 

Currently, we have adopted 5 villages in the vicinity of our institute, namely, Gadheri, Amanala, Chanditola, Mehgawan and Suarkol where we *donate education* to around 100 children of classes 1 through 10. Apart from providing basic education to the students in regular classes, **we also prepare the students of 4th and 5th grade for the prestigious Navodaya Vidyalaya** and other similar government-funded institutions which provides quality education to students, completely free of cost.

Apart from teaching the children, we do many other activities like **organizing Blood Donation Camps, Tree Plantation Drives, Cloth Donation, Stationery Distribution, Campaigns to spread awareness in villages, etc.**

**Our Achievements:**
- 1 student selected in Jawahar Navodaya Vidyalaya in 2018.
- 1 student selected in Jawahar Navodaya Vidyalaya in 2019.
- 2 students selected in Jawahar Navodaya Vidyalaya in 2020.
- 4 students cleared entrance examination for Eklavya Model Residential School (EMRS) in 2020.
- 4 students cleared entrance examination for Gyanodaya Vidyalaya in 2020.

(Like Navodaya Vidyalaya, both EMRS and Gyanodaya Vidyalaya provide free quality education to students from class 6 to 12).

Currently, we are operating in online mode to prepare students of class 5 for Navodaya Examination, 2021.

## About JagratiWebApp
JagratiWebApp is the **official web application** for managing day-to-day operations at Jagrati, like keeping track of the content being taught in a class and homework being given to the students, taking and keeping record of student and volunteer attendance, keeping record of all the students being taught under the initiative and the volunteers contributing towards the initiative among many things.

The main aim of the application is to simplify the work of volunteers by making all the information readily accessible to them like what was taught in the last class or in the last week and how many student attended those classes so that they can easily decide what should be taught on the present day and update the same in the application. Plus, it also helps in taking the attendance of students with more ease over the conventional method of manually taking note of the names of all the students present.

So, all in all, it is meant to help the volunteers work more effectively and efficiently and make it easy to keep track of daily activities.

## Technology Stack

**Frontend:** HTML, CSS(+ Bootstrap 4), JavaScript  
**Backend:** Python/Django  
**Database:** SQL (SQLite3/MySQL/PostgreSQL)  

And additional requirements are in [**requirements.txt**](https://github.com/garg3133/JagratiWebApp/blob/master/requirements.txt)

## To-Do

### New pages

- [ ] List of all Students
- [ ] List of all Volunteers
- [x] Student Profile
- [x] Volunteer profile
- [ ] Update Student Profile
- [ ] Update Volunteer Profile
- [x] Add new Student
- [ ] Calendar containing class schedule, events and other national/international important dates.
- [ ] Page for Managing Permissions
- [ ] Page for viewing and managing feedbacks
- [ ] Web Team Page

### New Apps

- [ ] Jagrati Inventory
- [ ] Events
- [ ] Meetings
- [ ] Study Material

### New Features

- [ ] Notifications
- [ ] Leaderboard (no. of hours contributed to Jagrati)


## Contributing

### Setting-up the project

  * Download and install Python 3.7
  * Download and install Git.
  * Fork the Repository.
  * Clone the repository to your local machine `$ git clone https://github.com/<your-github-username>/JagratiWebApp.git`
  * Change directory to JagratiWebApp `$ cd JagratiWebApp`
  * Install virtualenv `$ pip3 install virtualenv`
  * Create a virtual environment `$ virtualenv env -p python3.7`  
  * Activate the env: `$ source env/bin/activate` (for linux) `> ./env/Scripts/activate` (for Windows PowerShell)
  * Install the requirements: `$ pip install -r requirements.txt`
  * Create a new file in root folder of repository (`JagratiWebApp`) with name `.env` (only `.env` and not `.env.txt`) and add the following content in it:
    ```
    EMAIL_HOST_USER = 'your-email@domain.com'
    EMAIL_HOST_PASSWORD = 'your-password'

    SENDER_EMAIL = 'Jagrati <your-email@domain.com>'
    ADMINS_EMAIL = ['email-address-of-admin@domain.com']

    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'google-oauth2-key'
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'google-oauth2-secret'
    ```
    where, 
    * `EMAIL_HOST_USER` and `SENDER_EMAIL` is the email address of your Gmail account from which you want to send emails (By default, Django will output email contents in console. To actually send emails to real users, comment line 27 and uncomment line 28 in `Jagrati/settings/development.py`).
    * `EMAIL_HOST_PASSWORD` is the password for that Gmail account.
    * `ADMINS_EMAIL` is a list of email addresses of Admins of the site (who will recieve important updates from the site like when a new user joins in).
    * `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY` and `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET` are the API keys for login/signup using Google.

    **Note:** All the changes mentioned above in the `.env` template are *optional* and you do not need to change anything if you want all the email contents to be printed in the console itself and you do not wish to use login/signup through Google. The changes in the first 4 lines on `.env` file are required only if you wish to send out real emails to real people and changes in last 2 lines are required only if you wish to use login/signup through Google.
  * Create a copy of `sample-db.sqlite3` in root directory (`JagratiWebApp`) and rename it as `db.sqlite3`.
  * Make migrations `$ python manage.py makemigrations`
  * Migrate the changes to the database `$ python manage.py migrate`
  * Create admin `$ python manage.py createsuperuser`
  * Run the server `$ python manage.py runserver`
 

### Contributing Guidelines 
  * Feel free to open an issue to report a bug or request a new feature.
  * Before starting to work on an issue, comment on that issue that you want to work on this and then only start to code.
  * Create a new branch with a related name of the motive i.e. bug/refactor/feature and commit your changes in that branch only.  
  * Send a pull request anytime :)  
  * Join our Discord Community: https://discord.gg/Ek9q45ZjAv

## 💥 How to Contribute ?
- If you wish to contribute kindly check the [CONTRIBUTING.md](https://github.com/garg3133/JagratiWebApp/blob/master/CONTRIBUTING.md)🤝
