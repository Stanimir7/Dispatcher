import json, urllib, random, string, phonenumbers
from flask import request, jsonify, render_template
from bin import app, mysql, do_sms
from bin.sms import send_sms

############################
####### Confirm Code #######
############################

#Checks that a phone number is valid then creates a unique confirmation code.
@app.route("/confirm_code", methods=['POST'])
def confirm_code():
    try:
        _phoneNumber = request.get_json().get('phone_number','')
        
        #subroutine is local to util.py
        p_num = format_phone_number(_phoneNumber)
        if p_num == '':
            return jsonify({'status':"error",
                           'message':'You did not supply a valid phone number. Please try again.'})

        
        #Connect to DB, call stored proc
        cursor = mysql.connection.cursor()
        cursor.callproc('get_driver_from_phone',[p_num])
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
                    send_sms.send(p_num, 'Your Dispatcher Confirmation Code: \n'+conf_code)
                res = jsonify(data[0])
                mysql.connection.commit()

    except Exception as e:
        res = jsonify({'status':'error',
                       'message':'Whoops, please try again.',
                       'debug':str(e)})
    return res

############################
### Format Phone Number ####
############################

# if valid phone number returns properly formatted num as string
#   otherwise, ""
def format_phone_number(in_num):
    try:
        p_num = phonenumbers.parse(in_num, None)
    except phonenumbers.phonenumberutil.NumberParseException:
        try:
            #try assuming US number
            p_num = phonenumbers.parse(in_num, "US")
        except phonenumbers.phonenumberutil.NumberParseException:
            #Give up
            return ""
    
    if phonenumbers.is_possible_number(p_num):
        return phonenumbers.format_number(p_num, phonenumbers.PhoneNumberFormat.E164)
    else:
        return ""
    
