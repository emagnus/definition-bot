from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import NavigableString
from datetime import datetime
import time
import urllib2
import unicodedata

def fetch(url):
    opener = urllib2.build_opener()
    opener.addheaders = [("User-agent", "defino")]
    response = opener.open(url)
    return response.read()

def udquery(query):
    """ Prepare and query urban dictionary
    """
    query = "+".join(query)
    url = "http://www.urbandictionary.com/define.php/?term="+query
    soup = BeautifulSoup(fetch(url))    
    try:
        html = extract_text(soup.find("div",{"class":"definition"}).contents).replace("\r","")
        text = BeautifulStoneSoup(html,convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents[0]
        definition = unicode(text).decode("utf-8").encode("utf-8")
    except:
        definition = "Ingen definisjon."
    return definition

def extract_text(contents):
    if type(contents).__name__ == 'list':
        s = ""
        for c in contents:
            if type(c) != NavigableString:
                c = extract_text(c.contents)
            s += unicode(c)
        return s
    if type(contents) == NavigableString:
        return contents
    

        
