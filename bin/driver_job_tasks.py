import json, urllib, random, string
from flask import request, jsonify, render_template
from bin import app, mysql



@app.route("/driver_cancel_job", methods=['POST'])
def driver_cancel_job():
    _driver_id =  request.get_json().get('driver_id','')
    _job_id =  request.get_json().get('job_name','')
    
    cursor = mysql.connection.cursor()
    
    #CALL `dispatcher`.`driver_close_job`(<{IN p_idDriver INT}>, <{IN p_idJob INT}>, <{IN p_status ENUM('complete', 'canceled')}>);	
    cursor.callproc('driver_close_job', [driver_id, job_id, 'canceled'])
    
    data = cursor.fetchall()
    cursor.close()
    
    #Check for Error is DB call
    if len(data) is 0:
        mysql.connection.rollback()
        return jsonify({'status':'error','message': "ERROR: Empty Response"})
    if data[0].get('status') == 'error':
        #TODO: display the meaningful error:
        #data[0].get('message')
        mysql.connection.rollback()
        return jsonify({'status':'error: ' + str(data[0].get('message'))})

    #commit changes to DB
    mysql.connection.commit()
    return jsonify({'status':"success"})

@app.route("/driver_completed_job", methods=['POST'])
def driver_completed_job():
    _driver_id =  request.get_json().get('driver_id','')
    _job_id =  request.get_json().get('job_name','')
    
    cursor = mysql.connection.cursor()
    
    #CALL `dispatcher`.`driver_close_job`(<{IN p_idDriver INT}>, <{IN p_idJob INT}>, <{IN p_status ENUM('complete', 'canceled')}>);	
    cursor.callproc('driver_close_job', [driver_id, job_id, 'complete'])
    
    data = cursor.fetchall()
    cursor.close()
    
    #Check for Error is DB call
    if len(data) is 0:
        mysql.connection.rollback()
        return jsonify({'status':'error','message': "ERROR: Empty Response"})
    if data[0].get('status') == 'error':
        #TODO: display the meaningful error:
        #data[0].get('message')
        mysql.connection.rollback()
        return jsonify({'status':'error: ' + str(data[0].get('message'))})
    
    #commit changes to DB
    mysql.connection.commit()
    return jsonify({'status':"success"})
