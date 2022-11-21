import os
import sys

from base64 import urlsafe_b64decode
from gmail.google_auth import gmail_authenticate, search_messages
from english_to_spanish.english_spanish_translator import translator
from twilio_sms.send_sms_twilio import sms

txtList = []
englishText = ""

def parse_parts(service, parts, message):

    if parts:
        for part in parts:
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            
            if part.get("parts"):

                parse_parts(service, part.get("parts"), message)
            if mimeType == "text/plain":

                if data:
                    text = urlsafe_b64decode(data).decode()
                    print(text)
    txtList.append(text.split())

def mark_as_read(service, query):
    messages_to_mark = search_messages(service, query)
    print(f"Matched emails: {len(messages_to_mark)}")
    return service.users().messages().batchModify(
        userId='me',
        body={
            'ids': [ msg['id'] for msg in messages_to_mark],
            'removeLabelIds': ['UNREAD']
        }
    ).execute()

def read_message(service, message):
    global spanTxt, englishText

    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")

    if headers:
        
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':

                print("From:", value)

            if name.lower() == "subject":

                print("Subject:", value)
            if name.lower() == "date":
               
                print("Date:", value)
            if name.lower() == "body":
                print("body", value)
            print()

    parse_parts(service, parts, message)
    

    text1 = ""
    for ch in txtList[0]:
        text1 += ch + " "
    englishText = text1
    print("="*50)


service = gmail_authenticate()
query = input("Enter an email address to query: ")
while "@" not in query:
    query = input("Enter an email address to query: ")
results = search_messages(service, query)
#results = 
print(f"Found {len(results)} results.")
for msg in results:
    mark_as_read(service, query)
    read_message(service, msg)
    break
if len(results) > 0:
    print(query, "'s Most Recent Msg:", englishText)
    spanTxt = translator(englishText)
    print("Translated msg", spanTxt)
    print(sms(spanTxt, query))
else:
    print("Email Address not found.")