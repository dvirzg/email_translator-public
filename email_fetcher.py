import imaplib, getpass, re
import email
from email.header import decode_header
import os 
from supported_languages import lang_dict

# account credentials
username = "email@imap.com"
password = "**************"
# email provider's IMAP server
imap_server = "xxx" # find imap server address: https://www.systoolsgroup.com/imap/

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


# create an IMAP4 class with SSL 
imap = imaplib.IMAP4_SSL(imap_server)
# authenticate
imap.login(username, password)


# if everything goes right, the above logged us in. the following is used to retreive messages
status, messages = imap.select("INBOX")

# N <- number of top emails to fetch
N = 1
# total number of emails
messages = int(messages[0])

for i in range(messages, messages-N, -1):
    # fetch the email message by ID
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # parse a bytes email into a message object
            msg = email.message_from_bytes(response[1])
            # decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)
            # decode email sender
            From, encoding = decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                From = From.decode(encoding)
            print("Subject:", subject)
            print("From:", From)
            # if the email message is multipart
            if msg.is_multipart():
                # iterate over email parts
                for part in msg.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # get the email body
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        # content type is text/html and there is not attachment, passes this info further                        
                        # print text/plain emails and skip attachments
                        print(body)
                    elif "attachment" in content_disposition:
                        # download attachment
                        filename = part.get_filename()
                        if filename:
                            folder_name = clean(subject)
                            if not os.path.isdir(folder_name):
                                # make a folder for this email (named after the subject)
                                os.mkdir(folder_name)
                            filepath = os.path.join(folder_name, filename)
                            # download attachment and save it
                            open(filepath, "wb").write(part.get_payload(decode=True))
            else:
                # extract content type of email
                content_type = msg.get_content_type()
                # get the email body
                body = msg.get_payload(decode=True).decode()
                if content_type == "text/plain":
                    email_text = body
            if content_type == "text/html":
                # if it's HTML, create a new HTML file and open it in browser
                folder_name = clean(subject)
                if not os.path.isdir(folder_name):
                    # make a folder for this email (named after the subject)
                    os.mkdir(folder_name)
                filename = "untranslated_email.html"
                filepath = os.path.join(folder_name, filename)
                # write the file
                open(filepath, "w").write(body)
                email_html = open(filepath, 'r')
                # open in the default browser
                #webbrowser.open(filepath)
            print("="*100)
# close the connection and logout
sender = From.split("<")[1].lstrip().split('>')[0] 
print("Fetched email!")

status, messages = imap.search(None, "SEEN")
# convert messages to a list of email IDs
messages = messages[0].split(b' ')


for mail in messages:
    _, msg = imap.fetch(mail, "(RFC822)")
    # can delete the for loop for performance if there's a long list of emails
    # because it is only for printing the SUBJECT of target email to delete
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            # decodes the email subject
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                # if it's a bytes type, decodes to str
                subject = subject.decode()
            print("Deleting", subject)
    # marks the mail as deleted
    imap.store(mail, "+FLAGS", "\\Deleted")
imap.expunge() # deletes last seen email


# determines which language to translate to
for lang in lang_dict:
    if lang in subject.lower() or "[" + lang_dict[lang] + "]" in subject.lower():
        language = lang_dict[lang]
        break
    else:
        language = "en"


imap.close()
imap.logout()