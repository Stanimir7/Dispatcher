from flask import request, redirect, url_for, jsonify, render_template
import requests
import urllib.parse
from bin import app, expected_client_id, client_secret, hostname, endpoint_prefix, SUCCESSFUL_AUTH, do_auth, mysql

#Internal Current Business ID; should be set on first access request by clover
curr_business_id = ''
# Call this to force authenication on the endpoint
def force_auth(short_endpoint):
    global curr_business_id
    if not do_auth:
        curr_business_id = '1'
        return SUCCESSFUL_AUTH
    
    full_endpoint = endpoint_prefix + short_endpoint
    
    supplied_client_id = request.args.get('client_id', default = '')
    supplied_merchant_id = request.args.get('merchant_id', default = '')
    auth_code = request.args.get('code', default = '')
    if (supplied_client_id != expected_client_id or
        supplied_merchant_id == '' or
        auth_code == ''):
        redirect_url = 'https://sandbox.dev.clover.com/oauth/authorize?'
        redirect_params = { 'client_id' : expected_client_id,
            'redirect_uri' : hostname + full_endpoint }
        
        return redirect('{}{}'.format(redirect_url, urllib.parse.urlencode(redirect_params)))
    else:
        url = 'https://sandbox.dev.clover.com/oauth/token'
        info = { 'code' : auth_code, 'merchant_id' : supplied_merchant_id, 'client_id' : supplied_client_id, 'client_secret' : client_secret }
        r = requests.request('GET', url, params = info)
        if r.status_code == '500':
            return jsonify({'status': 'error', 'message': 'Received error from clover: ' + str(r.json())})
        else:
            auth_response = r.json()
            if "access_token" in auth_response:
                #grab business ID from merch id
                cursor = mysql.connection.cursor()
                cursor.callproc('get_business_from_merch_id',[supplied_merchant_id])
                data = cursor.fetchall()
                cursor.close()
                if len(data) is 0:
                    mysql.connection.rollback()
                    return render_template('message.html',
                           title='Whoops',
                           message='Something went wrong, please try again.') 
                elif data[0].get('status') == 'error':
                    mysql.connection.rollback()
                    return render_template('message.html',
                           title='Not Registered',
                           message='This business is not registered with Dispatcher. ')
                mysql.connection.commit()
                curr_business_id = data[0].get('idBusiness')
                return SUCCESSFUL_AUTH
            else:
                # FAILED_AUTH
                return render_template('message.html',
                           title='Authenication Failure',
                           message='The authenication attempt failed.')
            
            
#Called by clover ONLY
@app.route("/oauth_callback", methods=['POST','GET'])
def oauth_callback():

    supplied_client_id = request.args.get('client_id', default = '')
    supplied_merchant_id = request.args.get('merchant_id', default = '')
    auth_code = request.args.get('code', default = '')
   
    # this endpoint should only be called from clover, so don't do redirect if parameters are empty
    # if info is wrong return error
    if supplied_client_id != expected_client_id:
        err_msg = 'Invalid client id supplied: {}'.format(supplied_client_id)
        return jsonify({'status': 'error', 'message': err_msg})
    elif supplied_merchant_id == '':
        return jsonify({'status': 'error', 'message': "Please provide a merchant id."})
    elif auth_code == '':
        return jsonify({'status': 'error', 'message': "Please provide an auth code."})
    else:
        url = 'https://sandbox.dev.clover.com/oauth/token'
        info = { 'code' : auth_code, 'merchant_id' : supplied_merchant_id, 'client_id' : supplied_client_id, 'client_secret' : client_secret }
        r = requests.request('GET', url, params = info)
        if r.status_code == '500':
            return jsonify({'status': 'error', 'message': 'Received error from clover: ' + str(r.json())})
        else:
            # TODO: redirect to home page
            return jsonify({'status': 'success', 'message' : 'Received json data from clover: ' + str(r.json())})


# Testing/debug endpoint
@app.route("/test_authed_callback", methods=['POST', 'GET'])
def test_authed_callback():
    supplied_client_id = request.args.get('client_id', default = '')
    supplied_merchant_id = request.args.get('merchant_id', default = '')
    auth_code = request.args.get('code', default = '')
    if (supplied_client_id != expected_client_id or
        supplied_merchant_id == '' or
        auth_code == ''):
        redirect_url = 'https://sandbox.dev.clover.com/oauth/authorize?'
        redirect_params = { 'client_id' : expected_client_id,
            'redirect_uri' : 'http://ec2-52-23-224-226.compute-1.amazonaws.com/dispatcher/test_authed_callback' }
        
        return redirect('{}{}'.format(redirect_url, urllib.parse.urlencode(redirect_params)))
    else:
        url = 'https://sandbox.dev.clover.com/oauth/token'
        info = { 'code' : auth_code, 'merchant_id' : supplied_merchant_id, 'client_id' : supplied_client_id, 'client_secret' : client_secret }
        r = requests.request('GET', url, params = info)
        if r.status_code == '500':
            return jsonify({'status': 'error', 'message': 'Received error from clover: ' + str(r.json())})
        else:
            # return success status for now, but eventually this will be a redirect for each web page
            return jsonify({'status': 'success', 'response_json': r.json()})


# Example [also testing] force_auth usage
@app.route("/test_force_auth", methods=['POST', 'GET'])
def test_force_auth():
    auth_res = force_auth("/test_force_auth")
    if auth_res == SUCCESSFUL_AUTH:
        return "body of the page" + curr_business_id #Proceed with whatever the endpoint is doing
    else:
        return auth_res #MUST DO THIS; handles redirects, auth failure, etc

    
