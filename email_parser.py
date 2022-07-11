## This is a file used to translate html files. We first parse a doc using BeautifulSoup4 then we replace original text with translation.
from email_fetcher import content_type, language
from importlib.util import module_for_loader
from bs4 import BeautifulSoup
import translators as ts
from asyncore import write


if content_type == "text/html":
    from email_fetcher import email_html # edit to replace this with a "try, except" function at the start.
    soup = BeautifulSoup(email_html, 'html.parser')
    print("translating to", language)
    for i in soup.find_all(text=True):
        try:
            print("translating...")
            i.replace_with(ts.google(i.text, from_language='auto', to_language= language))
        except IndexError:
            pass
    translated_email = soup
    text = soup.text
    print("translated text/html email!")

elif content_type == "text/plain":
    from email_fetcher import email_text # edit out like first in-file use of email_html    
    print("translating to", language)
    text = ts.google(email_text, from_language='auto', to_language= language)
    print("translated text/plain email!")

elif content_type == "image/png":
    text = "My applogies, the email format is not supported, it is most likely an image/png file format that I cannot parse and translate at the moment.\n Thank you for using my service! Have a good rest of the day."
    print("problem, this is a picture file.")

else:
    text = "My applogies, the email format is not supported, my program only support html and text email formats, the email you have sent is neither, and is not an image/png format as well.\n Thank you for using my service! Have a good rest of the day."
    print("problem with content type identification:", content_type)


