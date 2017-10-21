import json, urllib
from flask import Flask
from flask import request
from flask import jsonify
from flask.ext.mysql import MySQL
import bin.sms.send_sms
#import hashlib
app = Flask(__name__)


#MySQL Connection
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'dispatcher'
app.config['MYSQL_DATABASE_PASSWORD'] = 'dispatcher'
app.config['MYSQL_DATABASE_DB'] = 'dispatcher'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

		
@app.route("/bin/register_driver")
def register_driver():
		_firstName
		_lastName
		_phoneNumber
		
		#call database stored proc
		cursor.callproc('register_driver',(_firstName, _lastName, _phoneNumber))
		
		return(0)