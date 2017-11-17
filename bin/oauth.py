from flask import request, redirect, url_for, jsonify
import requests
from bin import app

@app.route("/oauth_callback", methods=['POST','GET'])
def oauth_callback():
    expected_client_id = 'AR9BJGD3R4BE2'
    client_secret = 'fdcb7b56-7518-0efa-d3f6-179e5fb94a8f'

    supplied_client_id = request.args.get('client_id', default = '')
    supplied_merchant_id = request.args.get('merchant_id', default = '')
    auth_code = request.args.get('code', default = '')
    
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
            # TODO: this will probably need to be a redirect eventually
            return jsonify({'status': 'success', 'message' : 'Received json data from clover: ' + str(r.json())})
