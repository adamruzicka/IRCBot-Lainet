import urllib

def tiny_url(url):

    if url[0:7] == "http://" :
        apiurl = "http://tinyurl.com/api-create.php?url="
    if url[0:8] == "http://" :
        apiurl = "https://tinyurl.com/api-create.php?url="
    else:
        apiurl = "http://tinyurl.com/api-create.php?url=http://"
    tinyurl = urllib.urlopen(apiurl + url).read()
    return tinyurl