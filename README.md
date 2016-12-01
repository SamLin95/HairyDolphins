# HairyDolphins
## Introduction
HairyDolphins is a web app that connects travellers with local people, who are willing to spend a day (or even a few hours) working as a tourist guide, to help tourists get the best experience of their travel. Until today, tourist guide is a professional occupation and most of the guides are affiliated with travel agencies, so it is very difficult for independent travellers to find a local companion who can travel alongside with. Our idea is that everyone can work as a tourist guide, as long as he/she is a local resident, preferably bilingual, and is enthusiastic about taking visitors to interesting places. Our app is going to change the way of finding a tourist guide to the way that you book a taxi or request a Uber cab -- easy, fast, and reliable.

##Release Notes
###New Features
1. Completed Chat function to allow users to send and receive real time messages
2. Added a page to allow users to provide their recommendations
3. Added a page to allow users to edit user profiles
4. Seperated location from the keyword part to become an indiviual filter for local advisor searching
5. Allowed a local advisor to add himself/herself to the meetup list of a recommendation
###Bug Fixes
1. Clicking on Login no longer redirects the user back to the homepage
2. Fixed the time display of messages on Chat page
###Known Bugs
1. Once an user enters a chatroom with another user, the unread message count cannot be displayed normally for the user who is chatted with
2. When a chat action is initiated through the "Send Message" button on a local advisor's home page, the contact list will not immediately show the message receiver. 

