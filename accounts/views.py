from django.shortcuts import render
from .models import ledger
# Create your views here.
def first(request):
    if(request.method=="POST"):
        account_name=request.POST['account']
        transctionType=request.POST['TransctionType']
        particulars=request.POST['particulars']
        amount=request.POST['amount']
        l = ledger(AccountName=account_name,TransctionType=transctionType,Particulars=particulars,Amount=amount)
        l.save()
        m=[]
        l=ledger.objects.values('Date','TransctionType','Particulars','Amount').order_by('AccountName')
        return render(request,'dispLedger.html',{'led':l})
    return render(request,'ledger.html')


