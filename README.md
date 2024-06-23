# Online Bus Booking Application
[![MIT License][mit-shield]][mit]

This work is licenced under a [MIT license](https://opensource.org/licenses/MIT). Take a bow!

[mit-shield]: https://img.shields.io/badge/License-MIT-blue.svg
[mit]: https://opensource.org/licenses/MIT

## Description
The Online Bus Booking Application is a web-based platform designed to streamline the process of booking bus tickets. The application enables users to search for available bus routes, view seat availability, book tickets and make secure payments online. It aims to simplify the ticket booking process, reduce the need for physical ticket counters and provide a convenient and efficient way for travelers to manage their bus journeys.Its main goal is to provide a seamless online platform for booking bus tickets in Kenya. It focuses on eliminating the hassle of visiting physical ticket counters, reducing waiting times and offering a user-friendly interface for managing bus travel.

## Project Setup

### Dependencies

The system requires the following libraries, packages, and frameworks:

- **Python** - Programming language
- **Django** - Web framework
- **HTML** - Markup language for structuring web pages
- **CSS** - Styling for web pages (using TailwindCSS)
- **PostgreSQL** - Database management system
- **PayPal SDK** - For payment integration
- **Mpesa SDK** - For payment integration

### Packages to Download
Visit these links and follow the instructions to ensure these packages are installed in one's machine. 
1. https://www.python.org/downloads/
2. https://www.postgresql.org/download/
   
### Installation Steps of Project

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/online-bus-booking.git
    cd online-bus-booking
    ```

2. **Create and Activate a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Create the .env File**

   Create a .env file in the root directory of the project. This file will contain your confidential information. 
   
   ```SECRET_KEY=YOUR_SECRET_KEY
   DEBUG=True
   
   EMAIL_HOST_USER= YOUR_EMAIL_HOST_USER
   
   EMAIL_HOST_PASSWORD= YOUR_EMAIL_HOST_PASSWORD
   
   GOOGLE_CLIENT_ID= YOUR_SECRET_CLIENT_ID
   
   GOOGLE_CLIENT_SECRET= YOUR_GOOGLE_CLIENT_SECRET
   
   GITHUB_SECRET= GITHUB_SECRET_INFO
   
   GITHUB_CLIENT_ID=YOUR_CLIENT_ID
   ```

4. **Set Up the Database**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a Superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```

7. **Access the Application**:
    Open your web browser and navigate to `http://127.0.0.1:8000`.

## Usage Instructions

### How to Run System

Use the following command:
```bash
python manage.py runserver
```

### Expected Input Format
User Registration - Email, password, username

Bus Search - Origin, destination, date of travel

Booking - Selected bus, seat number, payment details

### Output Format
Search Results - Available bus routes and seat availability

Booking Confirmation - Details of the booked ticket and payment receipt

## Project Structure
### Overview
```
C:.
|   .env
|   .gitignore
|   db.sqlite3
|   manage.py
|   prototype1
|   README.md
|   requirements.txt
|   tree_structure.txt
|   
+---backend
|   |   asgi.py
|   |   settings.py
|   |   urls.py
|   |   wsgi.py
|   |   __init__.py
|           
+---main
|   |   admin.py
|   |   apps.py
|   |   forms.py
|   |   models.py
|   |   signals.py
|   |   tests.py
|   |   urls.py
|   |   views.py
|   |   __init__.py
|   |   
|   +---migrations
|   |   |   0001_initial.py
|   |   |   0002_alter_otptoken_otp_code.py
|   |   |   0003_booking_bus_profile_route_alter_otptoken_otp_code_and_more.py
|   |   |   0004_remove_profile_id_user_remove_profile_profileimg_and_more.py
|   |   |   0005_alter_otptoken_otp_code_alter_profile_phone_number.py
|   |   |   __init__.py
|   |   |   
|   +---templates
|   |   |   base.html
|   |   |   resend_otp.html
|   |   |   verify_token.html
|   |   |   
|   |   +---main
|   |   |       base.html
|   |   |       home.html
|   |   |       
|   |   \---registration
|   |           login.html
|   |           password_reset_form.html
|   |           sign_up.html
|           
+---media
|   |   blank-profile-picture.png
|   |   
|   \---profile_images
|           bus.jpg
|           homepage.jpg
|           Screenshot_2024-05-30_222652.png
|           
+---static
|   +---assets
|   \---Images
|           blank-profile-picture.png
|           bus.jpg
|           homepage.jpg
|           
\---templates
    |   setting.html
    |   
    \---registration
            password_reset_complete.html
            password_reset_confirm.html
            password_reset_done.html
            password_reset_email.html
            password_reset_form.html
```
* File tree generated using command `tree /F /A > tree_structure.txt`
### Key Files
manage.py - Lets one interact with this Django project in various ways.

settings.py - Contains configuration for the Django project, including database settings, installed apps, middleware and other settings.

models.py - Defines the data models for the application, representing the structure of the database.

urls.py - Contains URL declarations for the application. It maps URLs to the corresponding views.

## Additional Information
### Acknowledgement
This project is built using several open-source technologies and we would like to thank the developers of these technologies:
- [![Python][python-shield]][python]
- [![Django][django-shield]][django]
- [![PostgreSQL][postgresql-shield]][postgresql]
- [![HTML][html-shield]][html]

[python-shield]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[python]: https://www.python.org/

[django-shield]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white
[django]: https://www.djangoproject.com/

[postgresql-shield]: https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white
[postgresql]: https://www.postgresql.org/

[html-shield]: https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white
[html]: https://developer.mozilla.org/en-US/docs/Web/HTML
### Known Issues
1. Security Considerations
2. Validation and Error Handling
3. Payment Gateway Integration Issues
4. Real-time Seat Availability Updates
## Contact Information
For any inquiries, please contact us at:

https://github.com/Martinlenga

https://github.com/Chege-Gitiche


