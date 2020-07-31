from django.shortcuts import render
from .models import ledger,Account
from django.db.models import Avg, Count, Min, Sum
# Create your views here.
def first(request):
    if(request.method=="POST"):
        account_name=request.POST['account']
        transctionType=request.POST['TransctionType']
        particulars=request.POST['particulars']
        amount=request.POST['amount']
        if account_name=="" or particulars=="" or amount==0:
            return render(request,'ledger.html',{"failure":"All the fields need to be entered"})
        l = ledger(AccountName=account_name,TransctionType=transctionType,Particulars=particulars,Amount=amount)
        l.save()
        if transctionType=="Debit":
            l1=ledger(AccountName=particulars,TransctionType="Credit",Particulars=account_name,Amount=amount)
            l1.save()
        else:
            l1 = ledger(AccountName=particulars, TransctionType="Debit", Particulars=account_name, Amount=amount)
            l1.save()
        return render(request,'ledger.html',{"success":"Account Statement Added"})
    return render(request,'ledger.html')

def disp(request):
    list_accounts = ledger.objects.raw('SELECT DISTINCT AccountName,id from accounts_ledger')
    l=[]
    for i in list_accounts:
        if i.AccountName not in l:
            l.append(i.AccountName)
    if(request.method=="POST"):
        AccountName=request.POST['AccountName']
        Account = ledger.objects.all().filter(AccountName=AccountName)
        bal_debit = ledger.objects.filter(AccountName=AccountName,TransctionType="Debit").aggregate(debit=Sum('Amount'))
        bal_credit = ledger.objects.filter(AccountName=AccountName,TransctionType="Credit").aggregate(credit=Sum('Amount'))
        d=0
        c=0
        print(bal_debit)
        debit=bal_debit['debit']
        credit=bal_credit['credit']
        if credit==None:
            credit=0
        if debit==None:
            debit=0
        total = max(debit, credit)
        if debit>credit:
            d=debit-credit
            return render(request, 'dispLedger.html',
                          {'account': Account, 'list': l, 'debit': d,'total':total})
        else:
            c=credit-debit
            return render(request,'dispLedger.html',{'account':Account,'list':l,'credit':c,'total':total})
    else:
        return render(request,'dispLedger.html',{'list':l})


def allAcc(request):
    if request.method=="POST":
        field=request.POST['field']
        RandP=request.POST['RandP']
        IandE=request.POST['IandE']
        balsheet=request.POST['balsheet']
        amount=request.POST['amount']
        acc = Account(Field=field,RandP=RandP,IandE=IandE,BalSheet=balsheet,Amount=amount)
        acc.save()
        return render(request,"generic.html")
    return render(request,"generic.html")

def RandPDisplay(request):
    rec=Account.objects.raw('SELECT Field,id from accounts_account WHERE RandP=%s',['Receipts'])
    pay=Account.objects.raw('SELECT Field,id from accounts_account WHERE RandP=%s',['Payments'])
    l1=[]
    l2=[]
    for i in rec:
        if i.Field not in l1:
            l1.append(i.Field)
    for j in pay:
        if j.Field not in l2:
            l2.append(j.Field)
    s=[]
    t=[]
    for i in range(len(l1)):
        s.append(0)
    for j in range(len(l2)):
        t.append(0)
    for i in range(len(l1)):
        s[i]=Account.objects.filter(RandP="Receipts",Field=l1[i]).aggregate(a=Sum("Amount"))
    for i in range(len(l2)):
        t[i]=Account.objects.filter(RandP="Payments",Field=l2[i]).aggregate(b=Sum("Amount"))
    rec_total=Account.objects.filter(RandP="Receipts").aggregate(rec_sum=Sum("Amount"))
    pay_total=Account.objects.filter(RandP="Payments").aggregate(pay_sum=Sum("Amount"))
    l3=[]
    for i in range(max(len(l1),len(l2))):
        dict={}
        if i<len(l1):
            dict['rec_field']=l1[i]
            dict['rec_amt']=s[i]['a']
        if i<len(l2):
            dict['pay_field']=l2[i]
            dict['pay_amt']=t[i]['b']
        l3.append(dict)
    if rec_total['rec_sum']>pay_total['pay_sum']:
        ex1=rec_total['rec_sum']-pay_total['pay_sum']
        print(ex1)
        return render(request,"RandPdisp.html",{"rp":l3,"rec_total":rec_total,"ex1":ex1})
    else:
        ex2=pay_total['pay_sum']-rec_total['rec_sum']
        return render(request, "RandPdisp.html",
                          {"rp": l3, "rec_total": pay_total['pay_sum'], "ex2": ex2})


