import smtplib, ssl
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from bs4 import BeautifulSoup

from email_fetcher import username, password, sender, subject
from email_parser import translated_email, text

# if email has attachments, "attachment" in content_disposition <- True; 

# credentials
# sender's email
FROM = username
# receiver's email
TO   = sender


# initializes the message
msg = MIMEMultipart("alternative")
# sets the sender's email
msg["From"] = FROM
# sets the receiver's email
msg["To"] = TO
# sets the subject
msg["Subject"] = "Translated: " + subject


text_part = MIMEText(text, "plain")
html_part = MIMEText(translated_email, "html")
# attaches the email body to the mail message
# attaches the plain text version first
msg.attach(text_part)
msg.attach(html_part)
# msg.as_string() #to print the sent email


def send_mail(email, password, FROM, TO, msg):
    # initializes the SMTP server
    server = smtplib.SMTP("smtp-mail.outlook.com", 587)
    # connects to the SMTP server as TLS mode (secure) and send EHLO
    server.starttls()
    # logins to the account using the credentials
    server.login(email, password)
    # sends the email
    server.sendmail(FROM, TO, msg.as_string()) # how does this react with multiple sent-to email? is this formated as a list?
    # terminates the SMTP session
    server.quit()

# sends the mail
send_mail(username, password, FROM, TO, msg)
print("sending email...")
print("success!\n")

# only works on latin letters?
# attachments?