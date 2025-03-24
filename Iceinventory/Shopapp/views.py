from django.shortcuts import render, redirect, get_object_or_404
from Shopapp.models import CategoryDb, ProductDb 
from Iceapp.models import ContactDb, Order

# ProductDb
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate,login, logout
from django.views.decorators.cache import never_cache, cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError

# Create your views here.
@login_required(login_url='admin_login')
@never_cache
@cache_control(no_store=True, must_revalidate=True)
def adminindexpage(request):
    cat = CategoryDb.objects.all().count()
    pro = ProductDb.objects.all().count()
    order = Order.objects.all().count()
    return render(request, "adminindex.html",{ 'cat':cat, 'pro':pro, 'order':order})

def indexpage(request):
    return render(request, "index.html")


def admin_login(request):
    return render(request,"AdminLogin.html")
def adminlogin(request):
    if request.method=="POST":
        un=request.POST.get('user_name')
        pwd=request.POST.get('pass_word')
        if User.objects.filter(username__contains=un).exists():
            x = authenticate(username=un, password=pwd)
            if x is not None:
                login(request, x)
                request.session['username']=un
                request.session['password']=pwd
                messages.success(request, "Login successful")
                return redirect(adminindexpage)
            else:
                messages.error(request, "Invalid Username or Password")
                return redirect(admin_login)
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect(admin_login)
def admin_logout(request):
    logout(request)  # Clears the session
    messages.success(request, "Logout successful")
    
    return redirect(indexpage)

def categorypage(request):
    return render(request, "AddCategory.html")

def savecategory(request):
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        status = request.POST.get('status')
        category_image = request.FILES.get('category_image')
        user = request.user
        shop_owner = ShopOwner.objects.get(user=user)

        if not category_name:
            messages.error(request, "Category name is required!")
            return redirect("categorypage")

        # Create and save category
        category = CategoryDb(
            category_name=category_name,
            description=description,
            status=status,
            category_image=category_image,
            shop_owner=shop_owner,
        )
        try:
            category.full_clean()
            category.save()
            messages.success(request, "Category added successfully!")
        except ValidationError as e:
            messages.error(request, f"Error: {e}")

        return redirect("categorypage")

def category_display(request):
    categories = CategoryDb.objects.filter(is_approved=True)
    return render(request, 'DisplayCategory.html', {'categories': categories})

def deletecategory(request, dataid):
    if request.method == "POST":
        category = get_object_or_404(CategoryDb, id=dataid)
        category.delete()
        messages.success(request, "Category deleted successfully!")
    return redirect("category_display")

def editcategory(request, dataid):
    category = get_object_or_404(CategoryDb, id=dataid)
    return render(request, "EditCategory.html", {'category': category})

def updatecategory(request, dataid):
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        status = request.POST.get('status')
        category_image = request.FILES.get('category_image')

        # Retrieve category object
        category = get_object_or_404(CategoryDb, id=dataid)

        # Update fields
        category.category_name = category_name
        category.description = description
        category.status = status

        # Only update image if a new one is uploaded
        if category_image:
            category.category_image.delete(save=False)  # Delete the old image
            category.category_image = category_image

        try:
            category.full_clean()
            category.save()
            messages.success(request, "Category updated successfully!")
        except ValidationError as e:
            messages.error(request, f"Error: {e}")

        return redirect("category_display")

def productpage(request):
    catdis = CategoryDb.objects.all()
    return render(request, "AddProduct.html", {'catdis':catdis})

def saveproduct(request):
    if request.method == "POST":
        cat_id = request.POST.get('categoryname')  # Get category ID from form

        if not cat_id or not cat_id.isdigit():  # Ensure it's a valid number
            messages.error(request, "Invalid category selected")
            return redirect('productpage')

        category = get_object_or_404(CategoryDb, id=int(cat_id))  # Fetch category object
        user = request.user
        # shop_owner = ShopOwner.objects.get(user=user)
        shop_owner = get_object_or_404(ShopOwner, user=user)

        # Get form data
        product_name = request.POST.get('name')
        description = request.POST.get('description')
        product_price = request.POST.get('price')
        stock = request.POST.get('stock')
        status = request.POST.get('status')
        product_image = request.FILES.get('image', None)

        # Validate required fields
        if not product_name or not product_price or not status:
            messages.error(request, "Please fill all required fields")
            return redirect('productpage')

        # Create and save product
        obj = ProductDb(
            product_category=category,  # Corrected from 'categoryname' to 'category'
            product_name=product_name,
            description=description,
            product_price=product_price,
            stock=stock,
            status=status,
            product_image=product_image,
            shop_owner=shop_owner
        )
        obj.save()
        messages.success(request, "Product added successfully!")
        return redirect('productpage')

    messages.error(request, "Invalid request")
    return redirect('productpage')


