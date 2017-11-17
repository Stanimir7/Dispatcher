import json, urllib, random, string
from flask import request, jsonify, render_template
from bin import app, mysql



@app.route("/register_business", methods=['POST'])
def register_business():
    merchID =  request.get_json().get('merch_id','')
    merchName =  request.get_json().get('merch_name','')
    phoneNum=  request.get_json().get('phone_num','')
    address=  request.get_json().get('merch_address','')
    
    
    unique_url = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))

    cursor = mysql.connection.cursor()
    #call database stored proc
    #CALL `dispatcher`.`new_business`(<{IN p_merch_id CHAR(32)}>, <{IN p_name VARCHAR(128)}>, <{IN p_address VARCHAR(256)}>, <{IN p_phone CHAR(15)}>);
    cursor.callproc('new_business',[merchID,merchName,address,phoneNum,unique_url])
    
    data = cursor.fetchall()
    cursor.close()
    
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
