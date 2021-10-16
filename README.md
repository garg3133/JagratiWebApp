<p align="center">
    <a href="https://jagrati.herokuapp.com">
        <img src="static/logo.png" width="20%">
    </a>
</p>

<h1 align="center"> 
    Jagrati - An initiative of IIITians
</h1>

Jagrati is an initiative by the students of **IIITDM Jabalpur** to provide free and quality education to the poor and underprivileged children of villages surrounding our institute. 

Currently, we have adopted 5 villages in the vicinity of our institute, namely, Gadheri, Amanala, Chanditola, Mehgawan, and Suarkol where we *provide education* to around 100 children of classes 1 through 10. Apart from providing basic education to the students in regular classes, **we also prepare the students of 4th and 5th grade for the prestigious Navodaya Vidyalaya** and other similar government-funded institutions which provide quality education to students, completely free of cost.

Apart from teaching the children, we do many other activities like **organizing Blood Donation Camps, Tree Plantation Drives, Cloth Donation, Stationery Distribution, Campaigns to spread awareness in villages, etc.**

**Our Achievements:**
- 1 student was selected for Jawahar Navodaya Vidyalaya in 2018.
- 1 student was selected for Jawahar Navodaya Vidyalaya in 2019.
- 2 students were selected for Jawahar Navodaya Vidyalaya in 2020.
- 4 students cleared the entrance examination for Eklavya Model Residential School (EMRS) in 2020.
- 4 students cleared the entrance examination for Gyanodaya Vidyalaya in 2020.

(Like Navodaya Vidyalaya, both EMRS and Gyanodaya Vidyalaya provide free quality education to students from class 6 to 12).

Currently, we are operating in online mode to prepare students of class 5 for Navodaya Examination, 2021.

## About JagratiWebApp
JagratiWebApp is the **official web application** for managing day-to-day operations at Jagrati, like keeping track of the content being taught in a class and homework being given to the students, taking and keeping a record of student and volunteer attendance, keeping a record of all the students being taught under the initiative and the volunteers contributing towards the initiative among many things.

The main aim of the application is to simplify the work of volunteers by making all the information readily accessible to them like what was taught in the last class or in the last week and how many students attended those classes so that they can easily decide what should be taught on the present day and update the same in the application. Plus, it also helps in taking the attendance of students with more ease over the conventional method of manually taking note of the names of all the students present.

So, all in all, it is meant to help the volunteers work more effectively and efficiently and make it easy to keep track of daily activities.

## Technology Stack

### Frontend:
<img alt="HTML5" src="https://img.shields.io/badge/html5%20-%23E34F26.svg?&style=for-the-badge&logo=html5&logoColor=white"/> <img alt="CSS3" src="https://img.shields.io/badge/css3%20-%231572B6.svg?&style=for-the-badge&logo=css3&logoColor=white"/> <img alt="Bootstrap" src="https://img.shields.io/badge/bootstrap%20-%23563D7C.svg?&style=for-the-badge&logo=bootstrap&logoColor=white"/> <img alt="JavaScript" src="https://img.shields.io/badge/javascript%20-%23323330.svg?&style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"/>

### Backend:
<img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/> <img alt="Django" src="https://img.shields.io/badge/django%20-%23092E20.svg?&style=for-the-badge&logo=django&logoColor=white"/>

### Database:
<img alt="SQLite" src ="https://img.shields.io/badge/sqlite-%2307405e.svg?&style=for-the-badge&logo=sqlite&logoColor=white"/> <img alt="MySQL" src="https://img.shields.io/badge/mysql-%2300f.svg?&style=for-the-badge&logo=mysql&logoColor=white"/> <img alt="Postgres" src ="https://img.shields.io/badge/postgres-%23316192.svg?&style=for-the-badge&logo=postgresql&logoColor=white"/>

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

### Setting up the project

  * Download and install Python 3.7
  * Download and install Git.
  * Fork the Repository.
  * Clone the repository to your local machine `$ git clone https://github.com/<your-github-username>/JagratiWebApp.git`
  * Change directory to JagratiWebApp `$ cd JagratiWebApp`
  * Add a reference to the original repository  
   `$ git remote add upstream https://github.com/garg3133/JagratiWebApp.git`
  * Install virtualenv `$ pip3 install virtualenv`
  * Create a virtual environment `$ virtualenv env -p python3.7`  
  * Activate the env: `$ source env/bin/activate` (for linux) `> ./env/Scripts/activate` (for Windows PowerShell)
  * Install the requirements: `$ pip install -r requirements.txt`
  * Create a new file in the root directory of the repository (`JagratiWebApp`) with the name `.env` (only `.env` and not `.env.txt`) and add the following content to it:
    ```
    EMAIL_HOST_USER = 'your-email@domain.com'
    EMAIL_HOST_PASSWORD = 'your-password'

    SENDER_EMAIL = 'Jagrati <your-email@domain.com>'
    ADMINS_EMAIL = ['email-address-of-admin@domain.com']

    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'google-oauth2-key'
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'google-oauth2-secret'
    ```  
    or, just copy the `.env.save` file from the `samples` directory to the root directory (`JagratiWebApp`) and rename it to `.env` (only `.env` and not `.env.txt`)  
  
    where, 
    * `EMAIL_HOST_USER` and `SENDER_EMAIL` is the email address of your Gmail account from which you want to send emails (By default, Django will output email content into the console. To actually send emails to real users, comment line 30 and uncomment line 31 in `Jagrati/settings/development.py`).
    * `EMAIL_HOST_PASSWORD` is the password for that Gmail account.
    * `ADMINS_EMAIL` is a list of email addresses of Admins of the site (who will receive important updates from the site like when a new user joins in).
    * `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY` and `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET` are the API keys for login/signup using Google.

    **Note:** All the changes mentioned above in the `.env` template are *optional* and you do not need to change anything if you want all the email contents to be printed in the console itself and you do not wish to use the login/signup through Google. The changes in the first 4 lines in the `.env` file are required only if you wish to send out real emails to real people and changes in the last 2 lines are required only if you wish to use login/signup through Google.
  * Copy `sample-db.sqlite3` from `samples` directory to the root directory (`JagratiWebApp`) and rename it to `db.sqlite3`.
  * Make migrations `$ python manage.py makemigrations`
  * Migrate the changes to the database `$ python manage.py migrate`
  * Create admin `$ python manage.py createsuperuser`
  * Run the server `$ python manage.py runserver`
  
