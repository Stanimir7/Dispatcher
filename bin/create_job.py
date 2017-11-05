import json, urllib, random, string
from flask import request, jsonify, render_template, url_for, redirect
from bin import sms, app, mysql, do_sms

@app.route("/create_job", methods=['POST','GET'])
def create_job():
    try:
        body=""
        _merch_id = request.get_json().get('merch_id','')
        _job_title = request.get_json().get('job_title','')
        _job_desc = request.get_json().get('job_desc','')
        _from_loc = request.get_json().get('from_loc','')
        _to_loc = request.get_json().get('to_loc','')
        _bus_phone = request.get_json().get('bus_phone','')
        
        cursor = mysql.connection.cursor()
        cursor.callproc('get_business',[_merch_id])
        data = cursor.fetchall()
        cursor.close()
        
        if len(data) is 0:
            mysql.connection.rollback()
            return jsonify({'status': 'error','message': 'Empty DB Response'})
        mysql.connection.commit()
        _bus_name=data[0].get('BusName')
        body="New Job from "+ _bus_name
        
        cursor = mysql.connection.cursor()
        cursor.callproc('create_job',[data[0].get('idBusiness'),_job_title,_job_desc,_from_loc,_to_loc,_bus_phone])
        data_create_job = cursor.fetchall()
        cursor.close()
        if len(data_create_job) is 0:
            mysql.connection.rollback()
            return jsonify({'status': 'error','message': 'Empty DB Response'})
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
                return jsonify({'status': 'error','message': 'Empty DB Response'})
            elif data[0].get('status') == 'error': 
                mysql.connection.rollback()
                return jsonify(data_create_job[0])
            mysql.connection.commit()
            
            body_link=url_for('claim_page',unique_url=unique_url)
            body=body+" Claim link: "+body_link
            if do_sms:
                sms.send_sms.send(num, body)
                
            res = res + '|' + body
    except Exception as e:
        return jsonify({'status':str(e)})
    return jsonify({'status':'success'})

@app.route("/claim_page/<unique_url>",methods=["POST","GET"])
def claim_page(unique_url):
    #TODO: have this page be a manage job thing too, not just claim button
    #other than that, this is working
    try:
        cursor = mysql.connection.cursor()
        cursor.callproc('get_job_driver_from_url',[unique_url])
        data_url = cursor.fetchall()
        cursor.close()
        if len(data_url) is 0:
            mysql.connection.rollback()
            return render_template('message.html',
                           title='Whoops',
                           message='Something went wrong, please try again.')
        elif data_url[0].get('status') == 'error':
            mysql.connection.rollback()
            return render_template('message.html',
                           title='Whoops',
                           message='Something went wrong, please try again.' + data_url[0].get('message'))
        #Assume success if not error at this point
        mysql.connection.commit()
        
        cursor = mysql.connection.cursor()
        cursor.callproc('job_avail',[data_url[0].get('idJob')])
        data = cursor.fetchall()
        cursor.close()
        if data[0].get('avail') == 'false':
	    #wait for idAssignedDriver to be returned by job_avail before uncommenting
            #if(data_url[0].get('idDriver') == data[0].get('idAssignedDriver'):
                #this is the driver that has claimed the job, allow them to cancel or complete job
                #return render_template('cancel_complete.html',unique_url = unique_url)
            #else
                return render_template('message.html',
                           title='Job Taken',
                           message='Sorry, this job has been claimed. ')
        elif data[0].get('avail') == 'true':    
            return render_template('claim.html',
                           title='Claim Job',
                           bus_name=data_url[0].get('BusName'),
                           job_title=data_url[0].get('JobTitle'),
                           job_desc=data_url[0].get('JobDesc'),
                           from_loc=data_url[0].get('FromLoc'),
                           to_loc=data_url[0].get('ToLoc'),
                           bus_phone=data_url[0].get('BusContactPhone'),
                           #Driver's identifying info
                           unique_url=unique_url            
                           ) 
    except Exception as e:
        return jsonify({'status':str(e)})
    return 'end' #should never get here
    
@app.route("/claim_job",methods=["POST","GET"])
def claim_job():
    #TODO this is not complete
    #if not request.form.get('submit')
        #return
    unique_url = request.form.get('unique_url')
    
    cursor = mysql.connection.cursor()
    cursor.callproc('get_job_driver_from_url',[unique_url])
    data_url = cursor.fetchall()
    cursor.close()
    if len(data_url) is 0:
        mysql.connection.rollback()
        return render_template('message.html',
                       title='Whoops',
                       message='Something went wrong, please try again.')
    elif data_url[0].get('status') == 'error':
        mysql.connection.rollback()
        return render_template('message.html',
                       title='Whoops',
                       message='Something went wrong, please try again.' + data_url[0].get('message'))
    #Assume success if not error at this point
    mysql.connection.commit()
    
    #you now have all info through data_url
    
    
    return str(data_url)
    

