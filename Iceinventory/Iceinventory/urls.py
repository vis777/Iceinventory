"""
URL configuration for Iceinventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Shopapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Iceapp/', include("Iceapp.urls")),
    path("", views.indexpage, name="indexpage"),


    path("adminindexpage/", views.adminindexpage, name="adminindexpage"),
    path('admin_login/', views.admin_login, name="admin_login"),
    path('adminlogin/', views.adminlogin, name="adminlogin"),
    path('admin_logout/', views.admin_logout, name="admin_logout"),

    path('indexpage/', views.indexpage, name="indexpage"),
    path('categorypage/', views.categorypage, name="categorypage"),
    path('savecategory/', views.savecategory, name="savecategory"),
    path('category_display/', views.category_display, name='category_display'),
    path('editcategory/<int:dataid>/', views.editcategory, name='editcategory'),
    path('updatecategory/<int:dataid>/', views.updatecategory, name='updatecategory'),
    path('deletecategory/<int:dataid>/', views.deletecategory, name='deletecategory'),

    path('productpage/', views.productpage, name="productpage"),
    path('saveproduct/', views.saveproduct, name="saveproduct"),
    path('product_display/', views.product_display, name='product_display'),
    path('editproduct/<int:dataid>/', views.editproduct, name='editproduct'),
    path('updateproduct/<int:dataid>/', views.updateproduct, name='updateproduct'),
    path('deleteproduct/<int:dataid>/', views.deleteproduct, name='deleteproduct'),

    path("addicestock/", views.add_icestock, name="add_icestock"),
    path("saveicestock/", views.save_icestock, name="save_icestock"),
    path("icestock/", views.icestock_display, name="icestock_display"),
    path('edit_icestock/<int:dataid>/', views.edit_icestock, name='edit_icestock'),
    path('update_icestock/<int:dataid>/', views.update_icestock, name='update_icestock'),
    path('delete_icestock/<int:dataid>/', views.delete_icestock, name='delete_icestock'),
    

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
