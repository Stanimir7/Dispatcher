import json, urllib, random, string
from flask import request, jsonify, render_template
from bin import app, mysql, do_sms


@app.route("/business_jobs", methods=['GET'])
def business_home():
    
    return render_template('business_jobs.html',
                           title='Home')

@app.route("/business_new", methods=['GET'])
def business_new():
    
    return render_template('business_new.html',
                           title='Merchant Registration')

@app.route("/view_job_detail", methods=['GET'])
def view_job_detail():
    
    return render_template('job_detail.html',
                           title='Job Detail')