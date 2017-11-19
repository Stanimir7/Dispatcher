from flask import Flask
from flask_mysqldb import MySQL

# Clover Stuff
expected_client_id = 'AR9BJGD3R4BE2'
client_secret = 'fdcb7b56-7518-0efa-d3f6-179e5fb94a8f'

#Internal status constants
SUCCESSFUL_AUTH = 'successful_clover_auth'

#Internal Current Business ID; should be set on first access request by clover
curr_business_id = ''

#Current hostname. Needed to build clover auth stuff.
hostname = 'http://ec2-52-23-224-226.compute-1.amazonaws.com'

#Endpoint prefix. This is something configured in apache/wsgi; set here in variable for future-proofing
endpoint_prefix = '/dispatcher'

#Flask instance
app = Flask(__name__)


### MySQL ###
mysql = MySQL()
app.config['MYSQL_USER'] = 'dispatcher'
app.config['MYSQL_PASSWORD'] = 'dispatcher'
app.config['MYSQL_DB'] = 'dispatcher'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql.init_app(app)

### Debug ###
@app.route("/")
def hello():
    return "You probably meant to specify an endpoint."

    #SMS Flag
do_sms = False
    #clover auth flag
do_auth = True

if __name__ == "__main__":
    app.run(debug=True)
    
    
### Modules ###

from bin import views, views_ajax, business_job_tasks, business_driver_tasks, business_registration, driver_job_tasks, driver_registration, util, oauth

