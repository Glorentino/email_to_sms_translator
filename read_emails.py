import os
import sys
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode
from google_auth import gmail_authenticate, search_messages


def get_size_format(b, factor=1024, suffix="B"):

    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b/= factor
    return f"{b:.2f}Y{suffix}"

def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)

def parse_parts(servce, parts, folder_name, message):

    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = part.get("headers")
            if part.get("parts"):

                parse_parts(service, part.get("parts"), folder_name, message)
            if mimeType == "text/plain":

                if data:
                    text = urlsafe_b64decode(data).decode()
                    print(text)
            elif mimeType == "text/html":

                if not filename:
                    filename = "index.html"
                filepath = os.path.join(folder_name, filename)
                print("Saving HTML to", filepath)
                with open(filepath, "wb") as f:
                    f.write(urlsafe_b64decode(data))
            else:

                for part_header in part_headers:
                    part_header_name = part_header.get("name")
                    part_header_value = part_header.get("value")
                    if part_header_name == "Content-Disposition":
                        if "attachment" in part_header_value:

                            print("Saving the file:", filename, "size:", get_size_format(file_size))
                            attachment_id = body.get("attachmentId")
                            attachment = service.users().messages() \
                                        .attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
                            data = attachment.get("data")
                            filepath = os.path.join(folder_name, filename)
                            if data:
                                with open(filepath, "wb") as f:
                                    f.write(urlsafe_b64decode(data))



def read_message(service, message):

    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "email"
    has_subject = False
    if headers:
        
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                
                print("From:", value)
            if name.lower() == "to":
                
                print("To:", value)
            if name.lower() == "subject":
                
                has_subject = True
                
                folder_name = clean(value)
                
                folder_counter = 0
                while os.path.isdir(folder_name):
                    folder_counter += 1
                    
                    if folder_name[-1].isdigit() and folder_name[-2] == "_":
                        folder_name = f"{folder_name[:-2]}_{folder_counter}"
                    elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
                        folder_name = f"{folder_name[:-3]}_{folder_counter}"
                    else:
                        folder_name = f"{folder_name}_{folder_counter}"
                os.mkdir(folder_name)
                print("Subject:", value)
            if name.lower() == "date":
               
                print("Date:", value)
    if not has_subject:

        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
    parse_parts(service, parts, folder_name, message)
    print("="*50)


if __name__ == "__main__":
    service = gmail_authenticate()
    # get emails that match the query you specify from the command lines
    results = search_messages(service, sys.argv[1])
    print(f"Found {len(results)} results.")
    # for each email matched, read it (output plain/text to console & save HTML and attachments)
    for msg in results:
        read_message(service, msg)