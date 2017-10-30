import json, urllib
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template,url_for,redirect
from flask.ext.mysql import MySQL
import bin.sms.send_sms
import random
import hashlib
app = Flask(__name__)


#MySQL Connection
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'dispatcher'
app.config['MYSQL_DATABASE_PASSWORD'] = 'dispatcher'
app.config['MYSQL_DATABASE_DB'] = 'dispatcher'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/create_job", methods=['POST','GET'])
def create_job():

	conn = mysql.connect()
	cursor = conn.cursor()
	
	#TODO grab info from post request here, throw into correct vars
	#merchant ID is the only thing that is required, rest just pass in empty string if you don't want to worry about it for now
	_m=hashlib.md5()
	_body=""
	_merch_id = request.get_json().get('merch_id','')
	_job_title = request.get_json().get('job_title','')
	_job_desc = request.get_json().get('job_desc','')
	_from_loc = request.get_json().get('from_loc','')
	_to_loc = request.get_json().get('to_loc','')
	_bus_phone = request.get_json().get('bus_phone','')
	cursor.execute("SELECT BusName FROM Business WHERE MerchantID = "+_merch_id)
	_bus_name=cursor.fetchone()
	_body="New Job from "+ _bus_name
	m.update(_merch_id+_job_title+_job_des+_from_loc+_to_loc+_bus_phone)
	
	
	#call database stored proc
	#CALL `dispatcher`.`create_job`(<{IN p_merch_id CHAR(32)}>, <{IN p_title VARCHAR(64)}>, <{IN p_desc VARCHAR(256)}>, <{IN p_from_loc VARCHAR(256)}>, <{IN p_to_loc VARCHAR(256)}>, <{IN p_bus_phone CHAR(15)}>);
	cursor.callproc('create_job',(_merch_id,_job_itle,_job_desc,_from_loc,_to_loc,_bus_phone))

	data = cursor.fetchall()
 
	if len(data) is 0:
		return jsonify({'status':"ERROR: Empty Response"})
	if data[0] is 'error':
		return jsonify({'status':'error: ' + str(data[1])})
	_job_id=data[0]	
	
	res = ""
	for num in data[1:]:
		# row will contain a phone number that needs to recieve message.
		#TO DO: create unique link and add it to the body before sending text
		m.update(num)
		salt = random.randint(0,1000000000)
		m.update(salt)
		_job_hash=m.hexdigest() % 10**8
		unique_url=url_for('claim_page',hashed_value=_job_hash)
		#TO DO: store url in DB and associated with a jobID
		body=body+" claim link: "+unique_url
		############################sms.send_sms.send(num, body)
		
	#commit changes to DB
	conn.commit()
	cursor.close()
	conn.close()
	return jsonify({'status':"success"})

@app.route("/claim_page/<hashed_value>",methods=["POST","GET"])
def claim_page(hashed_value):
	conn = mysql.connect()
	cursor = conn.cursor()
	
	cursor.execute("SELECT jobID FROM <TableName> WHERE <uniqueJobID> = "+hashed_value)
	_job_id=cursor.fetchone()
	cursor.execute("SELECT job_status FROM <TableName> Where <uniqueJobID> = "+_job_id)
	_job_status=cursor.fetchone()
	if(_job_status == "open")
		cursor.execute("SELECT driverID FROM <TableName> WHERE <uniqueJobID> = "+hashed_value)
		_driver = cursor.fetchone()	
		# db call change _job_status and assign driver 
		cursor.close()
		conn.close()
		return render_template('claim.html',_bus_name=_bus_name,_job_title=_jobtitle,_job_desc=_job_desc,_from_loc=_from_loc,_to_loc=_to_loc,_bus_phone=bus_phone)
	
	else
		cursor.execute("SELECT driverID FROM <TableName> WHERE <uniqueJobID> = "+hashed_value)
		_driver_current_accessor = cursor.fetchone()	
		
		cursor.execute("SELECT driverID FROM <TableName> WHERE <JobID> = "+_job_id)
		_driver_actual = cursor.fetchone()	
		if(_driver_current_accessor==_driver_actual)
			## go to endpoint for canceling and completing a job
			cursor.close()
			conn.close()
			return render_template('can_comp.html')
		cursor.close()
		conn.close()
		return render_template('taken.html',...) #add aditional info
	

