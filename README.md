# ArtFusion
ArtFusion is a social media website created with Django, where users can create posts, follow their favorite content creators, and see the latest posts by different users. The project utilizes SQLite3 as the database and AWS S3 for media file storage. It also makes use of Django's built-in services such as send_mail, messages, and models.
## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)


## Features
- User authentication and registration
- Profile creation and management
- Post creation with media file upload
- Follow/unfollow other users
- View latest posts by all users
- Integration with AWS S3 for media file storage
- Email notifications for various events

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
python -m venv yourenv
source yourenv/bin/activate  # On Windows use `yourenv\Scripts\activate`
```
### Install Dependencies
```
pip install -r requirements.txt
```
### Setup Environment Variables
Create a `.env` file in the project directory (same directory as `settings.py`) and add your AWS credentials and other necessary environment variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_STORAGE_BUCKET_NAME=your-s3-bucket-name
AWS_S3_REGION_NAME=your-aws-region-name
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
```
### Apply Migrations
```
python manage.py migrate
```
### Create a Superuser
```
python manage.py createsuperuser
```
### Collect Static Files For Production (Optional)
```
python manage.py collectstatic
```
### Run the Development Server
```
python manage.py runserver
```
Visit `http://127.0.0.1:8000` in your web browser to see the application running.

## Usage
### User Registration and Login
- Users can register by providing a username, email, and password.
- After registration, users can log in using their credentials.
### Profile Management
- Users can create and update their profile, including uploading a profile picture.
### Post Creation
- Users can create posts with text and media (images) that are stored in AWS S3.
### Following Users
- Users can follow and unfollow other users
### Viewing Posts
- Users can view the latest posts by all users on the homepage.

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

### Email Configuration
Set up your email settings in the `.env` file to enable email notifications.
