import json, urllib, random, string
from flask import request, jsonify, render_template
from bin import app, mysql, do_sms, SUCCESSFUL_AUTH
import bin.oauth

############################
######## Business ########
############################

@app.route("/business_jobs", methods=['GET'])
def business_jobs():
    #auth check
    auth_res = bin.oauth.force_auth("/business_jobs")
    if auth_res == SUCCESSFUL_AUTH:
        return render_template('business_jobs.html',
                           title='Jobs',
                           idBusiness = bin.oauth.curr_business_id
                           )
    else:
        return auth_res #MUST DO THIS; handles redirects, auth failure, etc
    

@app.route("/business_drivers", methods=['GET'])
def business_drivers():
    #auth check
    auth_res = bin.oauth.force_auth("/business_drivers")
    if auth_res == SUCCESSFUL_AUTH:
        return render_template('business_drivers.html',
                           title='Drivers',
                           idBusiness= bin.oauth.curr_business_id
                           )
    else:
        return auth_res #MUST DO THIS; handles redirects, auth failure, etc
    
    


@app.route("/business_new", methods=['GET'])
def business_new():
    
    return render_template('business_new.html',
                           title='Merchant Registration')


############################
######## Driver ########
############################

#Driver signup to business
@app.route("/business_url/<unique_url>", methods=['GET','POST'])
def business_url(unique_url):
    #get business from unique_url
    cursor = mysql.connection.cursor()
    cursor.callproc('get_business_from_url', [unique_url])
    bus_data = cursor.fetchall()
    cursor.close()

    if len(bus_data) is 0:
        mysql.connection.rollback()
        return render_template('message.html',
                                title='Whoops',
                                message='Something went wrong, please try again.')
    
    return render_template('business_url.html',
                           title='Apply',
                           bus_name=bus_data[0].get('BusName'),
                           unique_url=unique_url)

@app.route("/driver_home", methods=['GET'])
def driver_home():
    
    return render_template('driver_home.html',
                           title='Driver Home'
                           )

@app.route("/driver_signup", methods=['GET'])
def driver_signup():
    
    return render_template('driver_signup.html',
                           title='Driver Signup'
                           )

@app.route("/driver_deregister", methods=['GET'])
def driver_deregister():
    
    return render_template('driver_deregister.html',
                           title='Driver Signup'
                           )

@app.route("/driver_find_business", methods=['GET'])
def driver_find_business():
    
    return render_template('driver_find_business.html',
                           title='Find Signup URL'
                           )
