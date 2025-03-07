from django.shortcuts import render,redirect, get_object_or_404
from Shopapp.models import CategoryDb,ProductDb
from Iceapp.models import ContactDb,CartDb,Checkoutdb
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
# import razorpay
# Create your views here.
def homepage(request):
    cat = CategoryDb.objects.all()
    return render(request,"Home.html", {'cat':cat})

def user_login(request):
    """Handles user login."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse_lazy("homepage"))
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, "Register.html")

def savereg(request):
    """Handles user registration."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Secure password hashing
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect("user_login")
        else:
            messages.error(request, "Registration failed. Please check the form.")
    
    return render(request, "Register.html", {"form": form})

def user_logout(request):
    """Handles user logout."""
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("indexpage")

def productspage(request):
    cat = CategoryDb.objects.all()
    pro = ProductDb.objects.all()
    return render(request,"Products.html",{'pro':pro, 'cat':cat})
def product_filter_page(request, cat_name):
    cat = CategoryDb.objects.all()
    data = ProductDb.objects.filter(product_category__category_name=cat_name)
    return render(request, "Products_Filtered.html", {'data':data, 'cat':cat})
def singleproductpage(request, proid):
    cat = CategoryDb.objects.all()
    data = ProductDb.objects.get(id=proid)
    return render(request, "SingleProduct.html", {'data':data, 'cat':cat})
def contactpage(request):
    cat = CategoryDb.objects.all()
    return render(request, "Contact.html", {'cat':cat})
def aboutpage(request):
    cat = CategoryDb.objects.all()
    return render(request, "AboutUs.html",{'cat':cat})
def servicepage(request):
    cat = CategoryDb.objects.all()
    return render(request, "Services.html",{'cat':cat})
def savecontact(request):
    if request.method == "POST":
        na = request.POST.get('name')
        em = request.POST.get('email')
        sub = request.POST.get('subject')
        mes = request.POST.get('message')
        obj = ContactDb(Contact_Name=na, Contact_Email=em, Subject=sub, Message=mes)
        obj.save()
        return redirect(contactpage)



def cartpage(request):
    data = CartDb.objects.filter(Username=request.session['Username'])
    total_price = 0
    for i in data:
        total_price = total_price+i.Total_Price
    return render(request,"Cart.html" , {'data':data, 'total_price':total_price})
def savecart(request):
    if request.method == "POST":
        na = request.POST.get('username')
        pna = request.POST.get('productname')
        qty = float(request.POST.get('quantity'))
        tp = float(request.POST.get('total'))
        des = request.POST.get('description')

        product = get_object_or_404(ProductDb, product_name=pna)
        stock = IceStock.objects.filter(ice_type=product).first()

        if not stock or stock.quantity_kg <= 0:
            messages.error(request, "This product is out of stock.")
            return redirect('singleproductpage', proid=product.id)

        if qty <= 0:
            messages.error(request, "Invalid quantity.")
            return redirect('singleproductpage', proid=product.id)

        if qty > stock.quantity_kg:
            messages.error(request, "Not enough stock available.")
            return redirect('singleproductpage', proid=product.id)

        # Check if the item is already in the cart for this user
        existing_cart_item = CartDb.objects.filter(Username=na, Productname=pna).first()

        if existing_cart_item:
            # Update existing cart item
            existing_cart_item.Quantity += qty
            existing_cart_item.Total_Price += tp
            existing_cart_item.save()
        else:
            # Create new cart item
            CartDb.objects.create(
                Username=na,
                Productname=pna,
                Quantity=qty,
                Total_Price=tp,
                Description=des
            )

        # Deduct stock
        stock.quantity_kg -= qty
        stock.save()

        messages.success(request, "Item added to cart successfully!")
        return redirect('cartpage')  # Use the name from urls.py

    return redirect('cartpage')

def deletecart(request, dataid):
    cart_item = get_object_or_404(CartDb, id=dataid)

    # Find the corresponding product in IceStock
    product = ProductDb.objects.filter(product_name=cart_item.Productname).first()
    if product:
        stock = IceStock.objects.filter(ice_type=product).first()
        if stock:
            stock.quantity_kg += cart_item.Quantity
            stock.save()

    cart_item.delete()

    return redirect('cartpage')

def checkoutpage(request):
    return render(request, "Checkout.html")
def checkoutpage(request):
    data = CartDb.objects.filter(Username=request.session['username'])
    total_price = 0
    for i in data:
        total_price = total_price + i.Total_Price
    return render(request,"Checkout.html",{'data':data,'total_price':total_price})
def save_checkout(request):
    if request.method=="POST":
        fn=request.POST.get('fname')
        ln= request.POST.get('lname')
        ema = request.POST.get('email')
        add = request.POST.get('addr')
        city = request.POST.get('city')
        count = request.POST.get('country')
        tel = request.POST.get('tele')
        obj=Checkoutdb(FirstName=fn,LastName=ln,EmailId=ema,Address=add,City=city,Country=count,Telephone=tel)
        obj.save()
        messages.success(request, "Checkout save successfully....!")
        return redirect(checkoutpage)
def yourorder(request):
    messages.success(request, "Place order has been success....!")
    return redirect(homepage)

def paymentpage(request):
    if request.method == "GET":
        data = CartDb.objects.filter(Username=request.session['UserName'])
        amount = 0
        for i in data:
            amount = amount + i.Total_Price
        order_currency="INR"
        client = razorpay.Client(auth=('rzp_test_8ZlQ5ZrMiHMwmU','f59o6eHBPsp6w3F2RW6ExcgZ'))
        payment=client.order.create({'amount':amount*100,'currency':order_currency,'payment_capture':'1'})
        return render(
            request,
            "payment.html",
            {
                "razorpay_key": 'rzp_test_W3mMQR6ikpp5sy',
                "payment": payment,
            },
        )
    return render(request,"payment.html")
