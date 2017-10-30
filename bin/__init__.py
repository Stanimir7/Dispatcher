import json, urllib, random, string
from flask import Flask
from flask import request
from flask import jsonify
from flask_mysqldb import MySQL
import bin.sms.send_sms
#import hashlib
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



@app.route("/")
def hello():
    return "Hello World!"

@app.route("/create_job", methods=['POST','GET'])
def create_job():
    #TODO grab info from post request here, throw into correct vars
    #merchant ID is the only thing that is required, rest just pass in empty string if you don't want to worry about it for now
    #_m=hashlib.md5()
    _body=""
    _merchID = 1
    _jobTitle = request.get_json().get('Job Title','')
    _jobDesc = 'Job Description'
    _fromLoc = '123 Wallaby Lane'
    _toLoc = '567 Pizza Pls'
    _busPhone = ''
    
    body=_jobTitle+_jobDesc+"from:"+_fromLoc+"to:"+_toLoc
    #m.update(merchID+body)
    #_jobID=m.hexdigest() % 10**8
    #body=body+jobID
    conn = mysql.connect()
    cursor = conn.cursor()
    #call database stored proc
    #CALL `dispatcher`.`create_job`(<{IN p_merch_id CHAR(32)}>, <{IN p_title VARCHAR(64)}>, <{IN p_desc VARCHAR(256)}>, <{IN p_from_loc VARCHAR(256)}>, <{IN p_to_loc VARCHAR(256)}>, <{IN p_bus_phone CHAR(15)}>);
    #cursor.callproc('create_job',(_merchID,_jobTitle,_jobDesc,_fromLoc,_toLoc,_busPhone))
    
    data = cursor.fetchall()
 
    if len(data) is 0:
        return jsonify({'status':"ERROR: Empty Response"})
    if data[0] is 'error':
        return jsonify({'status':'error: ' + str(data[1])})
    
    
    res = ""
    for num in data:
        # row will contain a phone number that needs to recieve message. literally just do
        # sms.send_sms.send(row)
        res = res + str(num)
        #sms.send_sms.send(num, body)
    
    #commit changes to DB
    conn.commit()
    
    return jsonify({'status':"success"})


@app.route("/register_driver", methods=['POST'])
def register_driver():
    try:
        _firstName = request.get_json().get('first_name','')
        _lastName = request.get_json().get('last_name','')
        _phoneNumber = request.get_json().get('phone_number','')
        
        #Connect to DB, call stored proc, close is handled automatically?
        cursor = mysql.connection.cursor()
        cursor.callproc('new_driver',(_firstName, _lastName, _phoneNumber))
        data = cursor.fetchall()
        cursor.close()
        #we are not expecting any data in response except in error
        if len(data) is not 0:
            res = jsonify(data[0])
            #res = jsonify({'status':str(data[0]),
            #               'message':str(data[1])})
            mysql.connection.rollback()
        else:
            #commit changes to DB
            mysql.connection.commit()
            res = jsonify({'status':"success"})
    except Exception as e:
        res = jsonify({'status':str(e)})
    return res

@app.route("/deregister_driver", methods=['POST'])
def deregister_driver():
    try:
        _key = request.form.get('key')
        _conf_code = request.form.get('conf_code')
        
        cursor = mysql.connection.cursor()
        cursor.callproc('check_confirm_code',[_key, _conf_code])
        data = cursor.fetchall()
        cursor.close()
        if len(data) is not 0:
            res = "invalid combo"
            mysql.connection.rollback()
        else:
            mysql.connection.commit()
            #TODO: grab all info about businesses that have hired this driver, display in form with checkboxes
            #   Display "deregister from dispatcher as a whole" button
        
        
    except Exception as e:
        res = jsonify({'status':str(e)})
    return res


@app.route("/confirm_code", methods=['POST'])
def confirm_code():
    try:
        _phoneNumber = request.get_json().get('phone_number','')
        
        #Connect to DB, call stored proc, close is handled automatically?
        cursor = mysql.connection.cursor()
        cursor.callproc('get_driver',[_phoneNumber])
        data = cursor.fetchall()
        cursor.close() 
        if len(data) is 0:
            res = jsonify({'status':'error','message':'Empty response'})
            mysql.connection.rollback()
        elif 'status' in data[0]: #status only in error state
            res = jsonify(data[0])
            mysql.connection.rollback()
        else:
            id_driver = data[0].get('idDriver')
            conf_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            cursor = mysql.connection.cursor()
            cursor.callproc('new_confirm_code',[id_driver, conf_code])
            data = cursor.fetchall()
            cursor.close()
            if len(data) is 0:
                res = jsonify({'status':'error','message':'Empty response'})
                mysql.connection.rollback()
            else:
                if do_sms:
                    sms.send_sms.send(_phoneNumber, 'Your Dispatcher Confirmation Code: \n'+conf_code)
                res = jsonify(data[0])
                mysql.connection.commit()

    except Exception as e:
        res = jsonify({'status':str(e)})
    return res
    
    
if __name__ == "__main__":
    app.run(debug=True)

