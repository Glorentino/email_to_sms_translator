from google_auth import gmail_authenticate, search_messages

def delete_messages(service, query):
    messages_to_delete = search_messages(service, query)
    return service.users().messages().batchDelete(
        userId='me',
        body={
            'ids':[ msg['id'] for msg in messages_to_delete]
        }
    ).execute()

# delete_messages(service, "Google Alerts") deletes all messages

if __name__ == "__main__":
    import sys
    service = gmail_authenticate()
    delete_messages(service, sys.argv[1])