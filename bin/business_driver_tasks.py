import json, urllib, random, string
from flask import request, jsonify, render_template, url_for, redirect
from bin import app, mysql, do_sms
import bin.oauth

#This allows the business to modify a driver's status and allows them to be moved between
#the Pending, Hired, and Blocked lists. The new status is pulled from the json along with
#the specified Driver and Business and updates the Database accordingly. 
@app.route("/business_mod_driver", methods=['POST'])
def business_mod_driver():
	#auth check
	if bin.oauth.curr_business_id == '': 
		return jsonify({'status':'error','message':'Not authenticated'})
	
	id_bus = request.get_json().get('id_bus','')
	id_driver = request.get_json().get('id_driver','')
	new_status = request.get_json().get('new_status','')
	
	cursor = mysql.connection.cursor()
	cursor.callproc('mod_business_driver',[id_driver,id_bus,new_status])
	data = cursor.fetchall()
	cursor.close()

	if len(data) is not 0:
		mysql.connection.commit()
		return jsonify(data[0])
	else:
		mysql.connection.rollback()
		return jsonify({'status':'error','message':'empty response'})
	
	
	
	
	
