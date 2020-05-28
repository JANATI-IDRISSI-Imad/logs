from django.shortcuts import render

# Create your views here.


def indextest(request):
            
    #try: 
        #if user.is_authenticated :
            return render(request,"indextest.html")
        #else :
            #return redirect("login")
    #except :
        #return redirect("login")
