import json, urllib, random, string
from flask import request, jsonify, render_template
from bin import app, mysql, do_sms
from bin.sms import send_sms

@app.route("/confirm_code", methods=['POST'])
def confirm_code():
    try:
        _phoneNumber = request.get_json().get('phone_number','')
        
        #Connect to DB, call stored proc, close is handled automatically?
        cursor = mysql.connection.cursor()
        cursor.callproc('get_driver_from_phone',[_phoneNumber])
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
                    send_sms.send(_phoneNumber, 'Your Dispatcher Confirmation Code: \n'+conf_code)
                res = jsonify(data[0])
                mysql.connection.commit()

    except Exception as e:
        res = jsonify({'status':str(e)})
    return res
    