# MediBuddy Server: Deployment

- [1. Initial Situation](#1-initial-situation)
    - [1.1 Setup non-root user](#11-setup-non-root-user)
    - [1.2 Installation fo global dependencies](#12-installation-fo-global-dependencies)
- [2. Setup Django Server](#2-setup-django-server)
- [3. Configure NGINX](#3-configure-nginx)
- [4. Add Support for HTTPS](#4-add-support-for-https)

<br>

## 1. Initial situation
The MediBuddy server deployment is based on Debian systems.
Most steps can be adapted for other Linux distributions.

<br>

### 1.1 Setup non-root user 

<br>

### 1.2 Installation fo global dependencies

The following dependencies must be installed before continuing:

- Python 3.14
- Pipenv

<br>

Verify your Python installation:

```shell
$ python3 --version
```

If Python is not installed or the version is lower than 3.14, follow the installation steps below.

<br>

#### 1.2.1 Install Python 3.14 on Debian

> Source: https://wiki.crowncloud.net/?Install_Python_3_14_on_Debian_13

<br>

First, update the operating system:

```shell
# apt-get update
# apt-get upgrade -y
```

Install the required build dependencies:

```shell
# apt-get install -y build-essential zlib1g-dev libncurses-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget curl llvm libbz2-dev xz-utils tk-dev liblzma-dev libncursesw6
```

Download and extract the Python source code:

```shell
# cd /usr/src
# wget https://www.python.org/ftp/python/3.14.0/Python-3.14.0.tgz
# tar xzf Python-3.14.0.tgz
# cd Python-3.14.0
```

Compile and install Python:

```shell
# ./configure --enable-optimizations
# make -j$(nproc)
# make altinstall
```

Install Pipenv:

```shell
# apt-get install pipenv
```

<br>

## 2. Setup Django server

<br>

### 2.1 Django base setup

Clone the repository into the application directory:

```shell
$ git clone git@github.com:nodedev7425/Medibuddy-backend.git /home/medibuddy/app
```

Create the virtual environment and install all dependencies:

```shell
$ cd /home/medibuddy/app
$ pipenv install
```

Copy the environment template:

```shell
$ cp .env.example .env
```

Update the following values inside the .env file:

```
SECRET_KEY=<new secret key>
DEBUG=False
ALLOWED_HOSTS=<your-domain>
CSRF_TRUSTED_ORIGINS=https://<your-domain>
STATIC_ROOT=/home/medibuddy/app/staticfiles
```

Restrict access to the environment file:

```shell
# chmod 600 .env
```

Run the database migrations:

```shell
$ pipenv run python manage.py migrate
```

Collect static files for production:

```shell
$ pipenv run python manage.py collectstatic
```

At this point, the Django application is ready to be served using Gunicorn and NGINX.

<br>

### 2.2 Gunicorn setup



<br>



## 3. Configurate NGINX

## 4. Add support for HTTPS


