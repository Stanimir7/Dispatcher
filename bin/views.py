import json, urllib, random, string
from flask import request, jsonify, render_template
from bin import app, mysql, do_sms, SUCCESSFUL_AUTH, hostname, endpoint_prefix
import bin.oauth

############################
######## Business ########
############################
@app.route("/business_home", methods=['GET'])
def business_home():
    #auth check
    make_template = lambda: render_template('business_home.html',
                           title='Home Page')
    return bin.oauth.handle_auth('/business_home', make_template)
   

def make_business_jobs_template():
    cursor = mysql.connection.cursor()
    cursor.callproc('get_business', [request.cookies.get('curr_business_id', default='')])
    bus_data = cursor.fetchall()
    cursor.close()
    bus_phone = ""
    from_loc = ""
    if len(bus_data) is 0 or bus_data[0].get('status') == 'error':
        mysql.connection.rollback()
    else:
        bus_phone = bus_data[0].get('DefaultPhone')
        from_loc = bus_data[0].get('DefaultAddress')
    return render_template('business_jobs.html',
            title='Jobs',
            idBusiness = request.cookies.get('curr_business_id', default=''),
            phoneNumber = bus_phone,
            address1 = from_loc
            )
        
    
@app.route("/business_jobs", methods=['GET'])
def business_jobs():
    return bin.oauth.handle_auth('/business_jobs', make_business_jobs_template)

def make_business_drivers_template():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Business WHERE idBusiness = %s", [ request.cookies.get('curr_business_id', default='')])
    data = cursor.fetchall()
    cursor.close()
    mysql.connection.commit()
    
    if len(data) is not 0:
        BusinessURL = hostname + endpoint_prefix + "/business_url/" + data[0].get('BusinessURL')
    else:
        BusinessURL = "No URL Defined"
    
    return render_template('business_drivers.html',
                       title='Drivers',
                       idBusiness= request.cookies.get('curr_business_id', default=''),
                       BusinessURL = BusinessURL
                       )

@app.route("/business_drivers", methods=['GET'])
def business_drivers():
    #auth check
    return bin.oauth.handle_auth('/business_drivers', make_business_drivers_template)    


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
