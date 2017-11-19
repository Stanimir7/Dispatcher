import json, urllib, random, string
from flask import request, jsonify, render_template, url_for
from bin import app, mysql, do_sms

############################
######## Driver Claim Job Page ########
############################
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

        if data_url[0].get('JobStatus') != 'pending':
            cursor = mysql.connection.cursor()
            cursor.callproc('get_assoc_job_driver',[data_url[0].get('idJob')])
            driver = cursor.fetchall()
            cursor.close()
            mysql.connection.commit()

            if data_url[0].get('idDriver') == driver[0].get('idDriver'):
                #this is the driver that has claimed the job, allow them to cancel or complete job
                return render_template('driver_close_job.html',
                               unique_url = unique_url,
                               job_title = data_url[0].get("JobTitle"),
                               job_desc = data_url[0].get("JobDesc"),
                               bus_phone = data_url[0].get("BusContactPhone"),
                               from_loc = data_url[0].get("FromLoc"),
                               to_loc=data_url[0].get("ToLoc"))
                
            else:
                return render_template('message.html',
                               title='Job Taken',
                               message='Sorry, this job has been claimed. ')
        elif data_url[0].get('JobStatus') == 'pending':    
            return render_template('driver_job_claim.html',
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
    
############################
######## Claim Job Action ########
############################
	
@app.route("/claim_job/<unique_url>",methods=["POST","GET"])
def claim_job(unique_url):
    if request.form.get('claim') is not None:
        return render_template('message.html',
                       title='Whoops',
                       message='Don\'t try to access this page directly')
   # unique_url = request.form.get('unique_url')
    
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
    cursor.callproc('driver_claim_job',[data_url[0].get('idJob'), data_url[0].get('idDriver')])
    response = cursor.fetchall()
    cursor.close()
    if len(response) is 0:
        mysql.connection.rollback()
        return render_template('message.html',
                       title='Whoops',
                       message='Something went wrong, please try again.')
    elif response[0].get('status') == 'error':
        mysql.connection.rollback()
        if response[0].get('message') == 'invalid_driver_id':
            return render_template('message.html',
                           title='Whoops',
                           message='Are you sure you are who you say you are?')
        elif response[0].get('message') == 'invalid_job_id':
            return render_template('message.html',
                           title='Whoops',
                           message='What job are you trying to claim exactly?')
        #should never get here
        return render_template('message.html',
                       title='Whoops',
                       message='Something went wrong, please try again.')

    #Assume success if not error at this point
    mysql.connection.commit()
    if response[0].get('status') == 'success':
        return render_template('driver_close_job.html',
                       unique_url = unique_url,
                       job_title = data_url[0].get("JobTitle"), 
                       job_desc = data_url[0].get("JobDesc"), 
                       bus_phone = data_url[0].get("BusContactPhone"),
                       from_loc = data_url[0].get("FromLoc"), 
                       to_loc=data_url[0].get("ToLoc"))
    if response[0].get('status') == 'info':
        if response[0].get('message') == 'job_claimed':
            return render_template('message.html',
                           title='Job is not available',
                           message='Sorry, someone else has claimed the job')
        elif response[0].get('message') == 'job_not_available':
            return render_template('message.html',
                           title='Job is not available',
                           message='Sorry, this job is no longer available')
        #should never get here
        return render_template('message.html',
                       title='Whoops',
                       message='Something went wrong, please try again.')

    #should never get here
    return str(data_url)

############################
######## Driver Cancel and Complete Job Action ########
############################
@app.route("/driver_close", methods=["POST","GET"])
def driver_close():
    unique_url = request.form.get('unique_url')
    status = request.form.get('status')

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
                       message='Something went wrong, please try again. '+ data_url[0].get('message'))
    #Assume success if not error at this point
    mysql.connection.commit()
     
    cursor = mysql.connection.cursor()
    cursor.callproc('get_assoc_job_driver',[data_url[0].get('idJob')])
    driver = cursor.fetchall()
    cursor.close()
    if len(driver) is 0:
        mysql.connection.rollback()
        return render_template('message.html',
                       title='Whoops',
                       message='Something went wrong, please try again.')
    elif driver[0].get('status') == 'error':
        mysql.connection.rollback()
        return render_template('message.html',
                       title='Whoops',
                       message='Something went wrong, please try again. '+ driver[0].get('message'))
    mysql.connection.commit()
    
    if data_url[0].get('idDriver') == driver[0].get('idDriver'):
        #this is the driver that has claimed the job, he should be allowed to cancel it
        if data_url[0].get('JobStatus') == 'claimed':
           #the job is claimed, not pending, complete, or canceled. Allow to cancel or complete it
           cursor = mysql.connection.cursor()
           cursor.callproc('driver_close_job',[data_url[0].get('idDriver'),data_url[0].get('idJob'),status])
           isClosed = cursor.fetchall()
           cursor.close()
           if len(isClosed) != 0: #NO REPLY IS GOOD HERE, if you get a reply, something went wrong
               mysql.connection.rollback()
               return render_template('message.html',
                              title='Whoops',
                              message='Something went wrong, please try again. '+ isClosed[0].get('message'))
           mysql.connection.commit()
           #closed successfully
           if status == 'canceled': #if canceled resend text to all drivers who had gotten the url
               cursor = mysql.connection.cursor()
               cursor.callproc('get_assoc_drivers',[data_url[0].get('idBusiness')])
               list_of_drivers = cursor.fetchall()
               cursor.close()
               if len(list_of_drivers) is 0:
                   mysql.connection.rollback()
                   return render_template('message.html',
                                  title='Whoops',
                                  message='Something went wrong, there are no drivers to inform of this job becoming available again. Please contact the business at '+ data_url[0].get('DefaultPhone'))
               #assume you have a list of drivers
               mysql.connection.commit()
               for row in list_of_drivers:
                   cursor = mysql.connection.cursor()
                   cursor.callproc('get_url_from_driver_job',[row.get('idDriver'),data_url[0].get('idJob')])
                   url = cursor.fetchall()
                   cursor.close()
                   if len(url) is 0:
                       mysql.connection.rollback()
                       #if you can't find a url for this job for this driver, skip them
                   #assume you have the url
                   mysql.connection.commit()
                   body_link=url_for('claim_page',unique_url=url[0].get('URL'))
                   body="A job has opened up again, claim link: "+body_link
                   if do_sms:
                       send_sms.send(row.get('PhoneNumber'), body)

               return render_template('driver_job_claim.html', #if canceled in error, allow them to claim again and return them to the claim page
                              title='Claim Job',
                              bus_name=data_url[0].get('BusName'),
                              job_title=data_url[0].get('JobTitle'),
                              job_desc=data_url[0].get('JobDesc'),
                              from_loc=data_url[0].get('FromLoc'),
                              to_loc=data_url[0].get('ToLoc'),
                              bus_phone=data_url[0].get('BusContactPhone'),
                              #Driver's identifying info
                              unique_url=unique_url)
           elif status == 'complete':
               return render_template('message.html',
                              title='Job completed',
                              message='Job has been completed.')
        else:
           #if Job Status is not "claimed"
           return render_template('message.html',
                          title='Whoops',
                          message='Something went wrong, you\'re trying to cancel a job that has not been claimed')
    else:
        #this is not the driver that has claimed the job
        return render_template('message.html',
                       title='Whoops',
                       message='You are not the driver that has claimed this job, how did you get here?')  
   
