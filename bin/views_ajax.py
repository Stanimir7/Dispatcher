import json, urllib, random, string
from flask import request, jsonify, render_template
from bin import app, mysql, do_sms
import bin.oauth

#######################
######## Business: Jobs #########
#######################
@app.route("/ajax/ajax_business_get_jobs", methods=['POST'])
def ajax_business_get_jobs():
    #auth check
    if bin.oauth.curr_business_id == '': 
        return '<p>Authenication Error. Please refresh the page.</p>'
    
    #bus_id = request.get_json().get('bus_id','')
    bus_id = bin.oauth.curr_business_id
    types = request.get_json().get('types','').split(",")
    
    jobs = []
    
    for status in types:
        cursor = mysql.connection.cursor()
        cursor.callproc('get_assoc_job_from_business',[bus_id, status])
        data = cursor.fetchall()
        cursor.close()
        mysql.connection.commit()
        if len(data) is not 0:
            jobs.extend(data)
    
    if len(jobs) is 0:
        return jsonify("<tr><td>No Jobs</td></tr>")
    
    return jsonify(render_template('ajax_business_job_rows.html',
                           jobs=jobs))

@app.route("/ajax/ajax_business_job_detail_table", methods=['POST'])
def ajax_job_detail_table():
    #auth check
    if bin.oauth.curr_business_id == '': 
        return jsonify({'status':'error','table_html':'<p>Authenication Error. Please refresh the page.</p>'})
    
    id_job = request.get_json().get('id_job','')

    cursor = mysql.connection.cursor()
    cursor.callproc('get_job',[id_job])
    data = cursor.fetchall()
    cursor.close()
    mysql.connection.commit()
    if len(data) is not 0:
        job = data[0]
        cursor = mysql.connection.cursor()
        cursor.callproc('get_assoc_job_driver',[id_job])
        data_driver = cursor.fetchall()
        cursor.close()
        mysql.connection.commit()
        if data_driver[0].get('status') == 'success':
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT DISTINCT * FROM Driver WHERE idDriver = %s", [data_driver[0].get('idDriver')])
            data_driver_detail = cursor.fetchall()
            cursor.close()
            mysql.connection.commit()
            if len(data_driver_detail) is not 0:
                return jsonify({
                    'status':'success',
                    'id_job':id_job,
                    'table_html':
                    render_template('ajax_business_job_detail_table.html',
                           single_job_detail=job,
                           driver_detail=data_driver_detail
                           )
                    })
        return jsonify({
                    'status':'success',
                    'id_job':id_job,
                    'table_html':
                    render_template('ajax_business_job_detail_table.html',
                           single_job_detail=job
                           )
                    })
    else:
        return jsonify({
                    'status':'success',
                    'id_job':id_job,
                    'table_html':
                    render_template('ajax_business_job_detail_table.html'
                           )
                    })

#######################
###### Business: Drivers Info ########
#######################
@app.route("/ajax/ajax_business_get_drivers", methods=['POST'])
def ajax_business_get_drivers():
    #auth check
    if bin.oauth.curr_business_id == '': 
        return '<p>Authenication Error. Please refresh the page.</p>'
    
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

@app.route("/ajax/ajax_business_driver_detail_table", methods=['POST'])
def ajax_driver_detail_table():
    #auth check
    if bin.oauth.curr_business_id == '': 
        return jsonify({'status':'error','table_html':'<p>Authenication Error. Please refresh the page.</p>'})
    
    #id_bus = request.get_json().get('id_bus','')
    id_bus = bin.oauth.curr_business_id
    id_driver = request.get_json().get('id_driver','')

    cursor = mysql.connection.cursor()
    cursor.callproc('get_business_driver',[id_bus,id_driver])
    data = cursor.fetchall()
    cursor.close()
    mysql.connection.commit()
    
    
    driver = {}
    jobs = {}
    
    if len(data) is not 0:
        driver = data[0]
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT DISTINCT j.* FROM JobDriver d JOIN Job j ON (j.idJob = d.fk_idJob) WHERE fk_idDriver = %s", [id_driver])
        data = cursor.fetchall()
        cursor.close()
        mysql.connection.commit()
        if len(data) is not 0:
            jobs = data
        
    
    
    return jsonify({
                    'status':'success',
                    'id_driver':id_driver,
                    'table_html':
                    render_template('ajax_business_driver_detail_table.html',
                           single_driver_detail=driver,
                           jobs=jobs)
                    })
