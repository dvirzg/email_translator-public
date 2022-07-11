* main.py logs in to the imap server, and continuously checks for new emails, it is the main file from which the program starts and terminates. it calls sends_email.py ;

* email_fetcher.py logs in to the imap server again (needs to be fixed so that is not needed), fetches the latest email, intitializes email details in variable form, 
  determines the target language, deletes the email from inbox, then logs out of the imap server;

* email_parser.py checks which format the recieved email follows (html/text/picture/other), if parses and translates the email;

* send_email.py attaches both text and html part of html emails (most common), then sends the translated email gotten from email_parser.py;

* supported_languages.py contains a dictionary of each supported language and their reference name (German can be refered to in the email as "[german]" or "[de]" independent of capitalization)