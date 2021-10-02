import requests
from django.shortcuts import render
import json
url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "83b1fcb3b3msh02ed9f175e3c4c6p19417ajsn2effd453278d"
    }

response = requests.request("GET", url, headers=headers).json()


def home(request):
    noofresults = int(response['results'])
    mylist = []
    for x in range(0,noofresults):

        mylist.append(response['response'][x]['country'])
    if request.method=="POST":
       selectedcountry=request.POST['selectedcountry']
       noofresults = int(response['results'])
       for x in range (0,noofresults):
           if selectedcountry==response['response'][x]['country']:
               new=response['response'][x]['cases']['new']
               active=response['response'][x]['cases']['active']
               critical=response['response'][x]['cases']['critical']
               recovered=response['response'][x]['cases']['recovered']
               total=response['response'][x]['cases']['total']
               deaths=int(total)-int(active)-int(recovered)
       context={'selectedcountry':selectedcountry,'mylist':mylist,'new':new,'active':active,'critical':critical,'recovered':recovered,'total':total,'deaths':deaths}
       return render(request, 'index.html', context)
    noofresults = int(response['results'])
    mylist=[]
    for x in range(0,noofresults):
        mylist.append(response['response'][x]['country'])
    context={'mylist':mylist}
    return render(request,'index.html',context)
