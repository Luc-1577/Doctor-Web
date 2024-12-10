import flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
import random as rd
import hashlib as hs
from datetime import timedelta as time
from datetime import date as dt

def hash_sha(password):
    sha256_ = hs.sha256()
    sha256_.update(password.encode())
    
    return sha256_.hexdigest()


load_dotenv()


app = flask.Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')
app.config['MYSQL_HOST'] = os.getenv('HOST')
app.config['MYSQL_USER'] = os.getenv('USER')
app.config['MYSQL_PASSWORD'] = os.getenv('PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DATABASE')
app.config['PERMANENT_SESSION_LIFETIME'] = time(hours=12)

sql = MySQL(app)


@app.route('/')
@app.route('/home')
def home():
    return flask.render_template('index.html')

@app.route('/news-detail.html')
def news():
    return flask.render_template('news-detail.html')

@app.route('/submit/appointment', methods=['POST'])
def make_appointment():
    name = flask.request.form.get('name')
    email = flask.request.form.get('email')
    date = flask.request.form.get('date')
    department = flask.request.form.get('department')
    phone = flask.request.form.get('phone')
    message = flask.request.form.get('message')
    
    date = date[8:] + date[4:8] + date[:4]

    cursor = sql.connection.cursor()
    cursor.execute(f'insert into pacients (name, email, telephone, message) values (%s, %s, %s, %s)', (name, email, phone, message))
    
    cursor.execute('select pacient_id from pacients where name = %s and telephone = %s', (name, phone))
    pacient_id = cursor.fetchall()
    
    cursor.execute('select doctor_id from doctors where department = %s', (department,))
    doctor_id = cursor.fetchall()
    doctor_id = rd.choice(doctor_id)
    
    cursor.execute(f'insert into appointments (pacient_id, doctor_id, department, date_) values (%s, %s, %s, %s)', (pacient_id, doctor_id, department, date))
    sql.connection.commit()
    cursor.close()
    
    return flask.redirect(flask.url_for('home'))

@app.route('/doctor')
@app.route('/doctor/login')
def login():
    
    return flask.render_template('login.html')

@app.route('/submit/login', methods=['POST'])
def user_check():
    username = flask.request.form.get('username')
    password = hash_sha(flask.request.form.get('password'))

    cursor = sql.connection.cursor()
    cursor.execute('select name, doctor_id from doctors where username = %s and password = %s', (username, password))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return flask.redirect(flask.url_for('login'))
    
    name = str(result[0][0])
    id = str(result[0][1])

    if not name.isalpha():
        return login()

    flask.session['user'] = id
        
    return flask.redirect(flask.url_for('user_page', name=name))    

@app.route('/doctor/<name>')
def user_page(name):
    user = flask.session.get('user')
    if not user:
        return flask.redirect(flask.url_for('login'))

    cursor = sql.connection.cursor()
    cursor.execute('select name from doctors where doctor_id = %s', (user,))
    name_db = cursor.fetchall()
    name_db = str(name_db[0][0])
        
    if name.title() != name_db:
        return flask.redirect(flask.url_for('login'))

    cursor = sql.connection.cursor()
    cursor.execute('''
                SELECT 
                    appointments.appointment_id, 
                    doctors.name AS doctor_name,
                    doctors.department AS doctor_department, 
                    pacients.name AS pacient_name, 
                    appointments.department, 
                    appointments.date_
                FROM 
                    appointments
                INNER JOIN 
                    doctors ON appointments.doctor_id = doctors.doctor_id
                INNER JOIN 
                    pacients ON appointments.pacient_id = pacients.pacient_id
                ''')

    result = cursor.fetchall()
    result = list(result)


    cursor.execute('SELECT department FROM doctors WHERE doctor_id = %s', (user,))
    
    department = cursor.fetchall()
    department = str(department[0][0])
        
    info = []
    
    for n in range(len(result)):
        if department in result[n] and name_db in result[n]:
            info.append(result[n])
    
    appointments = {'ID': '',
                    'Doctor': '',
                    'Doctor department': '',
                    'Pacient': '',
                    'Department': '',
                    'Date': ''}

    table = []
    date = str(dt.today())
    date = date[8:] + date[4:8] + date[:4]
    
    for i in range(len(info)):
        appointment = appointments.copy()
        for j, key in enumerate(appointments.keys()):
            appointment[key] = info[i][j]
            if appointment['Date'] == date:
                table.append(appointment)

    key_remove = ['Doctor', 'Doctor department', 'Department']
  
    for x in range(len(table)):
        for drop in key_remove:
            table[x].pop(drop)
    
    return flask.render_template('doctor.html', name=name_db, appointments=table)

@app.route('/doctor/update', methods=['POST'])
def update_credentials():
    user = flask.session.get('user')
    if user:
        new_username = flask.request.form.get('new_username')
        new_password = flask.request.form.get('new_password')
        
        cursor = sql.connection.cursor()
        if new_username:
            cursor.execute('update doctors set username = %s where doctor_id = %s', (new_username, user))
            sql.connection.commit()

        if new_password:
            new_password = hash_sha(new_password)
            cursor.execute('update doctors set password = %s where doctor_id = %s', (new_password, user)) 
            sql.connection.commit()
        
        cursor.close()

    return flask.redirect(flask.url_for('login'))

@app.route('/logout')
def logout():
    flask.session.clear()
    
    return flask.redirect(flask.url_for('login'))
    
    
if __name__ == '__main__':
    app.run(debug=False)