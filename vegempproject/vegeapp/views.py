from django.shortcuts import render
from django.views.generic import FormView
from .forms import vegeform
from .models import vegemodel
from django.db.models import Q

def vegelist(request):
    data = vegemodel.objects.all()
    context = {
        'data': data
    }
    return render(request,'index.html',context)

def marketprice(request,pk):
    data = vegemodel.objects.get(pk=pk)
    others = vegemodel.objects.filter(~Q(pk=pk)) #該当野菜以外の野菜データを取得
    httprequest = request.method
    if httprequest == 'POST':
        quantity = float(request.POST['quantity']) #数量を取得し、整数ならint型に変換
        if quantity - int(quantity) == 0:
            quantity = int(quantity)
        else:
            pass
        price = int(data.price) #該当野菜の価格を取得
        weight = int(data.weight) #該当野菜の重さを取得
        gram = quantity * weight #グラム数演算
        result = round(price * (gram / 1000),1) #演算
        if result - int(result) == 0: #金額が整数ならint型に変換
            result = int(result)
        else:
            pass
        context = {
            'request' : httprequest,
            'data': data,
            'others' : others,
            'quantity' : quantity,
            'result' : result,
        }
        return render(request,'marketprice.html',context)
    else:
        quantity = 0
        result = 0
        context = {
            'request' : httprequest,
            'data': data,
            'others' : others,
            'quantity' : quantity,
            'result' : result,
        }
        return render(request,'marketprice.html',context)

def about(request):
    return render(request,'about.html')

def datasource(request):
    return render(request,'datasource.html')