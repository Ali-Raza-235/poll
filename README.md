
# Poll Application

This is a Django-based poll application that allows users to:

- **Register and Login**
- **Create, Update, and Delete Polls** (Login required)
- **Add Poll Responses** (Login required)
- **View Poll Responses**
- **Logout**

The application features user authentication for managing polls and responses. Additionally, it uses **Django REST Framework** to provide API endpoints for poll management.

## Features

- **User Authentication**: Users can register, log in, and log out.
- **Poll Management**: Users can create, update, and delete polls after logging in.
- **Poll Responses**: Users can add responses to polls and view responses. Login is required to add responses.

## Deployment Details

The project is deployed on an **Amazon EC2 Instance**, running on **port 8000** using `nohup` to keep the server running in the background.

### Steps to Deploy:

1. Launch an **EC2 instance** (Ubuntu) and configure security groups to allow HTTP (port 80) and custom TCP (port 8000).
2. SSH into the EC2 instance and install necessary dependencies (Python, Django, etc.).
3. Clone the project repository from GitHub.
4. Set up a virtual environment and install the required Python packages from `requirements.txt`.
5. Apply migrations and collect static files (if any).
6. Use **nohup** to run the Django application in the background:
   ```bash
   nohup python3 manage.py runserver 0.0.0.0:8000 &
   ```
7. The application will now be accessible at the EC2 public IP, such as [http://13.48.58.193:8000/](http://13.48.58.193:8000/).

