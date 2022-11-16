import os

from base64 import urlsafe_b64encode

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

from google_auth import my_email, gmail_authenticate


def add_attachment(message, filename):
    content_type, encoding = guess_mime_type(filename)
    
    if content_type is None or encoding is not None:
        content_type = 'application/octect-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(filename, 'rb')
        msg = MIMEText(fp.read().decode(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(filename, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(filename, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(filename, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(filename)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

def build_message(destination, obj, body, attachement=[]):
    if not attachement:
        message = MIMEText(body)
        message['to'] = destination
        message['from'] = my_email
        message['subject'] = obj
    else:
        message = MIMEMultipart()
        message['to'] = destination
        message['from'] = my_email
        message['subject'] = obj
        message.attach(MIMEText(body))
        for filename in attachement:
            add_attachment(message, filename)
    
    return {'raw':urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, destination, obj, body, attachments=[]):
    return service.users().message().send(
        userId = "me",
        body=build_message(destination, obj, body, attachments)
    ).execute()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Email Sender using Gmail API")
    parser.add_argument('destination', type=str, help='The destination email address')
    parser.add_argument('subject', type=str, help='The subject of the email')
    parser.add_argument('body', type=str, help='The body of the email')
    parser.add_argument('-f', '--files', type=str, help='email attachments', nargs='+')

    args = parser.parse_args()
    service = gmail_authenticate()
    send_message(service, args.destination, args.subject, args.body, args.files)
