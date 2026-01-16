# Cyber Security Base 2025 - Final Project

This is a web application project for the University of Helsinki's *Cyber Security Base* course (Project I). 

The application is a **Music Album Blog** where users can sign up, log in, and write reviews for music albums. 


The detailed analysis of the vulnerabilities, including descriptions, locations in code, and mitigation strategies, can be found in the separate report file:

 **[Read the Vulnerability Report (REPORT.md)](REPORT.md)** 

##  Installation and Running

Follow these steps to get the application running on your local machine.


### Prerequisites
* Python 3 installed
* Git (optional, or download as ZIP)

### 1. Clone the repository
```bash
git clone [https://github.com/k1rtsu/CyberSecurityCourse-final-project.git](https://github.com/k1rtsu/CyberSecurityCourse-final-project.git)
cd CyberSecurityCourse-final-project
```


2. Set up the Virtual Environment
Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install Dependencies
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Initialize Database
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create an Admin User
To log in and manage the site, create a superuser account:

```bash
python manage.py createsuperuser
```
(Follow the prompts to set a username and password)


6. Run the Server
```bash
python manage.py runserver
```

