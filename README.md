# Aspire
**This is a Django application which uses Postgresql as its database**


**Postgresql setup for mac**
```
brew install postgresql@14 
brew services start postgresql
psql -U postgres
create database aspire;
create user aspire_user with encrypted password 'aspire@123';
grant all privileges on database aspire to aspire_user;
alter user aspire_user createdb;
```

**Django Application Setup**

1. create a new project folder and cd into it
    `mkdir aspire_project && cd aspire_project`
2. create a new python3 virtual environment
    `python3 -m venv aspireenv`
3. cctivate virtual environment
   `source aspireenv/bin/activate`
4. clone project `git clone`
5. cd into django project `cd aspire`
6. install requirements  `pip install -r requirements.txt`
7. run migrations `python manage.py migrate`
8. run server `python manage.py runserver`
9. to run test cases `python manage.py test aspireloan`

After completing the above steps Django server should be up and running
