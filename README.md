# email_to_sms_translator
Summary: 
At the job I am currently at, I have the everyday task of receiving emails, translating those emails and then sending those email messages 
to the proper members via SMS. After which I receive members responses and I respond to those client. 
This can get very repitive so I decided to automate first part of my task which is receiving email -> translating -> Sms to the members

Instructions:
If you're not signed in run "gmail_auto_login" for automated sign in. Once you're signed check what new emails are available. Run gmail_read_email.py to query by email address and the application should automatically send those messages to the right members

Technology: 
Gmail API, Twilio API, Translate PyPi, Selenium
Language
Python

Installation
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install twilio
pip install translate
pip install selenium
