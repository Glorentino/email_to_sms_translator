import os
from twilio.rest import Client
from database import client_to_members, members

account_sid = os.environ['TWILIO_ACCOUNT_SID']="ACf722a32f5330ed76c6ce1a3150b2c760" #Enter twilio account sid in str
auth_token = os.environ['TWILIO_AUTH_TOKEN']="d8f02da48f2b4056f8b2f88792850d72" # Enter twilio account auth token in str
client = Client(account_sid, auth_token)
def sms(translatedText, clientEmail):
    for i, v in client_to_members.items():
        if i == clientEmail:
            dest = v 
            for memName, v in members.items():
                if dest == memName:
                    text_to = v
                    message = client.messages \
                                    .create(
                                        body=translatedText,
                                        from_='16293331654',
                                        to=f'+1{text_to}'
                                    )
                    return f"Text from {clientEmail} sent to {memName} via {message.account_sid}"
    if clientEmail not in client_to_members:
        print("Client not in datebase")
        print(members)
        newMember = input("Assign the a member from above: ")
        while newMember not in members:
            newMember = input("Assign the a member from above: ")
        client_to_members[clientEmail] = newMember
        text_to = members[newMember]
        message = client.messages \
                        .create(
                            body=translatedText,
                            from_='+15017122661',
                            to=f'+1{text_to}'
                        )
        return f"Text from {clientEmail} sent to {newMember} via {message.account_sid}"


