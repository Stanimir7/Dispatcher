import json, urllib
from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_mysqldb import MySQL
import random, string
app = Flask(__name__)

import bin.create_job
import bin.sms.send_sms
#MySQL Connection
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_USER'] = 'dispatcher'
app.config['MYSQL_PASSWORD'] = 'dispatcher'
app.config['MYSQL_DB'] = 'dispatcher'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql.init_app(app)
