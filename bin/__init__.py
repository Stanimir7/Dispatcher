from flask import Flask
from flask_mysqldb import MySQL

#Flask instance
app = Flask(__name__)

#SMS Flag
do_sms = False

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

if __name__ == "__main__":
    app.run(debug=True)
    
    
### Modules ###

from bin import views, views_ajax, business_job_tasks, business_driver_tasks, business_registration, driver_job_tasks, driver_registration, util, oauth

