from django.shortcuts import render,redirect, get_object_or_404
from Shopapp.models import CategoryDb, ProductDb
from Iceapp.models import Customer, ContactDb,CartDb, Checkoutdb, Order
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import razorpay
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
# def singleproductpage(request, proid):
#     cat = CategoryDb.objects.all()
#     data = ProductDb.objects.get(id=proid)
#     return render(request, "SingleProduct.html", {'data':data, 'cat':cat})
# def singleproductpage(request, proid):
#     cat = CategoryDb.objects.all()
#     data = ProductDb.objects.get(id=proid)
#     try:
#         stock = IceStock.objects.get(ice_type=data)  # Fetch stock related to the product
#     except IceStock.DoesNotExist:
#         stock = None

#     return render(request, "SingleProduct.html", {'data': data, 'cat': cat, 'stock': stock})
def singleproductpage(request, proid):
    cat = CategoryDb.objects.all()  # Fetch all categories
    data = ProductDb.objects.get(id=proid)  # Fetch the product by id
    stock = data.stock  # Get the stock directly from the ProductDb model

    return render(request, "SingleProduct.html", {'data': data, 'cat': cat, 'stock': stock})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def reduce_stock(request, product_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON
            quantity = int(data.get("quantity"))  # Get quantity

            product = ProductDb.objects.get(id=product_id)  # Fetch product

            if product.stock >= quantity:
                product.stock -= quantity  # Reduce stock
                product.save()  # Save update
                return JsonResponse({
                    "status": "success", 
                    "message": "Stock updated!", 
                    "remaining_stock": product.stock
                })
            else:
                return JsonResponse({
                    "status": "error", 
                    "message": "Not enough stock!"
                })
        except ProductDb.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Product not found!"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data!"})
    
    return JsonResponse({"status": "error", "message": "Invalid request!"})

def contactpage(request):
    cat = CategoryDb.objects.all()
    return render(request, "Contact.html", {'cat':cat})
