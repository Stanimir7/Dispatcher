import json, urllib, random, string
from flask import request, jsonify, render_template
from bin import app, mysql, do_sms


@app.route("/business_jobs", methods=['GET'])
def business_jobs():
    
    return render_template('business_jobs.html',
                           title='Home',
                           idBusiness='1' #TODO dynamically put correct ID here
                           )

@app.route("/business_drivers", methods=['GET'])
def business_drivers():
    
    return render_template('business_drivers.html',
                           title='Home',
                           idBusiness='1' #TODO dynamically put correct ID here
                           )




@app.route("/business_new", methods=['GET'])
def business_new():
    
    return render_template('business_new.html',
                           title='Merchant Registration')
