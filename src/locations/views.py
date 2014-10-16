# Create your views here.
from django.shortcuts import render_to_response, RequestContext
from geolocator.functions import locu_details, foursquare_details
from .models import Location
import sys

def single_location(request, id):
    locuapi = False
    foursquareapi = False
    try:
        location = Location.objects.get(locu_id=id)
        locuapi = True
    except Location.DoesNotExist:
        foursquareapi = True
        locuapi = False
    except Location.MultipleObjectsReturned:
        location = Location.objects.filter(locu_id=id)[0]
        locuapi = True
    except:
        #location = 'Location not exists'
        location = "Unexpected error:", sys.exc_info()[0]
    details = []
    if locuapi:
        #print 'cccccccccccccccccccccccc'
        details = locu_details(id)
    if foursquareapi or not details:
        try:
            location = Location.objects.get(four_id=id)
        except Location.MultipleObjectsReturned:
            location = Location.objects.filter(four_id=id)[0]
        except:
            #location = 'Location not exists'
            location = "Unexpected error:", sys.exc_info()[0]
        details = foursquare_details(id)
        #details = Location.objects.all()
        #print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        print details
    return render_to_response('locations/single.html', locals(), context_instance=RequestContext(request))
