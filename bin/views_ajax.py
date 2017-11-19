import json, urllib, random, string
from flask import request, jsonify, render_template
from bin import app, mysql, do_sms
import bin.oauth

#######################
######## Jobs #########
#######################
@app.route("/ajax/ajax_business_get_jobs", methods=['POST'])
def ajax_business_get_jobs():
    #auth check
    if bin.oauth.curr_business_id == '': 
        return jsonify({'status':'error','message':'Not authenticated'})
    
    #bus_id = request.get_json().get('bus_id','')
    bus_id = bin.oauth.curr_business_id
    types = request.get_json().get('types','').split(",")
    
    jobs = []
    
    for status in types:
        cursor = mysql.connection.cursor()
        cursor.callproc('get_assoc_job_from_business',[bus_id, status])
        data = cursor.fetchall()
        cursor.close()
        
        if len(data) is not 0:
            jobs.extend(data)
    
    if len(jobs) is 0:
        return jsonify("<tr><td>No Jobs</td></tr>")
    
    return jsonify(render_template('ajax_business_job_rows.html',
                           jobs=jobs))

@app.route("/ajax/ajax_job_detail_table", methods=['POST'])
def ajax_job_detail_table():
    id_job = request.get_json().get('id_job','')

    cursor = mysql.connection.cursor()
    cursor.callproc('get_job',[id_job])
    data = cursor.fetchall()
    cursor.close()
        
    if len(data) is not 0:
        job = data[0]
    
    return jsonify({'id_job':id_job,
                    'table_html':
                    render_template('ajax_job_detail_table.html',
                           single_job_detail=job)
                    })

#######################
###### Drivers ########
#######################
@app.route("/ajax/ajax_business_get_drivers", methods=['POST'])
def ajax_business_get_drivers():
    #auth check
    if bin.oauth.curr_business_id == '': 
        return jsonify({'status':'error','message':'Not authenticated'})
    
    #id_bus = request.get_json().get('id_bus','')
    id_bus = bin.oauth.curr_business_id
    types = request.get_json().get('types','').split(",")
    
    drivers = []
    
    for status in types:
        cursor = mysql.connection.cursor()
        cursor.callproc('get_assoc_drivers_with_status',[id_bus, status])
        data = cursor.fetchall()
        cursor.close()
        
        if len(data) is not 0:
            drivers.extend(data)
    
    if len(drivers) is 0:
        return jsonify("<tr><td>No Drivers</td></tr>")
    
    return jsonify(render_template('ajax_business_driver_rows.html',
                           drivers=drivers))

@app.route("/ajax/ajax_driver_detail_table", methods=['POST'])
def ajax_driver_detail_table():
    #auth check
    if bin.oauth.curr_business_id == '': 
        return jsonify({'status':'error','message':'Not authenticated'})
    
    #id_bus = request.get_json().get('id_bus','')
    id_bus = bin.oauth.curr_business_id
    id_driver = request.get_json().get('id_driver','')

    cursor = mysql.connection.cursor()
    cursor.callproc('get_business_driver',[id_bus,id_driver])
    data = cursor.fetchall()
    cursor.close()
        
    if len(data) is not 0:
        driver = data[0]
    
    return jsonify({'id_driver':id_driver,
                    'table_html':
                    render_template('ajax_driver_detail_table.html',
                           single_driver_detail=driver)
                    })
