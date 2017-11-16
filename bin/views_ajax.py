import json, urllib, random, string
from flask import request, jsonify, render_template
from bin import app, mysql, do_sms

@app.route("/ajax/ajax_business_get_jobs", methods=['POST'])
def ajax_business_get_jobs():
    bus_id = request.get_json().get('bus_id','')
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
        return jsonify("<tr><td>No Closed Jobs</td></tr>")
    
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