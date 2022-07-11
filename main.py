import imaplib
import time

# account credentials
username = "email@imap.com"
password = "**************"
imap_server = "xxx" # find imap server address: https://www.systoolsgroup.com/imap/

# create an IMAP4 class with SSL 
imap = imaplib.IMAP4_SSL(imap_server)
# authenticate
imap.login(username, password)

while True:
    status, messages = imap.select("INBOX")
    messages = int(messages[0])
    
    if messages > 0:
        print("email detected! initiating translator...")
        try:
            exec(open('sends_email.py').read())
        except:
            print("problem identified, latest email will be skipped.")
    else:
        print("no emails detected, come back in 60 secconds.")
        time.sleep(60)

imap.close()
imap.logout()