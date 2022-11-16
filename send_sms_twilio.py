import os
from twilio.rest import Client
from english_spanish_translator import translation

# client email will be imported from read_emails, then we'll do a check if it in the database
# we'll pull the client values , then access the members that are paired to clients. Take their values and create a "to" global variable
# to will be variable we'll store the variables and send texts to. 

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+15017122661',
                     to='+15558675310'
                 )

print(message.sid)
