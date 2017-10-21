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

@app.route("/create_job", methods=['POST','GET'])
def create_job():
	#TODO grab info from post request here, throw into correct vars
	#merchant ID is the only thing that is required, rest just pass in empty string if you don't want to worry about it for now
	#_m=hashlib.md5()
	_body=""
	_merch_id = request.get_json().get('merch_id','')
	_job_title = request.get_json().get('job_title','')
	_job_desc = request.get_json().get('job_desc','')
	_from_loc = request.get_json().get('from_loc','')
	_to_loc = request.get_json().get('to_loc','')
	_bus_phone = request.get_json().get('bus_phone','')
	
	_body="New Job from ..."
	#m.update(merchID+body)
	#_jobID=m.hexdigest() % 10**8
	#body=body+jobID
	
	#call database stored proc
	#CALL `dispatcher`.`create_job`(<{IN p_merch_id CHAR(32)}>, <{IN p_title VARCHAR(64)}>, <{IN p_desc VARCHAR(256)}>, <{IN p_from_loc VARCHAR(256)}>, <{IN p_to_loc VARCHAR(256)}>, <{IN p_bus_phone CHAR(15)}>);
	cursor.callproc('create_job',(_merch_id,_job_itle,_job_desc,_from_loc,_to_loc,_bus_phone))

	data = cursor.fetchall()
 
	if len(data) is 0:
		return jsonify({'status':"ERROR: Empty Response"})
	if data[0] is 'error':
		return jsonify({'status':'error: ' + str(data[1])})
	
	
	res = ""
	for num in data:
		# row will contain a phone number that needs to recieve message.
		#TO DO: create unique link and add it to the body before sending text
		sms.send_sms.send(num, body)
	
	#commit changes to DB
	conn.commit()
	
	return jsonify({'status':"success"})
