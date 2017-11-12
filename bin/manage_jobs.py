import json, urllib, random, string
from flask import request, jsonify, render_template
from bin import app, mysql



@app.route("/cancel_job", methods=['POST'])
def cancel_job():
  
   cursor = mysql.connection.cursor()
   #Will need to access database to remove job from list
   
   data = cursor.fetchall()
   cursor.close()

@app.route("/completed_job", methods=['POST'])
def completed_job():

  cursor = mysql.connection.cursor()
  #Will need to access database to add job to complete list(or change Status, which ever way we handle)
  
  data = cursor.fetchall()
  cursor.close()
  
