from flask import Flask, render_template, request
#for database
from flask_mysqldb import MySQL

app = Flask(__name__)

#Database settings for mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbase_trekapp'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/all')
def list():
    return "Hello, this is list page"

@app.route('/register')
def register():
    return render_template('register.html')
    
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/doLogin', methods=['POST'])
def doLogin():
    email = request.form['email']
    password = request.form['psw']

    cursor = mysql.connection.cursor()
    resp = cursor.execute('''SELECT * FROM users WHERE users_email=%s and users_password=%s;''',(email,password))

    user = cursor.fetchone()

    if resp==1:
        return render_template('home.html', result=user)
    else:
        return render_template('login.html',result={"Invalid Credentials"})

@app.route('/doRegister', methods=['POST'])
def doRegister():
    users_id = request.form['id']
    users_full_name = request.form['fullName']
    users_email =request.form['email']
    users_phone_number = request.form['phoneNumber']
    users_address = request.form['address']
    users_password = request.form['psw']

    cursor= mysql.connection.cursor()
    cursor.execute('''INSERT INTO users VALUES(%s,%s,%s,%s,%s,%s)''',(users_id, users_full_name, users_email, users_phone_number, users_address, users_password))
    mysql.connection.commit()
    cursor.close()

    return render_template('login.html', result="Registered Succesfully, Please login to continue...")

@app.route('/treks')
def treks():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT td.dest_id as 'SNO', td.dest_title as 'Title', td.dest_days as 'Days', td.dest_difficulty as 'Difficulty', td.dest_total_cost as 'Total Cost', td.dest_upvotes as 'Upvotes', u.users_full_name as 'FullName' FROM trek_destination as td JOIN users as u ON (td.users_id = u.users_id);''')

    treks = cursor.fetchall()
    cursor.close() 
    return render_template('listing.html', result= treks)

@app.route('/trek/<int:trekId>')
def getTrekbyId(trekId):
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT td.dest_id as 'SNO', td.dest_title as 'Title', td.dest_days as 'Days', td.dest_difficulty as 'Difficulty', td.dest_total_cost as 'Total Cost', td.dest_upvotes as 'Upvotes', u.users_full_name as 'FullName' FROM trek_destination as td JOIN users as u ON (td.users_id = u.users_id) WHERE td.users_id = %s;''',(trekId,))

    trek = cursor.fetchone()
    cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM `iternaries` WHERE dest_id=%s;''',(trekId,))
    itenaries = cursor.fetchall()
    cursor.close()

    return render_template('trekDetail.html', result={"trek": trek, "itenaries": itenaries})

app.run()