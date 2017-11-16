import json, urllib, random, string
from flask import request, jsonify, render_template
from bin import app, mysql, do_sms

@app.route("/ajax_business_get_jobs", methods=['POST'])
def ajax_business_get_jobs():
    bus_id = request.get_json().get('bus_id','')
    types = request.get_json().get('types','')
    
    
    
    
    return render_template('ajax/job_row.html',
                           title='Home')