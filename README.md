# MediBuddy Server

- [1. Requirements](#1-requirements)
- [2. Getting started](#2-getting-started)
- [3. Command overview](#3-command-overview)
- [4. API endpoints](#4-api-endpoints)

<br>

## 1. Requirements

- Python 3.14
- Pipenv

<br>

## 2. Getting started

First, install all dependencies in the Pipenv virtual environment:
```shell
$ pipenv shell
$ pipenv install
```

<br>

Then copy-paste the `.env.example` and change the settings according to your needs.
Finally you will be able to start the server in development mode.

```shell
$ pipenv run python manage.py runserver
```

<br>

## 3. Command overview

<br>

### migrate (Django management command)

Creates the required database structure.
> Note: If the database does not exist, it will be created automatically.

```
$ python manage.py migrate
```

<br>

### runserver (Django development server)

Starts the local development server using the current settings.

```
$ python manage.py runserver
```

<br>

### create_device (Custom)

Creates a device for specified users and assigns the configured number of boxes.

**Arguments**

- **Device Name**
    - Flag: ``--device-name``
    - Required: Yes
    - Type: String

- **Box amount**
    - Flag: ``--boxes``
    - Required: Yes
    - Type: Integer

- **User IDs**:
    - Flag: ``--users``
    - Required: Yes
    - Type: List of UUIDs

**Example**
```
$ python manage.py create_device \
    --device-name "example" \
    --boxes 3 \
    --users uuid1 uuid2
```

<br>

### seed_demo_data (Custom)

Description: Generates a demo device with boxes and schedules for testing purposes. <br>

**Arguments**

- **Test user**:
    - Flag: ``--test-user``
    - Required: Yes
    - Type: UUID 

**Example**
```
$ python manage.py seed_demo_data \
    --test-user uuid
```

<br>

## 4. API endpoints
This project uses Swagger UI for API documentation.

You can access the documentation at:

```
/api/docs
```

For local development:

```
http://localhost:8000/api/docs
```




