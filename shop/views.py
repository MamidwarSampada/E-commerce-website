from django.shortcuts import render
from django.http import HttpResponse
from shop.models import Product,Contact,Orders,OrderUpdate
import json
import math

# Create your views here.
def index(request):
    allprods=[]
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        nSlides=n//4+math.ceil((n/4)+(n//4))
        ns=math.ceil(n/4)
        allprods.append([prod,range(1,ns),nSlides])
    params={
        'allprods':allprods
    }
    return render(request,'shop/index.html',params)

def searchMatch(query,item):
    if query.lower() in item.desc.lower() or query.lower() in item.product_name.lower() or query.lower() in item.category.lower():
        return True
    else:
        return False

def search(request):
   
    query=request.GET.get('search')
    allprods=[]
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prodtemp=Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query,item)]
        n=len(prod)
        nSlides=n//4+math.ceil((n/4)+(n//4))
        ns=math.ceil(n/4)
        if len(prod)!=0:
            allprods.append([prod,range(1,ns),nSlides])
    params={
        'allprods':allprods,
        'msg':'',
        'query':query,
    }
    if len(allprods)==0:
        params={'msg':"No Result Found!!! Please Enter Valid Data To Search...."}
        
    return render(request,'shop/search.html',params)

def about(request):
    return render(request,'shop/about.html')

def contact(request):
    thank=False
    if request.method=='POST':
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank = True
    return render(request,'shop/contact.html',{'thank':thank})

def tracker(request):
    if request.method=='POST':
        orderId=request.POST.get('orderId','')
        email=request.POST.get('email','')
        
        try:
            order=Orders.objects.filter(order_id=orderId,email=email)
            print(len(order))
            if len(order)>0:
                update= OrderUpdate.objects.filter(order_id=orderId)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response=json.dumps({"status":"success","updates":updates,"itemsJson":order[0].items_json},default=str)
                    print(response)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request,'shop/tracker.html')



def productView(request,myid):
    product=Product.objects.get(id=myid)
    # print(product)
    return render(request,'shop/productview.html',{'product':product})

def buynow(request,myid):
    product=Product.objects.get(id=myid)
    if request.method=="POST":
        items_json= request.POST.get('itemsJson', '')
        name=request.POST.get('name', '')
        amount=request.POST.get('amount')
        email=request.POST.get('email', '')
        address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city=request.POST.get('city', '')
        state=request.POST.get('state', '')
        zip_code=request.POST.get('zip_code', '')
        phone=request.POST.get('phone', '')
        
        order = Orders(items_json= items_json, name=name, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone,amount=amount)
        order.save()
        update=OrderUpdate(order_id=order.order_id,update_desc="The order has been placed")
        update.save()
        thank=True
        id=order.order_id
        return render(request, 'shop/buynow.html', {'thank':thank, 'id':id})
        
    
    return render(request, 'shop/buynow.html',{'product':product})
    
def checkout(request):
    if request.method=="POST":
        items_json= request.POST.get('itemsJson', '')
        name=request.POST.get('name', '')
        amount=request.POST.get('amount', '')
        email=request.POST.get('email', '')
        address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city=request.POST.get('city', '')
        state=request.POST.get('state', '')
        zip_code=request.POST.get('zip_code', '')
        phone=request.POST.get('phone', '')
        
        order = Orders(items_json= items_json, name=name, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone,amount=amount)
        order.save()
        update=OrderUpdate(order_id=order.order_id,update_desc="The order has been placed")
        update.save()
        thank=True
        id=order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
        
    
    return render(request, 'shop/checkout.html')