def product_display(request):
    prod = ProductDb.objects.filter(is_approved=True, stock__gt=0)
    return render(request, 'DisplayProduct.html', {'prod': prod})
def editproduct(request,dataid):
    cat = CategoryDb.objects.all()
    prods = ProductDb.objects.get(id=dataid)
    return render(request,"EditProduct.html",{'cat':cat, 'prods':prods})
def updateproduct(request, dataid):
    if request.method == "POST":
        cp_id = request.POST.get('categoryname')  # Get the category ID from form
        cp = get_object_or_404(CategoryDb, id=cp_id)  # Fetch category object

        nam = request.POST.get('name')
        des = request.POST.get('description')
        pri = request.POST.get('price')
        st = request.POST.get('stock')

        try:
            img = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = ProductDb.objects.get(id=dataid).product_image

        ProductDb.objects.filter(id=dataid).update(
            product_category=cp,  # Assign category object, not a string
            product_name=nam,
            description=des,
            product_price=pri,
            stock=st,
            product_image=file
        )

        return redirect(product_display)

def deleteproduct(request, dataid):
    prods = ProductDb.objects.filter(id=dataid)
    prods.delete()
    return redirect(product_display)
@login_required(login_url='admin_login')
@never_cache
@cache_control(no_store=True, must_revalidate=True)
def approve_category(request, dataid):
    category = get_object_or_404(CategoryDb, id=dataid)
    category.is_approved = True
    category.save()
    messages.success(request, "Category approved successfully!")
    return redirect('admin_category_approval')
@login_required(login_url='admin_login')
@never_cache
@cache_control(no_store=True, must_revalidate=True)
def reject_category(request, dataid):
    category = get_object_or_404(CategoryDb, id=dataid)
    category.delete()
    messages.error(request, "Category rejected and removed!")
    return redirect('admin_category_approval')
@login_required(login_url='admin_login')
@never_cache
@cache_control(no_store=True, must_revalidate=True)
def approve_product(request, dataid):
    product = get_object_or_404(ProductDb, id=dataid)
    product.is_approved = True
    product.save()
    messages.success(request, "Product approved successfully!")
    return redirect('admin_product_approval')
@login_required(login_url='admin_login')
@never_cache
@cache_control(no_store=True, must_revalidate=True)
def reject_product(request, dataid):
    product = get_object_or_404(ProductDb, id=dataid)
    product.delete()
    messages.error(request, "Product rejected and removed!")
    return redirect('admin_product_approval')
@login_required(login_url='admin_login')
@never_cache
@cache_control(no_store=True, must_revalidate=True)
def admin_category_approval(request):
    categories = CategoryDb.objects.filter(is_approved=False).select_related('shop_owner')
    return render(request, 'AdminCategoryApproval.html', {'categories': categories})
@login_required(login_url='admin_login')
@never_cache
@cache_control(no_store=True, must_revalidate=True)
def admin_product_approval(request):
    products = ProductDb.objects.filter(is_approved=False)
    return render(request, 'AdminProductApproval.html', {'products': products})

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from datetime import datetime
from Iceapp.models import Order  # Adjust the import based on your app structure

class OrderListView(View):
    """View to display all orders."""
    def get(self, request):
        orders = Order.objects.all().order_by('-order_date')
        return render(request, "OrderList.html", {"orders": orders})

class UpdateOrderStatusView(View):
    """View to update the status of an order."""
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get("status")

        if new_status in dict(Order.STATUS_CHOICES):
            order.update_status(new_status)
            messages.success(request, f"Order {order.id} status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status selection.")

        return redirect("order_list")

class DeleteOrderView(View):
    """View to delete an order."""
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        messages.success(request, f"Order {order.id} deleted successfully.")
        return redirect("order_list")
