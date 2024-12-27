# ArtFusion
ArtFusion is a social media website created with Django, where users can create posts, follow their favorite content creators, and see the latest posts by different users. The project utilizes SQL database(PostgreSQL) and AWS S3 for media file storage. It also makes use of Django's built-in services such as send_mail, messages, and models.
## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)


## Features
- User registration and authentication
- Profile creation and management
- Post creation with media file upload (on AWS S3)
- Like&Comment on posts
- Follow/unfollow other users
- Integration with AWS S3 for media file storage
- Email notifications for various events (Post creation)

## Installation
### Prerequisites
- `Python 3.x`
- `pip` (Python package installer)
- virtualenv (optional but recommended)
- AWS account with S3 bucket

### Clone the Repository
```
git clone https://github.com/yourusername/ArtFusion.git
cd ArtFusion
```
### Create and Activate Virtual Environment (Optional But Recommended)
```
# create your python virtual environment
python -m venv yourenv

# activate virtual environment
# windows:
yourenv\Scripts\activate
# other(linux):
source yourenv/bin/activate  
```
### Install Dependencies
```
pip install -r requirements.txt
```
### Setup Environment Variables
Create a `.env` file in the root project directory and add your credentials and other necessary environment variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_STORAGE_BUCKET_NAME=your-s3-bucket-name
AWS_S3_REGION_NAME=your-aws-region-name
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
SQL_DB_URL=postgresql-or-any-other-sql-db-connection-url
```
see [configuration](#configuration).
### Apply Migrations
```
python manage.py makemigrations
python manage.py migrate
```
### Create a Superuser (Optional: For admin panel access)
```
python manage.py createsuperuser
```
### Collect Static Files (Optional: For running server in production)
```
python manage.py collectstatic
```
### Run the Development Server
```
python manage.py runserver
```
Visit `http://127.0.0.1:8000` in your web browser to see the application running.

## Configuration
### AWS S3 Configuration
Ensure your `AWS S3 bucket` is properly configured with the necessary permissions for file upload and access. You need to allow public read access for objects so that users can see photos on their browser through website.  
You can use following `bucket policy` for enabling public read access:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicRead",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectVersion"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name/post_images/*",
                "arn:aws:s3:::your-bucket-name/profile_pics/*"
            ]
        }
    ]
}
```
### Database Configuration
I have used render's PostgreSQL DB instance as hobby project for this project. And I have used Database's URL for direct configuration in database in `settings.py` with dj-database-url.
```
DATABASES = {
    'default': dj_database_url.parse(os.environ.get("SQL_DB_URL"))
}
```
You can search for detailed steps in google/youtube. Search: `render postgres database django`

## Usage
### User Registration and Login
- Users can register by providing a username, email, and password.
- After registration, users can log in using their credentials.
### Profile Management
- User can create and update their profile, including uploading a profile picture.
### Post
- User can create posts with media (images) that are stored in AWS S3.
- User can delete their posts.
- User can like or comment on other user's posts.
### Follow Users
- Users can follow and unfollow other users.

