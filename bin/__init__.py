from flask import Flask
from flask_mysqldb import MySQL

#Flask instance
app = Flask(__name__)

#SMS Flag
do_sms = True
 

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
from bin import driver_management, util

