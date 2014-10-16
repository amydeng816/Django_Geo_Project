import urllib2
import json
from geopy import geocoders

def locu_search(query):
    api = '8033868594b602976f33afe0e2d6476a15d29f26'
    uri = 'https://api.locu.com/v1_0/venue/search/?'
    local = query
    locality = local.replace(' ', '+')
    
    new_url = uri + 'api_key=' + api + '&locality=' + locality
    print new_url
    obj = urllib2.urlopen(new_url)
    data = json.load(obj)
    
    #print data
    locations = []
    for o in data['objects']:
        if o["categories"]:
            for i in o["categories"]:
                if i == "restaurant":
                    item_list = [o['name'], o['id']]
                    locations.append(item_list)
                    break
    if not locations:
        return False
    return locations

def locu_details(locu_id):
    url = 'https://api.locu.com/v1_0/venue/'
    api = '8033868594b602976f33afe0e2d6476a15d29f26'
    #id1 = (str(locu_id)).replace(' ', '%20')
    new_url = url + str(locu_id) + '/?api_key=' + api
    print new_url
    obj = urllib2.urlopen(new_url)
    data = json.load(obj)
    details = []
    otherinfo = []
    details.append(data['objects'][0]["lat"])
    details.append(data['objects'][0]["long"])
    otherinfo.append(data['objects'][0]["phone"])
    otherinfo.append(data['objects'][0]["website_url"])
    otherinfo.append(data['objects'][0]["street_address"])
    otherinfo.append(data['objects'][0]["locality"])
    otherinfo.append(data['objects'][0]["region"])
    return details, otherinfo

def foursquare_details(four_id):
    token = '0JYVVX02CNHVNBEDJ0RKGBEFMR3XC0IBNXP0PM5IJD1DKZXT'
    new_url = 'https://api.foursquare.com/v2/venues/' + str(four_id) + '?oauth_token=' + token + '&v=20131016'
    print new_url
    obj = urllib2.urlopen(new_url)
    data = json.load(obj)
    details = []
    otherinfo = []
    details.append([data['response']['venue']['location']['lat']])
    details.append([data['response']['venue']['location']['lng']])
    otherinfo.append(str(data['response']['venue']['url']))
    otherinfo.append(str(data['response']['venue']['location']['formattedAddress'][0]))
    otherinfo.append(str(data['response']['venue']['location']['formattedAddress'][1]))
    otherinfo.append(str(data['response']['venue']['contact']['formattedPhone']))
    return details, otherinfo
    
def foursquare_search(Query):
    token = '0JYVVX02CNHVNBEDJ0RKGBEFMR3XC0IBNXP0PM5IJD1DKZXT'
    place, lat, lng = find_place(Query)
    latlng = 'll=' + str(lat) + '%2C%20' + str(lng)
    url = 'https://api.foursquare.com/v2/venues/search?oauth_token=' + token + '&v=20131016&' + latlng + '&intent=checkin'
    #print 'pppppppppppppppppp'
    print url
    obj = urllib2.urlopen(url)
    data = json.load(obj)
    #print data
    locations = []
    otherinfo = []
    for res in data['response']['venues']:
        lname = res['name']
        lid = str(res['id'])
        urlmenu = 'https://api.foursquare.com/v2/venues/' + lid + '/menu?oauth_token=' + token + '&v=20131016'
        obj1 = urllib2.urlopen(urlmenu)
        data1 = json.load(obj1)
        if data1['response']['menu'] and data1['response']['menu']['menus']['count'] > 0:
            locations.append([res['name'], res['id']])
    return locations

def find_place(query):
    g =  geocoders.GoogleV3()
    place, (lat, lag) = g.geocode(query)
    return place, lat, lag