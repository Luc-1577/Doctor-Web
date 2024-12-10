# Doctor-Web

This is a back-end web application built using Flask, MySQL, and dotenv for managing doctor appointments.

## Features

- Patient can submit appointment requests.
- Doctors can log in to view their appointments for the day.
- Secure authentication using hashed passwords.
- Support for managing doctor's credentials (username and password).

## Technologies Used

- **Flask** - A micro web framework for Python.
- **MySQL** - A relational database management system.
- **Python-dotenv** - A module to load environment variables from `.env` files.
- **Flask-MySQLdb** - A MySQL extension for Flask.
- **Hashlib** - A library to hash passwords using SHA-256.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Luc-1577/Doctor-Web.git
   ```

2. Navigate into the project directory:

   ```bash
   cd doctor-web
   ```

3. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Change the `.env` file with your MySQL credentials:

   ```dotenv
   SECRET_KEY=your-secret-key
   HOST=your-database-host
   USER=your-database-user
   PASSWORD=your-database-password
   DATABASE=your-database-name
   ```

5. Run the Flask application:

   ```bash
   python app.py
   ```
   
## Routes

- **`/` or `/home`**: Displays the homepage.
- **`/submit/appointment`**: Handles appointment submissions.
- **`/doctor/login`**: Login page for doctors.
- **`/submit/login`**: Handles doctor login.
- **`/doctor/<name>`**: Doctor's appointment overview page.
- **`/doctor/update`**: Allows doctors to update their username and password.
- **`/logout`**: Logs out the current doctor and clears the session.

## Database Schema

The application uses the following tables:

- **pacients**: Stores patient information (name, email, phone, message).
- **doctors**: Stores doctor information (username, password, department).
- **appointments**: Stores appointment details (pacient_id, doctor_id, date, department).

## Acknowledgments

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-MySQLdb Documentation](https://flask-mysqldb.readthedocs.io/en/latest/)
- [Python-dotenv Documentation](https://pypi.org/project/python-dotenv/)