## Installation Guide
### Quick Links
[Overview](#overview)

[Prerequisites](#prerequisites)

[Dependencies](#dependencies)

[Download](#download)

[Build](#build)

[Installation](#installation)

[Running Application](#running)

[Deploy HairyDolphins To A Real Server (Optional)](#deploy)

[Troubleshooting](#troubleshooting)

<a name="overview"/>
### Overview

HairyDolphins is a webapp which needs to be eventually hosted on a server. The way to deploy and configure the website depends on the operating system and the server option. However, there are some prerequisites and dependencies that are common for all server options. This installation guide will direct the user to install and host the HairyDolphins on a local machine and deploy the website to a Apache2 server operated on a Ubuntu machine.

<a name="prerequisites"/>
### Prerequisites

#### A Server Running Linux, MacOS or Windows
The website needs to be hosted on a server machine which is running Linux, MacOS or Windows.

#### Connect To the Internet
The installation of website requires the Internet connection to necessary tools and packages. Verify a connection was established, for example with ping:
```
ping www.google.com
```

#### Install Python 2.7 (The version matters)
The website is implemented in python 2.7 so the machine to host is required to have python 2.7 installed. There are a lot of ways to install python 2.7. The proper ways to install python 2.7 on different platforms can be found on:
http://docs.python-guide.org/en/latest/starting/installation/


To verify if python 2.7 has been installed, use command:

```
python --version
```

The version of current python on your machine should be returned if installed successfully.


#### Install python-pip
The website uses a lot of python packages. The installation of those packages needs python-pip, which is a package management system used to install and manage software packages written in Python. The offical way to install python-pip is provided on https://pip.pypa.io/en/stable/installing/. To verify if python-pip has been installed, use command:

```
pip --version
```

The version of python-pip on your machine should be returned if installed successfully


#### Install PostgreSQL 9.5 (The version matters)
Although HairyDolphins store data on a database on Amazon RDS rather than on the server. A critical python package still needs PostgreSQL to be installed on the machine where the website is hosted. The installation is easy on most of Linux systems and MacOS


If you are working on the Ubuntu system, you should be able to easily install PostgreSQL 9.5 by the following command:

```
sudo apt-get install postgresql-9.5
```

MacOS Users can easily install PostgreSQL 9.5 through brew (To know how to install brew, users can go to http://brew.sh/):

```
sudo brew install postgresql-9.5
```

PostgreSQL as a community supported database supports almost all popular operating systems and has provided very detailed directions about how to install PostgrSQL on different platforms, which can be found on: https://wiki.postgresql.org/wiki/Detailed_installation_guides.


#### Setup Amazon S3
HariyDolphins store files on Amazon Simple Storage Service(S3). A Amazon S3 bucket needs to be created to allow website to run normally. Users should follow instrucions provided on https://aws.amazon.com/s3/getting-started/ to sign up for Amazon S3 and create a bucket named ‘hairydolphins’ to which the webite will upload files.

<a name="dependencies"/>
### Dependencies
To run the website on any kind of server, all python packages below need to be installed through python-pip, the dependencies are provided in form of ‘package-name==packageversion’, which can be directly used by python pip. The way to install a dependency is using command:

```
pip install package-name==packageversion
```

All requirements are listed in HairyDolphins/src/main/python/requirement.txt, and you can install them all at once through command: 

```
pip install -r requirement.txt
```

List of all dependencies required: 

* Flask==0.11.1
* psycopg2==2.6.2
* Flask-Login==0.3.2
* Flask-RESTful==0.3.5
* Flask-SQLAlchemy==2.1
* flask-restful-swagger==0.19
* SQLAlchemy-Searchable==0.10.2
* marshmallow==2.10.0
* marshmallow-sqlalchemy==0.10.0
* Flask-Triangle==0.5.4
* Flask-SocketIO==2.7.1
* eventlet==0.19.0
* boto==2.42.0
* Werkzeug==0.11.11

<a name="download"/>
### Download
https://github.com/SamLin95/HairyDolphins/archive/master.zip

<a name="build"/>
### Build
No build necessary for this app.

<a name="installation"/>
### Installation
#### Step 1. Clone Source Code From Github
Firstly, users need to download the source code from Github to proceed. Users can either download the source code using git clone:

```
git clone https://github.com/SamLin95/HairyDolphins.git
```

(If you have not installed git yet, you can follow steps on this link to install git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)


Or manually download the source code from github through link https://github.com/SamLin95/HairyDolphins/archive/master.zip and uncompress the zip file.


#### Step 2. Install Dependencies Using python-pip
As mentioned in [Dependencies](#dependencies) section above, users then need to install all python dependencies with python-pip.


After successfully installed all dependencies, users will be able to view all already installed packages using command:

```
pip freeze
```

#### Step 3. Set S3 Credentials
Python package boto will lookup your S3 credentials automatically so all users have to do is to export credentials as environment variables on the host machine or store S3 credentials in a specific file.


Boto will check environment variables below for credentials:

* AWS_ACCESS_KEY_ID: The access key for your AWS account.
* AWS_SECRET_ACCESS_KEY: The secret key for your AWS account.

Users can follow instructions on https://www.cyberciti.biz/faq/set-environment-variable-linux/ To set environment variables on Linux http://www.computerhope.com/issues/ch000549.htm on Windows.

Besides environment variables, users can also choose to store credentials in some specific files such as .aws/credentials. To know more options about where to store S3 credentials , users can read http://boto3.readthedocs.io/en/latest/guide/configuration.html

<a name="running"/>
### Running Application
Everything has already been set if the website is to be hosted locally. Users now need to go to HairyDolphins/src/main/python folder and run command:

```
python runserver.py 
```

Now you should be able to browse HairyDolphins website through url localhost:8080 in the browser.
![alt text](https://github.com/SamLin95/HairyDolphins/blob/master/repo_resources/success_installed.png "Installed Successfully")
To know more about how HairyDolphins can be hosted on a real server, users can continue to read the following section below. 

<a name="deploy"/>
### Deploy HairyDolphins To A Real Server (Optional)
HairyDolphins is implemented in Python flask which has its built-in server. However, Flask’s built-in server is not suitable for production as it doesn’t scale well and by default serves only one request at a time. Fortunately,  Flask application object is the actual WSGI application which is able to be deployed to a WSGI server and there are a lot of options available. Some of options and corresponding deployment guidance can be found on http://flask.pocoo.org/docs/0.11/deploying/.


Here we will take latest Apache2 server as an example to introduce a very basic approach to hosting HairyDolphins on a server running Ubuntu system.


#### Step1. Install Apache2
Users need Apache2 to be installed on the server machine. Installing Apache2 on Ubuntu can be achieved simply by the command:

```
sudo apt-get apache2
```

#### Step2. Install HairyDolphins
Users now need to follow instructions given in the installation section before to install HairyDolphins on the server. The HairyDolphins directory is suggested to be stored to the path /var/www/html according to the custom.


#### Step3. Install mod_wsgi And Create .wsgi File
Besides Apache2 itself, an apache2 module named libapache2-mod-wsgi also needs to be installed to support hosting wsgi application. The command to install the module on Ubuntu is:

```
apt-get install libapache2-mod-wsgi
```

After installing the module, users need to create a .wsgi file for Apache2 to run the application. The .wsgi file uses the Python syntax and it needs to import the Flask object as application to allow Apache2 to handle. Assume that HairyDolphins directory is stored in /var/www/html/ as mentioned. The content of .wsgi file should look like:

```python
import sys
sys.path.insert(0, '/var/www/html/HairyDolphins/src/main/python')

from webapp import app as application
```

#### Step4. Configure Apache2
The last thing you have to do is to create an Apache configuration file for the application. The details about Apache2 configuration file can be found on the official website: http://httpd.apache.org/docs/2.0/configuring.html. And mod_wsgi has more configuration options, which can be found on: http://modwsgi.readthedocs.io/en/develop/configuration.html. 


A simple configuration file example(which should be created in /etc/apache2/sites-enabled/) is given as below given the fact that the .wsgi file created in the previous step is named hairydolphins.wsgi and its file path is /var/www/html/HairyDolphins/src/main/python/hairydolphins.wsgi.

```apacheconf
<VirtualHost *:80>
        #This should be your domain name
        ServerName www.hairydolphins.com
        #This would be the file path root for the following relative file path
        DocumentRoot /var/www/html
	
        #Configure a distinct daemon process for running WSGI applications.
        WSGIDaemonProcess www.hairydolphins.com threads=5
        #The file path of the .wsgi file needs to be referred here
        WSGIScriptAlias / /var/www/html/HairyDolphins/src/main/python/hairydolphins.wsgi

        <Directory HairyDolphins/src/main/python/webapp>
            #Sets which process group WSGI application is assigned to.
            WSGIProcessGroup www.hairydolphins.com
            #Sets which application group WSGI application belongs to.
            WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        </Directory>

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```


Apache2 needs to be restarted to make the configuration file effective. The command to restart Apache2 is:
```
sudo service apache2 restart
```
Notice that users still can not access the website through the domain name set in the configuration yet if the domain name is not actually owned. The final step that is required to take is to purchase the domain name and associate the domain with the server IP address.

<a name="troubleshooting"/>
### Troubleshooting
When users are installing python dependencies, they sometimes have trouble installing psycopg2, which is a PostgreSQL adapter for the Python. Some error messages reported are:


##### Error: pg_config executable not found.

The error message means you have probably not installed the PostgreSQL on your server. You will need to install PostgreSQL by following the link : https://wiki.postgresql.org/wiki/Detailed_installation_guides.


##### Error: You need to install postgresql-server-dev-X.Y for building a server-side extension or libpq-dev for building a client-side application.

You may see this error when libpq header files are lacked. You will need to install the package postgresql-server-dev-9.5 by using command:
sudo apt-get install postgresql-server-dev-9.5


If you have other problems when installing psycopg2 using pip, you will be able to find more details on the package’s offical site: http://initd.org/psycopg/docs/install.html#requirements

If you have any question about this installation guide, please contact huangdun@gatech.edu.
