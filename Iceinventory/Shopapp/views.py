from django.shortcuts import render, redirect, get_object_or_404
from Shopapp.models import CategoryDb,ProductDb,IceStock
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError

# Create your views here.
def adminindexpage(request):
    return render(request, "adminindex.html")

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
    del request.session['username']
    messages.success(request, "Logout successfull")
    return redirect(indexpage)

def categorypage(request):
    return render(request, "AddCategory.html")

def savecategory(request):
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        status = request.POST.get('status')
        category_image = request.FILES.get('category_image')

        if not category_name:
            messages.error(request, "Category name is required!")
            return redirect("categorypage")

        # Create and save category
        category = CategoryDb(
            category_name=category_name,
            description=description,
            status=status,
            category_image=category_image
        )
        try:
            category.full_clean()
            category.save()
            messages.success(request, "Category added successfully!")
        except ValidationError as e:
            messages.error(request, f"Error: {e}")

        return redirect("categorypage")

def category_display(request):
    categories = CategoryDb.objects.all()
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

        # Get form data
        product_name = request.POST.get('name')
        description = request.POST.get('description')
        product_price = request.POST.get('price')
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
            status=status,
            product_image=product_image
        )
        obj.save()
        messages.success(request, "Product added successfully!")
        return redirect('productpage')

    messages.error(request, "Invalid request")
    return redirect('productpage')


def product_display(request):
    prod = ProductDb.objects.all()
    return render(request,'DisplayProduct.html',{'prod':prod})
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
            product_image=file
        )

        return redirect(product_display)

def deleteproduct(request, dataid):
    prods = ProductDb.objects.filter(id=dataid)
    prods.delete()
    return redirect(product_display)

def add_icestock(request):
    products = ProductDb.objects.all()  # Fetch available products
    return render(request, "AddIceStock.html", {"products": products})

def save_icestock(request):
    if request.method == "POST":
        ice_type_id = request.POST.get("ice_type")  # Get selected product ID
        quantity_kg = request.POST.get("quantity_kg")
        reorder_point = request.POST.get("reorder_point")

        try:
            ice_type = ProductDb.objects.get(id=ice_type_id)  # Fetch product instance
            IceStock.objects.create(
                ice_type=ice_type,
                quantity_kg=quantity_kg,
                reorder_point=reorder_point,
            )
            messages.success(request, "Ice stock added successfully!")
        except ProductDb.DoesNotExist:
            messages.error(request, "Invalid product selection.")

        return redirect("icestock_display")

def icestock_display(request):
    stocks = IceStock.objects.all()
    return render(request, "IceStockList.html", {"stocks": stocks})

def edit_icestock(request, dataid):
    products = ProductDb.objects.all()  # Fetch all products for selection
    stock = get_object_or_404(IceStock, id=dataid)  # Fetch the stock entry
    return render(request, "EditIcestock.html", {'products': products, 'stock': stock})

def update_icestock(request, dataid):
    if request.method == "POST":
        print(request.POST)  # Debugging: See what data is being sent

        product_id = request.POST.get('ice_type')  # Match form field name
        
        # Ensure product_id is provided
        if not product_id:
            return render(request, "EditIceStock.html", {"error": "Product selection is required."})

        # Fetch the product safely
        product = get_object_or_404(ProductDb, id=product_id)

        # Get input values
        quantity = request.POST.get('quantity_kg')
        reorder_point = request.POST.get('reorder_point')

        # Fetch the existing IceStock entry and update it
        icestock = get_object_or_404(IceStock, id=dataid)
        icestock.ice_type = product
        icestock.quantity_kg = quantity
        icestock.reorder_point = reorder_point
        icestock.save()

        return redirect('icestock_display')

    return render(request, "EditIceStock.html", {"error": "Invalid request method."})

def delete_icestock(request, dataid):
    stock = IceStock.objects.filter(id=dataid)
    stock.delete()
    return redirect('icestock_display')  # Redirect after deletion