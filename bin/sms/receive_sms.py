import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods=['Get', 'Post'])

def sms_reply():
	resp = MessagingResponse()

	resp.message("Testing 1,2,3");

	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)
