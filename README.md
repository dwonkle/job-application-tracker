# job-application-tracker
A full-stack web app for tracking job applications. Built with Flask, MySQL, and Bootstrap.

## Setup

### 1. Install Dependencies

```
pip install -r requirements.txt
```

### 2. Set Up The Database

After confirming that MySQL is installed and running,

```
mysql -u root -p < schema.sql
```

### 3. Configure Database Password

Open 'database.py' and replace the password with your MySQL root password.

### 4. Run

```
python app.py
```
And open `http://127.0.0.1:5000` in browser.
