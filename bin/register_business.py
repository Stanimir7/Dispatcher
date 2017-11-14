import json, urllib, random, string
from flask import request, jsonify, render_template
from bin import app, mysql



@app.route("/register_business", methods=['POST'])
def register_business():
    _merchID =  request.get_json().get('merch_id','')
    _merchName =  request.get_json().get('merch_name','')
    _phoneNum=  request.get_json().get('phone_num','')
    _address=  request.get_json().get('merch_address','')
    
    cursor = mysql.connection.cursor()
    #call database stored proc
    #CALL `dispatcher`.`new_business`(<{IN p_merch_id CHAR(32)}>, <{IN p_name VARCHAR(128)}>, <{IN p_address VARCHAR(256)}>, <{IN p_phone CHAR(15)}>);
    cursor.callproc('new_business',[_merchID,_merchName,_address,_phoneNum,''])
    
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
