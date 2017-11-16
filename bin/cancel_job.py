import json, urllib, random, string
from flask import request, jsonify, render_template
from bin import app, mysql



@app.route("/cancel_job", methods=['POST'])
def cancel_job():
  
  job_id =  request.get_json().get('job_id','')

  cursor = mysql.connection.cursor()
  
  #CALL `dispatcher`.`driver_close_job`(<{IN p_idDriver INT}>, <{IN p_idJob INT}>, <{IN p_status ENUM('complete', 'canceled')}>);	
  #TODO Check to see if driver claimed Job. If so, notify them.
  cursor.callproc('business_close_job', [job_id, 'canceled'])
  
  data = cursor.fetchall()
  cursor.close()
  
  #Check for Error is DB call
  if len(data) is 0:
        mysql.connection.rollback()
        return jsonify({'status':"success"})
  if data[0].get('status') == 'error':
        #TODO: display the meaningful error:
        #data[0].get('message')
        mysql.connection.rollback()
        return jsonify({'status':'error: ' + str(data[0].get('message'))})
    
   #commit changes to DB
  mysql.connection.commit()
  return jsonify({'status':"success"})