def savecontact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if not name or not email or not subject or not message:
            messages.error(request, "All fields are required!")
            return redirect("contactpage")

        # Save to database
        ContactDb.objects.create(
            Contact_Name=name,
            Contact_Email=email,
            Subject=subject,
            Message=message
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect("contactpage")

    return redirect("contactpage")  # Redirect if accessed via GET

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



# def cartpage(request):
#     data = CartDb.objects.filter(Username=request.session['username'])
#     total_price = 0
#     for i in data:
#         total_price = total_price+i.Total_Price
#     return render(request,"Cart.html" , {'data':data, 'total_price':total_price})
@login_required(login_url='user_login')  # Ensures user must be logged in
def cartpage(request):
    username = request.user.username  # Get the authenticated user's username
    cart_items = CartDb.objects.filter(Username=username)
    
    # Get stock for each product in the cart
    cart_data = []
    total_price = 0

    for item in cart_items:
        product = ProductDb.objects.filter(product_name=item.Productname).first()
        stock_quantity = product.stock if product else 0  # Get stock if product exists
        total_price += item.Total_Price

        cart_data.append({
            "id": item.id,
            "Productname": item.Productname,
            "Quantity": item.Quantity,
            "Total_Price": item.Total_Price,
            "Description": item.Description,
            "Stock": stock_quantity  # Add stock to context
        })

    return render(request, "Cart.html", {'data': cart_data, 'total_price': total_price})


@login_required(login_url='user_login')  
def savecart(request):
    if request.method == "POST":
        username = request.POST.get('username')
        product_name = request.POST.get('productname')
        quantity = int(request.POST.get('quantity'))
        price = float(request.POST.get('price'))
        description = request.POST.get('description')

        try:
            product = ProductDb.objects.get(product_name=product_name)

            if product.stock >= quantity:  # Check stock availability
                product.stock -= quantity  # Reduce stock
                product.save()  # Save updated stock

                # Save cart details
                CartDb.objects.create(
                    Username=username,
                    Productname=product_name,
                    Quantity=quantity,
                    Total_Price=quantity * price,
                    Description=description
                )
                
                return redirect("cartpage")  # Redirect to cart
            else:
                return render(request, "SingleProduct.html", {
                    "data": product,
                    "error": "Not enough stock available"
                })

        except ProductDb.DoesNotExist:
            return render(request, "SingleProduct.html", {
                "error": "Product not found!"
            })

    return redirect("singleproductpage")  
def deletecart(request, dataid):
    cart_item = get_object_or_404(CartDb, id=dataid)

    # Find the corresponding product in ProductDb
    product = ProductDb.objects.filter(product_name=cart_item.Productname).first()
    if product:
        product.stock += cart_item.Quantity  # Update stock quantity
        product.save()

    cart_item.delete()  # Delete the cart item

    return redirect('cartpage')

@login_required
def checkoutpage(request):
    username = request.user.username  # Get logged-in user's username
    data = CartDb.objects.filter(Username=username)  # Filter cart items for the user
    total_price = sum(item.Total_Price for item in data if item.Total_Price)  # Calculate total price

    return render(request, "Checkout.html", {'username': username, 'data': data, 'total_price': total_price})


def save_checkout(request):
    if request.method == "POST":
        print(request.POST)  # Debug: Print form data received
        fn = request.POST.get('fname')
        ln = request.POST.get('lname')
        ema = request.POST.get('email')
        add = request.POST.get('addr')
        city = request.POST.get('city')
        count = request.POST.get('country')
        tel = request.POST.get('tele')
        pr_id = request.POST.get('product_id')
        user_id = request.POST.get('user')
        # user = get_object_or_404(User, username=user_id)
        user = request.user
        # customer = Customer.objects.get(user=user)
        cart = CartDb.objects.filter(id=pr_id).first()


        username = request.user.username  # Get logged-in username
        print(f"Username: {username}, FirstName: {fn}, LastName: {ln}, Email: {ema}, Address: {add}")  # Debug

        if not all([fn, ln, ema, add, city, count, tel]):  # Ensure no empty fields
            messages.error(request, "All fields are required.")
            return redirect(checkoutpage)

        obj = Checkoutdb(
            FirstName=fn,
            LastName=ln,
            EmailId=ema,
            Address=add,
            City=city,
            Country=count,
            Telephone=tel,
            user=user,
            cart=cart # Store the username in the database
        )
        try:
            obj.save()
            messages.success(request, "Checkout saved successfully!")
        except Exception as e:
            messages.error(request, f"Error saving checkout: {e}")  # Debugging error message
            print("Database Save Error:", e)

        return redirect(paymentpage)

def yourorder(request):
    messages.success(request, "Place order has been success....!")
    return redirect(homepage)

@login_required
def paymentpage(request):
    if request.method == "GET":
        username = request.user.username
        data = CartDb.objects.filter(Username=username)

        if not data:
            messages.error(request, "Your cart is empty.")
            return redirect("cartpage")

        total_price = sum(item.Total_Price for item in data if item.Total_Price)
        order_currency = "INR"
        
        client = razorpay.Client(auth=('rzp_test_8ZlQ5ZrMiHMwmU', 'f59o6eHBPsp6w3F2RW6ExcgZ'))
        payment = client.order.create({'amount': total_price * 100, 'currency': order_currency, 'payment_capture': '1'})

        return render(
            request,
            "Payment.html",
            {
                "razorpay_key": 'rzp_test_W3mMQR6ikpp5sy',
                "payment": payment,
            },
        )

    return render(request, "Payment.html")

# @login_required
# def payment_success(request):
#     """Handles post-payment logic."""
    
#     # Get Razorpay payment ID from the URL
#     payment_id = request.GET.get("payment_id")

#     if not payment_id:
#         messages.error(request, "Payment verification failed!")
#         return redirect(cartpage)

#     username = request.user.username
#     cart_items = CartDb.objects.filter(Username=username)

#     if not cart_items:
#         messages.error(request, "No items in cart to process.")
#         return redirect(cartpage)

#     # Reduce stock after successful payment
#     for item in cart_items:
#         product = get_object_or_404(ProductDb, product_name=item.Productname)

#         if product.stock >= item.Quantity:
#             product.stock -= item.Quantity
#             product.save()
#         else:
#             messages.error(request, f"{product.product_name} is out of stock!")
#             return redirect(cartpage)  # Redirect if stock is insufficient

#     # Clear cart after successful order
#     cart_items.delete()

#     messages.success(request, "Payment successful! Your order has been placed.")
#     return render(request, "payment_success.html", {"payment_id": payment_id})

# @login_required
# def payment_success(request):
#     """Handles post-payment logic."""
#     payment_id = request.GET.get("payment_id")

#     if not payment_id:
#         messages.error(request, "Payment verification failed!")
#         return redirect("cartpage")

#     username = request.user.username
#     cart_items = CartDb.objects.filter(Username=username)

#     if not cart_items:
#         messages.error(request, "No items in cart to process.")
#         return redirect("cartpage")

#     # Prepare order details
#     order_products = []
#     total_price = 0

#     for item in cart_items:
#         product = get_object_or_404(ProductDb, product_name=item.Productname)

#         if product.stock >= item.Quantity:
#             product.stock -= item.Quantity  # Reduce stock
#             product.save()
#         else:
#             messages.error(request, f"{product.product_name} is out of stock!")
#             return redirect("cartpage")

#         order_products.append({
#             "Productname": item.Productname,
#             "Quantity": item.Quantity,
#             "Total_Price": item.Total_Price,
#         })
#         total_price += item.Total_Price

#     # Create Order entry
#     order = Order.objects.create(
#         user=request.user,
#         products=order_products,
#         total_price=total_price,
#         status="Processing"  # Default status after payment
#     )

#     # Clear cart after successful order
#     cart_items.delete()

#     messages.success(request, "Payment successful! Your order has been placed.")
#     return render(request, "payment_success.html", {"payment_id": payment_id, "order": order})



# from django.contrib.auth.decorators import login_required
@login_required
def payment_success(request):
    """Handles post-payment logic only after confirming payment."""
    payment_id = request.GET.get("payment_id")

    if not payment_id:
        messages.error(request, "Payment verification failed!")
        return redirect("cartpage")

    username = request.user.username
    cart_items = CartDb.objects.filter(Username=username)

    if not cart_items:
        messages.error(request, "No items in cart to process.")
        return redirect("cartpage")

    # Prepare order details
    order_products = []
    total_price = 0

    for item in cart_items:
        product = get_object_or_404(ProductDb, product_name=item.Productname)

        order_products.append({
            "Productname": item.Productname,
            "Quantity": item.Quantity,
            "Total_Price": item.Total_Price,
        })
        total_price += item.Total_Price

    # Create Order entry first (before reducing stock)
    order = Order.objects.create(
        user=request.user,
        products=order_products,
        total_price=total_price,
        status="Processing"  # Default status after payment
    )

    # Now, reduce stock safely
    for item in cart_items:
        product = get_object_or_404(ProductDb, product_name=item.Productname)

        if product.stock >= item.Quantity:
            product.stock -= item.Quantity  # Reduce stock only after order is confirmed
            product.save()
        else:
            # If stock is insufficient after payment, cancel the order and refund
            order.delete()
            messages.error(request, f"Payment successful, but {product.product_name} is out of stock! Refund initiated.")
            return redirect("cartpage")

    # Clear cart after successful order
    cart_items.delete()

    messages.success(request, "Payment successful! Your order has been placed.")
    return render(request, "payment_success.html", {"payment_id": payment_id, "order": order})

@login_required
def order_history(request):
    """Displays the user's past orders after successful payment."""
    orders = Order.objects.filter(user=request.user).order_by("-order_date")
    return render(request, "Order.html", {"orders": orders})
# from django.shortcuts import render, redirect
# from django.views import View
# from .models import Order, Customer

# class CheckoutView(View):
#     def get(self, request):
#         return render(request, 'checkout.html')  # Render the checkout page

#     def post(self, request):
#         customer_id = request.POST.get('customer_id')
#         stock_id = request.POST.get('stock_id')
#         quantity = request.POST.get('quantity')

#         try:
#             customer = Customer.objects.get(id=customer_id)
#             stock = ProductDb.objects.get(id=stock_id)

#             order = Order.objects.create(
#                 customer=customer,
#                 stock=stock,
#                 quantity_ordered=quantity,
#                 status="pending"
#             )
#             return redirect('make_payment', order_id=order.id)
#         except Customer.DoesNotExist:
#             return render(request, 'checkout.html', {'error': 'Customer not found'})
#         except ProductDb.DoesNotExist:
#             return render(request, 'checkout.html', {'error': 'Product not found'})
# class PaymentView(View):
#     def get(self, request, order_id):
#         order = Order.objects.get(id=order_id)
#         return render(request, 'make_payment.html', {'order': order})

# class ConfirmPaymentView(View):
#     def post(self, request, order_id):
#         order = Order.objects.get(id=order_id)
#         payment_method = request.POST.get('payment_method')

#         # Update order status after payment confirmation
#         order.status = "delivered" if payment_method != "Cash on Delivery" else "pending"
#         order.save()

#         return redirect('payment_success', order_id=order.id)

# class PaymentSuccessView(View):
#     def get(self, request, order_id):
#         order = Order.objects.get(id=order_id)
#         return render(request, 'payment_success.html', {'order': order})
# def PaymentSuceessful(request, product_id):
#     product = ProductDb.objects.get(id=product_id)
#     context= {
#         "product": product
#     }
#     return render(request, "")


# def paymentpage(request):
#     if request.method == "GET":
#         data = CartDb.objects.filter(Username=request.session['UserName'])
#         amount = 0
#         for i in data:
#             amount = amount + i.Total_Price
#         order_currency="INR"
#         client = razorpay.Client(auth=('rzp_test_8ZlQ5ZrMiHMwmU','f59o6eHBPsp6w3F2RW6ExcgZ'))
#         payment=client.order.create({'amount':amount*100,'currency':order_currency,'payment_capture':'1'})
#         return render(
#             request,
#             "payment.html",
#             {
#                 "razorpay_key": 'rzp_test_W3mMQR6ikpp5sy',
#                 "payment": payment,
#             },
#         )
#     return render(request,"payment.html")