#### 💡️ **Pro Tip:** 
  * Always keep your master branch in sync with the main repository (by running `$ git pull upstream master` on your local master branch). 
  * Always create a new branch before making any changes (`$ git checkout -b <new-branch-name>`), never ever make any changes directly on the master branch.

 ### Setting up the project in docker

  * Fork the Repository.
  * Clone the repository to your local machine `$ git clone https://github.com/<your-github-username>/JagratiWebApp.git`
  * Change directory to JagratiWebApp `$ cd JagratiWebApp`
  * Copy the `.env.save` file from `samples` directory to the root directory (`JagratiWebApp`) and rename it to `.env` (only `.env` and not `.env.txt`).  
    
    (Read the [above](https://github.com/garg3133/JagratiWebApp#setting-up-the-project) section for details on all the variables used in `.env` file)
   
  * Copy `sample-db.sqlite3` from `samples` directory to the root directory (`JagratiWebApp`) and rename it to `db.sqlite3`.
  * Build the docker file to an image `sudo docker build -t <IMAGE_NAME> .`
  * Run the docker image `sudo docker run -p 8000:8000 <IMAGE_NAME>`
  * The server will start at the default port (8000), head over to your web browser to test.


### Contributing Guidelines 
  * Feel free to open an issue to report a bug or request a new feature.
  * Before starting to work on an issue, comment on that issue that you want to work on this and then only start to code.
  * Create a new branch with a related name of the motive i.e. bug/refactor/feature and commit your changes in that branch only.  
  * Send a pull request anytime :)  
  * Join our Discord Community: https://discord.gg/Ek9q45ZjAv
  * For more extensive guidelines, kindly check the [CONTRIBUTING.md](https://github.com/garg3133/JagratiWebApp/blob/master/CONTRIBUTING.md)🤝

## Open source programs we have been a part of 🚀:
Open source is a term that originally referred to Open Source Software (OSS). Open source software is code that is designed to be publicly accessible -- anyone can see, modify, and distribute the code as they see fit. There are a lot of open source programs held throughout the year to encourage people to contribute to open source and build awesome projects for the community. JagratiWebApp is one such open source project and has participated in quite a few events like the following.

<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://kwoc.kossiitkgp.org/">
        <img alt="" src="https://i.imgur.com/BRvF8x8.png" width="100" height="100"><br><sub><b>Kharagpur Winter of Code</b></sub><br>2020</a>
      </td>
      <td align="center"><a href="https://swoc.tech/">
        <img alt="" src="https://i.imgur.com/gRnFEGM.png" width="100" height="100"><br><sub><b> Script Winter of Code</b></sub><br>2020</a>
      </td>
      <td align="center"><a href="https://mexili.github.io/winter_of_code/#/">
        <img alt="" src="https://i.imgur.com/BHSz238.png" width="100" height="100"><br><sub><b> Mexili Winter of Code</b></sub><br>2021</a>
      </td>
        <td align="center"><a href="https://gssoc.girlscript.tech/">
      <img alt="" src="https://i.imgur.com/rtDGMEA.png" width="100" height="100"><br><sub><b> Girlscript Summer of Code</b></sub><br>2021</a>
      </td>
    </tr>
  </tbody>
</table>

## Project Maintainer 😃
<table>
  <tbody><tr>
    <td align="center">
    <a href="https://github.com/garg3133">
    <img alt="" src="https://avatars.githubusercontent.com/u/39924567?s=400&v=4" width="130px;"><br><sub><b> Priyansh Garg </b></sub></a>
    <br>
    <a href="https://github.com/garg3133/JagratiWebApp/commits?author=garg3133" title="Code">💻 </a>
    </td>
  </tr>
</tbody></table>

## Our valuable Contributors👩‍💻👨‍💻:
<a href="https://github.com/garg3133/JagratiWebApp/graphs/contributors">
  <img src="https://contributors-img.web.app/image?repo=garg3133/JagratiWebApp" />
</a>
