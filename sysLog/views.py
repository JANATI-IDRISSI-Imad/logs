from django.shortcuts import render
from authentication.models import User
# Create your views here.

def tablesyslog(request):
    #try: 
        #if user.is_authenticated :
            user=User.objects.get(email=request.session['email'])
            logs=user.servers.get(host=request.session['server']).syslogs
            print(logs.count())
            return render(request,"tablesyslog.html",{'logs':logs})
        #else :
            #return redirect("login")
    #except :
        #return redirect("login")
        
#5666