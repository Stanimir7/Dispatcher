import json, urllib
from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_mysqldb import MySQL
import bin.sms.send_sms
import random, hashlib, string
app = Flask(__name__)
do_sms = False

#MySQL Connection
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_USER'] = 'dispatcher'
app.config['MYSQL_PASSWORD'] = 'dispatcher'
app.config['MYSQL_DB'] = 'dispatcher'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql.init_app(app)

@app.route("/create_job", methods=['POST','GET'])
def create_job():
    try:
        #TODO grab info from post request here, throw into correct vars
        #merchant ID is the only thing that is required, rest just pass in empty string if you don't want to worry about it for now
        #_m=hashlib.md5()
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
        #cursor.execute("SELECT BusName FROM Business WHERE MerchantID = "+_merch_id)
        _bus_name=data[0].get('BusName')
        body="New Job from "+ _bus_name
        #_m.update(_merch_id+_job_title+_job_desc+_from_loc+_to_loc+_bus_phone)
        
        
        #call database stored proc
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
            unique_url = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            
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
            
            #############################
            # Overkill hash stuff:
            #_m.update(row)
            #salt = random.randint(0,1000000000)
            #m.update(salt)
            #_job_hash=m.hexdigest() % 10**8
            #############################
            
            #body_link=url_for('claim_page',hashed_value=unique_url)
            body_link = unique_url
            body=body+" Claim link: "+body_link
            if do_sms:
                sms.send_sms.send(num, body)
                
            res = res + '|' + body
    except Exception as e:
        return jsonify({'status':str(e)})
    #return str(request.form)
    return res #should never get here

#@app.route("/claim_page/<hashed_value>",methods=["POST","GET"])
#def claim_page(hashed_value):
#    conn = mysql.connect()
#    cursor = conn.cursor()
#    
#    cursor.execute("SELECT jobID FROM <TableName> WHERE <uniqueJobID> = "+hashed_value)
#    _job_id=cursor.fetchone()
#    cursor.execute("SELECT job_status FROM <TableName> Where <uniqueJobID> = "+_job_id)
#    _job_status=cursor.fetchone()
#    if(_job_status == "open")
#        cursor.execute("SELECT driverID FROM <TableName> WHERE <uniqueJobID> = "+hashed_value)
#        _driver = cursor.fetchone()    
#        # db call change _job_status and assign driver 
#        cursor.close()
#        conn.close()
#        return render_template('claim.html',_bus_name=_bus_name,_job_title=_jobtitle,_job_desc=_job_desc,_from_loc=_from_loc,_to_loc=_to_loc,_bus_phone=bus_phone)
#    
#    else
#        cursor.execute("SELECT driverID FROM <TableName> WHERE <uniqueJobID> = "+hashed_value)
#        _driver_current_accessor = cursor.fetchone()    
#        
#        cursor.execute("SELECT driverID FROM <TableName> WHERE <JobID> = "+_job_id)
#        _driver_actual = cursor.fetchone()    
#        if(_driver_current_accessor==_driver_actual)
#            ## go to endpoint for canceling and completing a job
#            cursor.close()
#            conn.close()
#            return render_template('can_comp.html')
#        cursor.close()
#        conn.close()
#        return render_template('taken.html',...) #add aditional info
    

