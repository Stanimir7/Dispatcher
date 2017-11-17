import json, urllib, random, string
from flask import request, jsonify, render_template
from bin import app, mysql


@app.route("/register_driver", methods=['POST'])
def register_driver():
    try:
        _firstName = request.get_json().get('first_name','')
        _lastName = request.get_json().get('last_name','')
        _phoneNumber = request.get_json().get('phone_number','')
        
        #Connect to DB, call stored proc, close is handled automatically?
        cursor = mysql.connection.cursor()
        cursor.callproc('new_driver',[_firstName, _lastName, _phoneNumber])
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

@app.route("/format_deregister_driver", methods=['GET','POST'])
def format_deregister_driver():
    try:
        _key = request.form.get('key')
        _conf_code = request.form.get('conf_code')
        
        cursor = mysql.connection.cursor()
        cursor.callproc('check_confirm_code',[_key, _conf_code])
        data = cursor.fetchall()
        cursor.close()
        
        if len(data) is 0:
            mysql.connection.rollback()
            return render_template('message.html',
                           title='Whoops',
                           message='Something went wrong, please try again.')
        elif data[0].get('status') == 'invalid':
            mysql.connection.rollback()
            return render_template('message.html',
                           title='Incorrect Code',
                           message="Incorrect confirmation code.")
        elif data[0].get('status') == 'success':
            
            mysql.connection.commit()
            id_driver = data[0].get('idDriver')
            
            cursor = mysql.connection.cursor()
            cursor.callproc('get_assoc_businesses',[id_driver])
            data = cursor.fetchall()
            cursor.close()
            mysql.connection.commit()
            
            user = {
                'key': _key,
                'conf_code': _conf_code
            }
            lines = []
            if len(data) is not 0:
                user['nickname'] = data[0].get('FirstName')
                
                for row in data:
                    if row.get('HireStatus') != 'blocked':
                        lines.append(
                            {
                                'id': row.get('idBusinessDriver'),
                                'business': row.get('BusName'),
                                'status': row.get('HireStatus')
                            }
                        )
                        
            return render_template("driver_view_deregister.html",
                           title='Deregister',
                           user=user,
                           lines=lines)
            #TODO: grab all info about businesses that have hired this driver, display in form with checkboxes
            #   Display "deregister from dispatcher as a whole" button
            
        
        
    except Exception as e:
        return jsonify({'status':str(e)})
    return 'end' #should never get here


@app.route("/perform_deregister_driver", methods=['GET','POST'])
def perform_deregister_driver():
    try:
        #This check maintains security; valid conf_code is required
        _key = request.form.get('key')
        _conf_code = request.form.get('conf_code')
        
        cursor = mysql.connection.cursor()
        cursor.callproc('check_confirm_code',[_key, _conf_code])
        data = cursor.fetchall()
        cursor.close()
        
        if len(data) is 0:
            mysql.connection.rollback()
            return render_template('message.html',
                           title='Whoops',
                           message='Something went wrong, please try again.')
        elif data[0].get('status') == 'invalid':
            mysql.connection.rollback()
            return render_template('message.html',
                           title='Incorrect Code',
                           message="Incorrect confirmation code.")
        elif data[0].get('status') == 'success':
            mysql.connection.commit()
            id_driver = data[0].get('idDriver')
            
            #consume conf_code
            cursor = mysql.connection.cursor()
            cursor.callproc('delete_confirm_code',[_key])
            data = cursor.fetchall()
            cursor.close()
            mysql.connection.commit()
            
            #build requested mods
            id_to_drop = []
            drop_all = 'all' in request.form
            for v in request.form.getlist('choices'):
                id_to_drop.append(v)
            
            sql_list = ''
            if len(id_to_drop) is not 0:
                sql_list = ','.join(map(str, id_to_drop))
            
            #execute mods
            cursor = mysql.connection.cursor()
            cursor.callproc('delete_driver',[drop_all,id_driver,sql_list])
            data = cursor.fetchall()
            cursor.close()
            mysql.connection.commit()
            
            
            #return  str(sql_list) + "|" + str(drop_all)
            return render_template('message.html',
                           title='Successful Deregistration',
                           message='You have successfuly applied the changes.')
                        

    except Exception as e:
        return jsonify({'status':str(e)})
    #return str(request.form)
    return 'end' #should never get here


#Register Driver with a business    
@app.route("/register_driver/<unique_url>", methods=['GET','POST'])
def register_driver_w_business(unique_url):
    try:
        _phoneNumber = request.get_json().get('phone_number','')
       # _phoneNumber = request.get_json().get('phone_number','')

        #get driver from phone number
        cursor = mysql.connection.cursor()
        cursor.callproc('get_driver_from_phone', _phoneNumber)
        data = cursor.fetchall()
        cursor.close()

        if len(data) is 0:
            mysql.connection.rollback()
            return render_template('message.html', 
                                   title='Whoops',
                                   message='Please register with our service before trying to register with any businesses')
        elif data[0].get('status') == 'success':
            id_driver = data[0].get('idDriver')

        #get business from unique_url
        cursor = mysql.connection.cursor()
        #TODO Not Correct Proc Call
        cursor.callproc('get_business', unique_url)
        data = cursor.fetchall()
        cursor.close()

        if len(data) is 0:
            mysql.connection.rollback()
            return render_template('message.html',
                                    title='Whoops',
                                    message='Something went wrong, please try again.')
        elif data[0].get('status') == 'success':
            id_business = data[0].get('idBusiness')

        cursor = mysql.connection.cursor()
        cursor.callproc('new_business_driver', id_driver, id_business)
        cursor.close()
        mysql.connection.commit()

        return render_template('message.html', 
                                title='Succesful Registration',
                                message='You have succesfuly registered with' + id_business[1])

    except Exception as e:
        return jsonify({'status':str(e)})

    return 'end' #should never get here
