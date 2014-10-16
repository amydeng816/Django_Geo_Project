import urllib2
import json
from .apis import *
from geopy import geocoders

def locu_search(query):
    api = '8033868594b602976f33afe0e2d6476a15d29f26'
    uri = 'https://api.locu.com/v1_0/venue/search/?'
    local = query
    locality = local.replace(' ', '+')
    
    new_url = uri + 'api_key=' + api + '&locality=' + locality
    obj = urllib2.urlopen(new_url)
    data = json.load(obj)
    
    #print data
    locations = []
    for abc in data['objects']:
        item_list = [abc['name'], abc['id']]
        locations.append(item_list)
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
    for abc in data['objects']:
        details.append(abc['lat'])
        details.append(abc['long'])
    return details

def foursquare_details(four_id):
    token = '0JYVVX02CNHVNBEDJ0RKGBEFMR3XC0IBNXP0PM5IJD1DKZXT'
    new_url = 'https://api.foursquare.com/v2/venues/' + str(four_id) + '?oauth_token=' + token + '&v=20131016'
    print new_url
    obj = urllib2.urlopen(new_url)
    data = json.load(obj)
    details = []
    details.append([data['response']['venue']['location']['lat']])
    details.append([data['response']['venue']['location']['lng']])
    return details
    
def foursquare_search(Query):
    token = '0JYVVX02CNHVNBEDJ0RKGBEFMR3XC0IBNXP0PM5IJD1DKZXT'
    place, lat, lng = find_place(Query)
    latlng = 'll=' + str(lat) + '%2C%20' + str(lng)
    url = 'https://api.foursquare.com/v2/venues/search?oauth_token=' + token + '&v=20131016&' + latlng + '&intent=checkin'
    #print 'pppppppppppppppppp'
    #print url
    obj = urllib2.urlopen(url)
    data = json.load(obj)
    #print data
    locations = []
    for abc in data['response']['venues']:
        locations.append([abc['name'], abc['id']])
        try:
            print 'phone = ' + abc['contact']['twitter']
        except Exception:
            pass
            
        try:
            print 'city = ' + abc['location']['city']
        except Exception:
            pass
    return locations

def find_place(query):
    g =  geocoders.GoogleV3()
    place, (lat, lag) = g.geocode(query)
    return place, lat, lag