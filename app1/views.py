from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'a/themexriver.com/tfhtml/finance-top/index.html')