from flask import Flask
from flask_mysqldb import MySQL

#Flask instance
app = Flask(__name__)

# Clover Stuff
expected_client_id = 'AR9BJGD3R4BE2'
client_secret = 'fdcb7b56-7518-0efa-d3f6-179e5fb94a8f'

#Internal status constants
SUCCESSFUL_AUTH = 'successful_clover_auth'

#Current hostname. Needed to build clover auth stuff.
hostname = 'http://ec2-52-23-224-226.compute-1.amazonaws.com'

#Endpoint prefix. This is something configured in apache/wsgi; set here in variable for future-proofing
endpoint_prefix = '/dispatcher'


#jinja
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

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
do_sms = True
    #clover auth 
do_auth = True
use_debug_token = False
use_debug_merch = False
debug_token = '9b92a644-ea10-3efb-e37a-108b8178dff9'
debug_merch = '2A8HAXYZ845P4'

if __name__ == "__main__":
    app.run(debug=True)
    
    
### Modules ###

from bin import views, views_ajax, business_job_tasks, business_driver_tasks, business_registration, driver_job_tasks, driver_registration, util, oauth

