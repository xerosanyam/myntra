import urllib2
import json
import sys
import random
from datetime import datetime
import getuserdata


def getData(url):
    value = []
    data = []
    ans = []
    response = urllib2.urlopen(url)
    info = json.load(response)
    gender=info["gender"]
    if gender=="male":
     gender="Men"
    else:
     gender="women"
    i = 0
    while i < len(info["likes"]["data"]):
        data.insert(i, info["likes"]["data"][i]["name"].replace(" ", "-"))
        i = i + 1
    #print data
    i = 0
    while i < 3:
        k = random.randrange(0, len(data) - 1)
        if k not in value:
            image_url, temp_url = check(data, k, value,gender)
            if image_url != 0 and temp_url != 0:
            # print "\n\n hello world \n"
                print "welcome"
                myntra_url = "www.myntra.com/" + temp_url
                ans.append((image_url,myntra_url))
                i = i + 1
                value.insert(i, k)
    print "\n\n\n\n"
    print ans, len(ans)
    return ans



def check(data, k, value,gender):
    base = "http://developer.myntra.com/search/data/"
    url = base + data[k] +gender
    response = urllib2.urlopen(url)
    json_data = json.load(response)
    print "hello"
    if (len(json_data["data"]["results"]["products"]) != 0):
        #print "\n printing \n"
        #print data[k]
        #print json_data["data"]["results"]["products"][0]["search_image"]
        #print json_data["data"]["results"]["products"][0]["dre_landing_page_url"]
        # print "\ni dont know\n"
        return json_data["data"]["results"]["products"][0]["search_image"], json_data["data"]["results"]["products"][0]["dre_landing_page_url"]

    return 0,0
    # else:
    #     k = random.randrange(0, len(data) - 1)
    #     if k not in value:
    #         check(data, k, value)
    #     else:
    #         k = random.randrange(0, len(data) - 1)
    #         check(data, k, value)


def getUrl(mobile):
    token, id = getuserdata.userdata(mobile)
    print token, id
    base = "https://graph.facebook.com/"
    mid = "?fields=id,name,picture,likes,gender&access_token="
    url = base + str(id) + mid + token
    print url
    getData(url)

getUrl(8439257665)
