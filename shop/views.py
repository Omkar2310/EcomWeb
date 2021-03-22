from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import Product,Contact,Orders,OrderUpdate,User
import json
from math import ceil


# Create your views here.
def index(request):
    products = Product.objects.all()
    print(products)
    n=len(products)
    numofslides = n//4 + ceil((n/4) - (n//4))
    allProds=[]

    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds }

    if 'user' in request.session:
        current_user = request.session['user']
        param = {'current_user': current_user}
        return render(request,'shop/index.html',params)
    else:
        return redirect('login')
    # return render(request, 'login.html')

    

def about(request):
    return render(request,'shop/about.html')

def contact(request):
    if request.method == "POST":
        # print(request)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        print(name, email, phone, desc)
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request,'shop/contact.html')

def signup(request):
	if request.method == 'POST':
		uname = request.POST.get('uname')
		pwd = request.POST.get('pwd')
		# print(uname, pwd)
		if User.objects.filter(username=uname).count()>0:
			return HttpResponse('Username already exists.')
		else:
			user = User(username=uname, password=pwd)
			user.save()
			return redirect('login')
	else:
		return render(request, 'shop/signup.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')

def prodView(request,myid):
    #Fetch the product using the ID
    product = Product.objects.filter(id=myid)
    return render(request,'shop/prodview.html', {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        # print(request)
        items_json = request.POST.get('itemsJson', '')

        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + ' ' +  request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        print(items_json,name, email,address,city,state,zip_code ,phone )
        order = Orders(items_json=items_json,name=name, email=email, address=address,city=city,state=state,zip_code=zip_code ,phone=phone )
        order.save()
        thank = True
        id=order.order_id
        update = OrderUpdate(order_id=id,update_desc="Order has been placed")
        update.save() 
        return render(request, 'shop/checkout.html', {'thank' : thank,'id':id})

    return render(request,'shop/checkout.html')



def search(request):
    return render(request,'shop/search.html')



 
    



def login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')

        check_user = User.objects.filter(username=uname, password=pwd)
        if check_user:
            request.session['user'] = uname
            return redirect('/')
        else:
            return HttpResponse('Please enter valid Username or Password.')

    return render(request, 'shop/login.html')


def logout(request):
    try:
        del request.session['user']
    except:
        return redirect('login')
    return redirect('login')