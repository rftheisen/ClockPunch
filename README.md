# ClockPunch
An application that lets you clock in and track time.

There are a surprising number of organizations out there still tracking employee time using paper and pencil. This application is for those organizations to have an easier way to do it, for free. 

## How to setup and run ClockPunch in a Development Environment

Ensure that the Python3 virtual environment is installed. 

```
sudo apt install python3-venv
```
Create a new directory for the project. 
```
mkdir clockpunch
cd clockpunch
```
Create the python virtual environment
```
python3 -m venv venv
```
Activate the python virtual environment. 
```
source venv/bin/activate
```
Install the required packages: flask and sqlalchemy
```
pip install flask flask-sqlalchemy
```

## Theres still work to do....

There is still some work to do with ClockPunch. If you would like to contribute for learning purposes or just out of the kindness of your heart, here are a few things I need help with building: 

- Stronger authentication
- Support for Active Directory, Entra ID and other identify services on-prem and cloud-based
- Export button to allow data to be exported in multiple formats
- Gamified UI
- Documentation to help less technical users setup ClockPunch in their environments
- Any new ideas! Feel free to study and experiment with ClockPunch, you may get new ideas I never thought of.
  

If you contribute to ClockPunch in anyway, I will gladly be a reference for you in your job search. 
