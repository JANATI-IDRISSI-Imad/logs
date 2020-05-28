from django.shortcuts import render, HttpResponse, redirect
from .models import User , Server , syslog 
from django.contrib import messages
from scp import SCPClient
import paramiko
from mainapp.views import indextest
from django.contrib.sessions.backends.base import  SessionBase
from django.core import serializers
from sysLog.views import tablesyslog
from datetime import datetime
# Create your views here.





def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client


def register(request):
    if request.method=='POST':
        user = User()
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.password = request.POST['password']
        user.email = request.POST['email']
        user.save()
        return redirect("login")
    else :
        return render(request,"register.html")

def login(request):
    global  user
    user=User()
    if request.method=='POST':
        user.email = request.POST['email']
        user.password = request.POST['password']
        user =  User.objects.get(email=user.email, password=user.password)
        if user is None :
            messages.info(request, 'Error')
            return redirect("login")          
        else :           
            request.session['email'] = user.email
            return redirect(loginserver)            
    else:
        return render(request,"login.html")


def loginserver(request):
    #try: 
        #if user.is_authenticated :

            if request.method=='POST':
                server =Server()
                server.host = request.POST['server']
                server.port = request.POST['port']
                server.user = request.POST['user']
                server.password = request.POST['password']
                src = "C:/log/syslog.1"
                dst = "E:/4eme/imad/django/log/"
                try :                    
                    ssh = createSSHClient(server.host, server.port, server.user, server.password)
                    scp = SCPClient(ssh.get_transport())
                    scp.get(src , dst)
                    
                    user.servers.update()
                    
                    request.session['server'] = server.host
                    
                    #server.logs=Log()
                    if user.servers.count() == 0 :                        
                        user.servers.append(server)
                        
                    else :  
                        print(user.servers.count())                      
                        if user.servers.get(host=request.session['server']) == None :
                            
                            user.servers.append(server)

                    
                    setsyslog(request)

                    return redirect(tablesyslog)
                except Exception as e :
                    messages.info(request,e)
                    return redirect("loginserver")   
            else:
                return render(request,"loginserver.html")

import calendar
def getmount(mountstr):

    j = 0
    for i in calendar.month_abbr:
        if i==mountstr :
            return j
        #print(j,'-',i)
        j+=1
    return j

def setsyslog(request):
    file = open('E:/4eme/imad/django/log/syslog.1', "r")
    lines = file. readlines()
    file.close()
    logs= user.servers.get(host=request.session['server']).syslogs
    testlast=1
    if logs.count()!=0 :
        lastlog=logs[logs.count()-1]
        testlast=0

    #print(logs.last())
    for line in lines :
            tab=line.split()                  
            l = syslog()
            l.local = tab[3]
            date_string=str(getmount(tab[0]))+" "+tab[1]+" "+ tab[2]
            l.date = datetime.strptime(date_string, "%m %d %H:%M:%S") 
            if testlast ==0 :
                if lastlog.date<l.date :
                    #l.date = tab[0]+" "+tab[1]+" "+ tab[2]
                    s=tab[4].split("[")
                    l.service = tab[4]
                    s=""
                    i=0
                    for s1 in tab :
                        if i>=5 :
                            s=s +s1+" "
                        i=i+1
                    l.message = s
                    user.servers.get(host=request.session['server']).syslogs.append(l)
            else :
                #print("imad")
                s=tab[4].split("[")
                l.service = tab[4]
                s=""
                i=0
                for s1 in tab :
                    if i>=5 :
                        s=s +s1+" "
                    i=i+1
                l.message = s
                user.servers.get(host=request.session['server']).syslogs.append(l)
    user.save()
        


def getUser():
    return user