def IandEDisplay(request):
    inc=Account.objects.raw('SELECT Field,id from accounts_account WHERE IandE=%s',['Income'])
    exp=Account.objects.raw('SELECT Field,id from accounts_account WHERE IandE=%s',['Exp'])
    l1=[]
    l2=[]
    for i in inc:
        if i.Field not in l1:
            l1.append(i.Field)
    for j in exp:
        if j.Field not in l2:
            l2.append(j.Field)
    print(l2)
    s=[]
    t=[]
    for i in range(len(l1)):
        s.append(0)
    for j in range(len(l2)):
        t.append(0)
    for i in range(len(l1)):
        s[i]=Account.objects.filter(IandE="Income",Field=l1[i]).aggregate(a=Sum("Amount"))
    for i in range(len(l2)):
        t[i]=Account.objects.filter(IandE="Exp",Field=l2[i]).aggregate(b=Sum("Amount"))
    inc_total=Account.objects.filter(IandE="Income").aggregate(rec_sum=Sum("Amount"))
    print(inc_total['rec_sum'])
    exp_total=Account.objects.filter(IandE="Exp").aggregate(pay_sum=Sum("Amount"))
    print(exp_total['pay_sum'])
    print(t)
    l3=[]
    for i in range(max(len(l1),len(l2))):
        dict={}
        if i<len(l1):
            dict['inc_field']=l1[i]
            dict['inc_amt']=s[i]['a']
        if i<len(l2):
            dict['exp_field']=l2[i]
            dict['exp_amt']=t[i]['b']
        l3.append(dict)
    if inc_total['rec_sum']>exp_total['pay_sum']:
        ex1=inc_total['rec_sum']-exp_total['pay_sum']
        return render(request,"IandEdisp.html",{"rp":l3,"rec_total":inc_total,"ex1":ex1})
    else:
        ex2=exp_total['pay_sum']-inc_total['rec_sum']
        return render(request, "Iandedisp.html",
                          {"rp": l3, "rec_total": exp_total['pay_sum'], "ex2": ex2})

def BalSheetDisp(request):
    asset = Account.objects.raw('SELECT Field,id from accounts_account WHERE BalSheet=%s', ['Assets'])
    lia = Account.objects.raw('SELECT Field,id from accounts_account WHERE BalSheet=%s', ['Lia'])
    l1 = []
    l2 = []
    for i in asset:
        if i.Field not in l1:
            l1.append(i.Field)
    for j in lia:
        if j.Field not in l2:
            l2.append(j.Field)
    print(l2)
    s = []
    t = []
    for i in range(len(l1)):
        s.append(0)
    for j in range(len(l2)):
        t.append(0)
    for i in range(len(l1)):
        s[i] = Account.objects.filter(BalSheet="Assets", Field=l1[i]).aggregate(a=Sum("Amount"))
    for i in range(len(l2)):
        t[i] = Account.objects.filter(BalSheet="Lia", Field=l2[i]).aggregate(b=Sum("Amount"))
    as_total = Account.objects.filter(BalSheet="Assets").aggregate(rec_sum=Sum("Amount"))
    lia_total = Account.objects.filter(BalSheet="Lia").aggregate(pay_sum=Sum("Amount"))
    l3 = []
    for i in range(max(len(l1), len(l2))):
        dict = {}
        if i < len(l1):
            dict['as_field'] = l1[i]
            dict['as_amt'] = s[i]['a']
        if i < len(l2):
            dict['lia_field'] = l2[i]
            dict['lia_amt'] = t[i]['b']
        l3.append(dict)
    inc_total = Account.objects.filter(IandE="Income").aggregate(rec_sum=Sum("Amount"))
    exp_total = Account.objects.filter(IandE="Exp").aggregate(pay_sum=Sum("Amount"))
    rec_total = Account.objects.filter(RandP="Receipts").aggregate(rec_sum=Sum("Amount"))
    pay_total = Account.objects.filter(RandP="Payments").aggregate(pay_sum=Sum("Amount"))
    c=0
    d=0
    if inc_total['rec_sum']>exp_total['pay_sum']:
        c=1
        ex1=inc_total['rec_sum']-exp_total['pay_sum']
        as_total['rec_sum']=as_total['rec_sum']+ex1
    else:
        ex1=exp_total['pay_sum']-inc_total['rec_sum']
        lia_total['pay_sum']=lia_total['pay_sum']+ex1
    if rec_total['rec_sum']>pay_total['pay_sum']:
        ex3=rec_total['rec_sum']-pay_total['pay_sum']
        lia_total['pay_sum']=lia_total['pay_sum']+ex3
    else:
        d=1
        ex3=pay_total['pay_sum']-rec_total['rec_sum']
        as_total['rec_sum']=as_total['rec_sum']+ex3
    return render(request,"bals.html",{"sheet":l3,"ie":ex1,"rp":ex3,"c":c,"d":d,"as_total":as_total,"lia_total":lia_total})