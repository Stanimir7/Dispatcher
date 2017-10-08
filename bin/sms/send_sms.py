import os
from twilio.rest import Client

account_sid = "AC07b8ffa96a015ff7f1b16892d7b0650d"
auth_token = "10a3d2daf852e2b5c62c298e6f2854cd"

client = Client(account_sid, auth_token)

my_twilio_number = "+18564463454"
dest_cell_number = "+1"

def send():
	message = client.messages.create(
		to=dest_cell_number,
		from_=my_twilio_number,
		body="Hi group!  Just gotta figure out recieving texts"
	)

