
## PROJECT DESCRIPTION
Program that monitors an email, parses and translates every incoming email in text/HTML format, then automatically sends back the translated email to the original sender. Default translation is to English, can be specified differently by adding "[language_name]" in the email subject.

Used Python's "email" package to fetch emails, "BeautifulSoup4" to parse HTML documents, and Google's translation API to translate string sentences. 
-----------------------------------------------------------------------------------------------------------------------------

## FILE DESCRIPTION
these are the files used and their function:

* main.py logs in to imap server, continuously checks for new emails, it is the main file from which the program starts and terminates. 
  it calls sends_email.py;
* email_fetcher.py logs in to imap server again, fetches latest email, intitializes details in variable form,  determines target language,  
  deletes the email from inbox, logs out of imap server;
* email_parser.py checks which format the recieved email follows (html/text/picture/other), parses and translates the email;
* send_email.py attaches both text and html part of html emails (most common), sends the translated email imported from email_parser.py;
* supported_languages.py contains a dictionary of each supported language and their reference name 
  (German can be refered to in the email as "[german]" or "[de]" independent of capitalization)
