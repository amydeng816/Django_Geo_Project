from django.shortcuts import render_to_response, RequestContext
from locations.models import Location
from .functions import locu_search, foursquare_search
def home(request):
    if request.method == 'POST':
        print request.POST
        Query = request.POST['search']
        locations = locu_search(Query)
        if not locations:
            locations = foursquare_search(Query)
            for loc in locations:
                name1, four_id1 = loc[0], loc[1]
                new_location, created = Location.objects.get_or_create(name=name1, four_id=four_id1)
                if created:
                    print "Created new id for %s with id of %s" %(name1, four_id1)
            print locations
        else:
            for loc in locations:
                name1, locu_id1 = loc[0], loc[1]
                new_location, created = Location.objects.get_or_create(name=name1, locu_id=locu_id1)
                if created:
                    print "Created new id for %s with id of %s" %(name1, locu_id1)
            print locations
    return render_to_response('home.html', locals(), context_instance=RequestContext(request))