from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

# def biggest_bid(bids):
#     biggest_bid = 0
#     for bid in bids:
#         if bid.bid > biggest_bid:
#             biggest_bid = bid.bid
#     return biggest_bid


class ObjectIndexMexin:
    model = None
    template = None  

    def get(self,request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        else:
            obj = self.model.objects.all()        
            return render(request, self.template,{
                "lots" : obj            
            })
