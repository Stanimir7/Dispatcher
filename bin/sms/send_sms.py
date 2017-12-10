import os
from twilio.rest import Client

account_sid = "AC07b8ffa96a015ff7f1b16892d7b0650d"
auth_token = "10a3d2daf852e2b5c62c298e6f2854cd"

client = Client(account_sid, auth_token)

my_twilio_number = "+18564463454"
dest_cell_number = "+1"

#Send a sms through Twilio with a specified message
def send(_num, _body):
	message = client.messages.create(
		to = _num,
		from_ = my_twilio_number,
		body = _body
	)

