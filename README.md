
# Online Bus Booking System

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Setup Guide](#setup-guide)
   - [Clone the Repository](#1-clone-the-repository)
   - [Set Up the Virtual Environment](#2-set-up-the-virtual-environment)
   - [Install Dependencies](#3-install-dependencies)
   - [Create the .env File](#4-create-the-env-file)
   - [Set Up PostgreSQL Database](#5-set-up-postgresql-database)
   - [Update Settings](#6-update-settings)
   - [Apply Migrations](#7-apply-migrations)
   - [Run the Server](#8-run-the-server)
- [License](#license)

## Introduction
This project is an online bus booking system that provides users with the ability to book bus tickets, view real-time updates, and receive feedback. This guide will walk you through the steps to set up the project on your local machine.

## Prerequisites
Before you begin, ensure you have the following installed on your system:
- Python 3.x
- PostgreSQL
- Git

## Setup Guide

### 1. Clone the Repository
First, clone the project repository from GitHub:

git clone https://github.com/yourusername/online-bus-booking.git

cd online-bus-booking

### 2. Set Up the Virtual Environment
This is to manage dependencies:

python -m venv (name of env)

source (name of env)/bin/activate  # On Windows, use `(name of env)\Scripts\activate`
### 3. Install Dependencies
Install the required dependencies from the requirements.txt file:

pip install -r requirements.txt
### 4. Create the .env File
Create a .env file in the root directory of the project. This file will contain your confidential information. 

SECRET_KEY=YOUR_SECRET_KEY

DEBUG=True

EMAIL_HOST_USER= YOUR_EMAIL_HOST_USER

EMAIL_HOST_PASSWORD= YOUR_EMAIL_HOST_PASSWORD

GOOGLE_CLIENT_ID= YOUR_SECRET_CLIENT_ID

GOOGLE_CLIENT_SECRET= YOUR_GOOGLE_CLIENT_SECRET

GITHUB_SECRET= GITHUB_SECRET_INFO

GITHUB_CLIENT_ID=YOUR_CLIENT_ID

### 5. Set Up PostgreSQL Database
Create a PostgreSQL database. This will have all the tables relating to the project and a schema will be created. The name of the database is BusBooking.
### 6. Update Settings
In the settings.py file, update the DATABASES section to use PostgreSQL and your credentials from the .env file:

import os

from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': os.getenv('DB_NAME'),

        'USER': os.getenv('DB_USER'),

        'PASSWORD': os.getenv('DB_PASSWORD'),

        'HOST': os.getenv('DB_HOST'),

        'PORT': os.getenv('DB_PORT'),
    }
}
### 7. Apply Migrations
Initial database migrations are applied to so as to be in sync with the models created:
python manage.py makemigrations
python manage.py migrate
### 8. Run the Server
Start the development server:

python manage.py runserver
## License
Online Bus Booking is licensed under the [MIT license](https://opensource.org/licenses/MIT). Take a bow!


