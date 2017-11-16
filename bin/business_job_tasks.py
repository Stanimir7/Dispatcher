import json, urllib, random, string
from flask import request, jsonify, render_template, url_for, redirect
from bin import app, mysql, do_sms
from bin.sms import send_sms


############################
######## Create Job ########
############################

@app.route("/create_job", methods=['POST','GET'])
def create_job():
    try:
        body=""
        #_merch_id = request.get_json().get('merch_id','')
        id_bus = request.get_json().get('id_bus','')
        _job_title = request.get_json().get('job_title','')
        _job_desc = request.get_json().get('job_desc','')
        _from_loc = request.get_json().get('from_loc','')
        _to_loc = request.get_json().get('to_loc','')
        _bus_phone = request.get_json().get('bus_phone','')
        
        cursor = mysql.connection.cursor()
        cursor.callproc('get_business',[id_bus])
        data = cursor.fetchall()
        cursor.close()
        
        if len(data) is 0:
            mysql.connection.rollback()
            return jsonify({'status': 'error','message': 'Empty DB Response1'})
        mysql.connection.commit()
        _bus_name=data[0].get('BusName')
        body="New Job from "+ _bus_name
        
        cursor = mysql.connection.cursor()
        cursor.callproc('create_job',[data[0].get('idBusiness'),_job_title,_job_desc,_from_loc,_to_loc,_bus_phone])
        data_create_job = cursor.fetchall()
        cursor.close()
        if len(data_create_job) is 0:
            mysql.connection.rollback()
            return jsonify({'status': 'error','message': 'Empty DB Response2'})
        elif data_create_job[0].get('status') == 'error': 
            mysql.connection.rollback()
            return jsonify(data_create_job[0])
        mysql.connection.commit()
        
        res = ''
        
        for row in data_create_job:
            unique_url = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))

            cursor = mysql.connection.cursor()
            cursor.callproc('new_job_driver_url',[row.get('idDriver'),row.get('idJob'),unique_url])
            data = cursor.fetchall()
            cursor.close()
            if len(data) is 0:
                mysql.connection.rollback()
                return jsonify({'status': 'error','message': 'Empty DB Response3'})
            elif data[0].get('status') == 'error': 
                mysql.connection.rollback()
                return jsonify(data_create_job[0])
            mysql.connection.commit()
            
            body_link=url_for('claim_page',unique_url=unique_url)
            body=body+" Claim link: "+body_link
            if do_sms:
                send_sms.send(row.get('PhoneNumber'), body)
                
            res = res + '|' + body
    except Exception as e:
        return jsonify({'status':str(e)})
    return jsonify({'status':'success'})

#################################
######## Cancel/Complete ########
#################################

#TODO consolidate cancel/complete into:
@app.route("/business_close_job", methods=['POST'])
def business_close_job():
    job_id =  request.get_json().get('job_id','')
    action =  request.get_json().get('action','')
    
    cursor = mysql.connection.cursor()
    cursor.callproc('business_close_job',[job_id,action])
    data = cursor.fetchall()
    cursor.close()
    #Check for Error is DB call
    if len(data) is 0:
          mysql.connection.commit()
          return jsonify({'status':"success"})
    if data[0].get('status') == 'error':
          #TODO: display the meaningful error:
          #data[0].get('message')
          mysql.connection.rollback()
          return jsonify({'status':'error: ' + str(data[0].get('message'))})
    
    
    
    

@app.route("/business_cancel_job", methods=['POST'])
def business_cancel_job():
  
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



@app.route("/business_complete_job", methods=['POST'])
def business_complete_job():
  
  job_id =  request.get_json().get('job_id','')

  cursor = mysql.connection.cursor()
  
  #CALL `dispatcher`.`driver_close_job`(<{IN p_idDriver INT}>, <{IN p_idJob INT}>, <{IN p_status ENUM('complete', 'canceled')}>);	
  #TODO Check to see if driver claimed Job. If so, notify them.
  cursor.callproc('business_close_job', [job_id, 'completed'])
  
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

