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


    path("orders/", views.OrderListView.as_view(), name="order_list"),
    path("orders/update/<int:order_id>/", views.UpdateOrderStatusView.as_view(), name="update_order_status"),
    path("orders/delete/<int:order_id>/", views.DeleteOrderView.as_view(), name="delete_order"),

     path("contact-details/", views.contact_details, name="contact_details"),
    

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
