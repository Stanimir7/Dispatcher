import json, urllib, random, string
from flask import request, jsonify, render_template
from bin import app, mysql, do_sms

@app.route("/ajax/ajax_business_get_jobs", methods=['POST'])
def ajax_business_get_jobs():
    bus_id = request.get_json().get('bus_id','')
    types = request.get_json().get('types','')
    
    jobs = []
    
    for status in types:
        cursor = mysql.connection.cursor()
        cursor.callproc('get_assoc_job_from_business',[bus_id, status])
        data = cursor.fetchall()
        cursor.close()
        
        if len(data) is not 0:
            jobs.extend(data)
    
    return jsonify(render_template('ajax/job_row.html',
                           jobs=jobs))