# Hostify

ALX Portfolio Project: Hostify is a platform designed to simplify Hotel booking services, focusing on streamlined setup, management, and monitoring

## Features
- Django-powered backend
- MySQL database integration
- Secure environment configurations using `.env`

## Installation
### Prerequisites
- Python 3.x
- MySQL

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/patrickodeh1/Hostify.git
   cd Hostify
2. Create a virtual environment and install dependencies:
    ```bash
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt

3. Set up the .env file:
    
    SECRET_KEY=your-very-secret-key
    DB_NAME=hostify_db
    DB_USER=your-username
    DB_PASSWORD=your-password
    DB_HOST=127.0.0.1
    DB_PORT=3306

4. Apply migrations and run the server:

    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

5. Access the application at http://127.0.0.1:8000/.

### Contributing

Contributions are welcome! Fork the repository and submit a pull request.

### Author

Patrick Odeh

### Appreciation

Gratitude to God, ALX staffs and students who has been very supportive and who I have learnt a lot from.
