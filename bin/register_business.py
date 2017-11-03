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
app.config['MYSQL_USER'] = 'dispatcher'
app.config['MYSQL_PASSWORD'] = 'dispatcher'
app.config['MYSQL_DB'] = 'dispatcher'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS'] = 
mysql.init_app(app)

@app.route("/register_business", methods=['GET', 'POST'])
def register_business():
	_merchID =  request.get_json().get('merch_id','')
	_merchName =  request.get_json().get('merch_name','')
	_phoneNum=  request.get_json().get('phone_num','')
	_address=  request.get_json().get('merch_address','')
	
	cursor = mysql.connection.cursor()
	#call database stored proc
	#CALL `dispatcher`.`new_business`(<{IN p_merch_id CHAR(32)}>, <{IN p_name VARCHAR(128)}>, <{IN p_address VARCHAR(256)}>, <{IN p_phone CHAR(15)}>);
	cursor.callproc('new_business',(_merchID,_merchName,_address,_phoneNum))
	
	data = cursor.fetchall()
	cursor.close()
 
	if len(data) is 0:
		mysql.connection.rollback()
		return jsonify({'status':'error','message' ,"ERROR: Empty Response"})
	if data[0] is 'error':
		mysql.connection.rollback()
		return jsonify({'status':'error: ' + str(data[1])})
	
	#commit changes to DB
	mysql.connection.commit()
	return jsonify({'status':"success"})
