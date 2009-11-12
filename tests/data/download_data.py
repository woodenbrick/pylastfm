import urllib
params = {"api_key" : "2d21a4ab6f049a413eb27dbf9af10579", "user" : "woodenbrick"}
root_url = "http://ws.audioscrobbler.com/2.0/?"
look_for = '<li><a href="/api/show/?service='
request = urllib.urlopen("http://www.last.fm/api/intro")
for line in request.readlines():
    if line.strip().startswith(look_for):
        name_rindex = line.find("</a>")
        url_rindex = line.find('">')
        params['method'] = line[url_rindex+2: name_rindex]
        encoded_values = urllib.urlencode(params)
        print("Getting", params['method'])
        urllib.urlretrieve(root_url + encoded_values, params['method'])
        
        


