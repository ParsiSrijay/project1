
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView
# Create your views here.
import pickle
from sklearn.externals import joblib
from sklearn.preprocessing import MinMaxScaler
import pickle
from sklearn.externals import joblib
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

from .models import shg,installments,LoanRegister
def signup(request):
        if request.method == 'POST':
            name=request.POST['name']
            act=request.POST['act']
            amount=int(request.POST['amt'])
            amt=amount*100000
            woman=request.POST['wb']
            location=request.POST['location']
            tp=request.POST['tp']
            rate=request.POST['rate']
            reg=request.POST['reg']
            pd=request.POST['pd']
            ycj=request.POST['ycj']
            if name=="" or act=="" or amount==0 or woman=="" or location=="" or tp=="" or pd=="" or ycj=="":
                return render(request,'a/themexriver.com/tfhtml/finance-top/form.html',{'content':"Enter all The required fields"})
            action=act
            if pd=='Yes' or pd=='yes' or pd=='y':
                pd=1
            else:
                pd=0
            if act=='Tailoring':
                act=1
            elif act=='Handicraft':
                act=2
            elif act=='Handloom':
                act=3
            elif act=='Agriculture':
                act=4
            elif act=='Diary Activities':
                act=5
            elif act == 'Food Processing':
                act = 6
            else:
                act=7
                action="Fishing"
            print(amt,amount)
            model = joblib.load('C:/Users/P SRIJAY/Desktop/sih/imo1.pkl')
            x=[int(amount),int(woman),int(ycj),int(tp),act,pd]
            x=np.array(x)
            x=x.reshape(1,-1)
            y_test=model.predict(x)
            if y_test[0]==1:
                s=shg(Name=name,Activity=action,Amount=amt,Woman_beneficiaries=woman,Location=location,TimePeriod=tp,Rate=rate,Registration_id_imo=reg)
                s.save()
                lr=LoanRegister(Name=name,OpeningBalance=amt,LoanRepayment=0,Interest=0,ClosingBalance=amt)
                lr.save()
                return render(request,'a/themexriver.com/tfhtml/finance-top/form.html',{'content':"Successfully Loan Approved"})
            else:
                return render(request,'a/themexriver.com/tfhtml/finance-top/form.html',{'content': "Loan Rejected!!!"})
        else:
            return render(request,'a/themexriver.com/tfhtml/finance-top/form.html')
def display(request):
    if request.method=='POST':
        reg=request.POST['reg']
        list_shg=shg.objects.values('Name','Amount','Activity').filter(Registration_id_imo=reg)
        return render(request,"form.html",{'shg':list_shg})
    else:
        return render(request,"a.html")
def payinstallments(request):
    if request.method=='POST':
        id=request.POST['id']
        name=request.POST['name']
        inst=request.POST['installments']
        reg=request.POST['reg']
        s=shg.objects.get(Name=name,Registration_id_imo=reg)
        openbal=s.Amount
        loaninst=inst
        rate=s.Rate/12
        time=s.TimePeriod
        interest= (openbal*rate*time)/100
        closebal=openbal-int(loaninst)+interest
        s.Amount=closebal
        s.save()
        lr=LoanRegister(Name=name,OpeningBalance=openbal,LoanRepayment=inst,Interest=interest,ClosingBalance=closebal)
        lr.save()
        return redirect('http://127.0.0.1:8000/add/display')
    else:
        return render(request,'index.html')

def dispLR(request):
    name_list = LoanRegister.objects.raw('SELECT DISTINCT Name,id from addshg_loanregister')
    l = []
    for i in name_list:
        if i.Name not in l:
            l.append(i.Name)
    if request.method=="POST":
        name=request.POST['name']
        lr=LoanRegister.objects.all().filter(Name=name)
        return render(request,"form.html",{"shg":lr,"name_list":l})
    else:
        return render(request,"form.html",{"name_list":l})
