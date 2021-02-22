# Dockerfile wriiten for continous development 
# Running on django development server
# Making it easy for contributers across all environment to setup a Django platform in seconds
# 
# 
# 
# v1.0.0 

FROM python:3.6 
# This is the image base 


RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Keeping a work directory
WORKDIR /usr/src/app

# Copying and installing requirememts.txt
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Moving the files into our working directory
COPY . .

# Default port 8000 is opened from docker to server the project
EXPOSE 8000

# Django setups with DB and admin user
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py createsuperuser

# Entrypoint, While running this command will be executed
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]