@login_required(login_url='admin_login')
@never_cache
@cache_control(no_store=True, must_revalidate=True)
def contact_details(request):
    """Fetch and display all contact messages."""
    contacts = ContactDb.objects.all().order_by("-id")  # Latest messages first
    return render(request, "contact_details.html", {"contacts": contacts})



from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ShopOwnerRegistrationForm
from .models import ShopOwner



def ownerpage(request, user_id):
    shop_owner = get_object_or_404(ShopOwner, user__id=user_id)

    # Ensure the logged-in user is accessing their own page
    if request.user.id != user_id:
        return redirect("forbidden_page")  # Redirect if unauthorized

    return render(request, "Ownerindex.html", {"shop_owner": shop_owner})
def register(request):
    if request.method == 'POST':
        form = ShopOwnerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            shop_owner = form.save(commit=False)
            shop_owner.user = user
            shop_owner.save()
            login(request, user)  # Auto-login after registration
            return redirect('ownerpage', user_id=user.id)  # Redirect to a dashboard page
    else:
        form = ShopOwnerRegistrationForm()
    
    return render(request, 'Register.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import ShopOwnerLoginForm

def shop_owner_login(request):
    
    if request.method == "POST":
        form = ShopOwnerLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                remember_me = form.cleaned_data.get('remember_me')

                # Set session expiry based on "Remember Me" checkbox
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Session expires when browser closes
                
                messages.success(request, "Login successful!")
                return redirect('ownerpage', user_id=user.id)  # Redirect to a dashboard page after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ShopOwnerLoginForm()

    return render(request, "Login.html", {"form": form})

    from django.contrib.auth import logout

def shop_owner_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('indexpage')  # Redirect back to login page after logout

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import ShopOwner
from .forms import ShopOwnerRegistrationForm

# @login_required
# def profile_view(request):
#     shop_owner = get_object_or_404(ShopOwner, user=request.user)
#     user = request.user  

#     if request.method == 'POST':
#         if 'delete_profile' in request.POST:
#             shop_owner.delete()
#             user.delete()
#             messages.success(request, 'Profile deleted successfully!')
#             return redirect('indepage')

#         form = ShopOwnerRegistrationForm(request.POST, request.FILES, instance=shop_owner)
#         if form.is_valid():
#             shop_owner = form.save(commit=False)
#             user.username = request.POST.get("username", user.username)
#             user.email = request.POST.get("email", user.email)
#             user.save()
#             shop_owner.save()
#             messages.success(request, 'Profile updated successfully!')
#             return redirect('profile')
#     else:
#         form = ShopOwnerRegistrationForm(instance=shop_owner)

#     return render(request, 'owner_profile.html', {'form': form, 'shop_owner': shop_owner})
@login_required
def profile_view(request):
    print("✅ Accessing profile page for user:", request.user)

    shop_owner = get_object_or_404(ShopOwner, user=request.user)
    user = request.user  

    print("✅ ShopOwner found:", shop_owner)

    form = ShopOwnerRegistrationForm(instance=shop_owner)

    return render(request, 'owner_profile.html', {'form': form, 'shop_owner': shop_owner})


@login_required
def edit_profile(request):
    shop_owner = get_object_or_404(ShopOwner, user=request.user)
    user = request.user  # Get user instance

    if request.method == "POST":
        form = ShopOwnerRegistrationForm(request.POST, request.FILES, instance=shop_owner)

        if form.is_valid():
            shop_owner = form.save(commit=False)
            shop_owner.owner_name = form.cleaned_data["owner_name"]
            shop_owner.phone = form.cleaned_data["phone"]
            shop_owner.shop_name = form.cleaned_data["shop_name"]
            shop_owner.location = form.cleaned_data["location"]

            # Update profile image only if a new one is uploaded
            if "shop_image" in request.FILES:
                shop_owner.shop_image = request.FILES["shop_image"]

            # Update the user email separately
            user.email = form.cleaned_data["email"]
            user.save()

            shop_owner.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")  # Redirect to profile page

        else:
            print("❌ Form errors:", form.errors)
            messages.error(request, "Please correct the errors below.")

    else:
        form = ShopOwnerRegistrationForm(instance=shop_owner, initial={"email": user.email})

    return render(request, "EditProfile.html", {"form": form, "shop_owner": shop_owner})