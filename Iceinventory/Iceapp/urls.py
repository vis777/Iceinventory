from django.urls import path
from . import views

urlpatterns= [
    path('homepage/', views.homepage, name="homepage"),
    path('productspage/', views.productspage, name="productspage"),
    path('product_filter_page/<cat_name>/', views.product_filter_page, name="product_filter_page"),
    path('singleproductpage/<int:proid>/', views.singleproductpage, name="singleproductpage"),
    path('reduce_stock/<int:product_id>/', views.reduce_stock, name='reduce_stock'),
    path('contactpage/', views.contactpage, name="contactpage"),
     path("savecontact/", views.savecontact, name="savecontact"),
    path('aboutpage/', views.aboutpage, name="aboutpage"),
    path('servicepage/', views.servicepage, name="servicepage"),
    path('savecontact/', views.savecontact, name="savecontact"),
    path('savereg/', views.savereg, name="savereg"),

    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name="user_logout" ),

    path('cartpage/', views.cartpage, name="cartpage"),
    path('savecart/', views.savecart, name="savecart"),
    path('deletecart/<int:dataid>/', views.deletecart, name="deletecart"),


    path('checkoutpage/', views.checkoutpage, name="checkoutpage"),
    path('save_checkout/', views.save_checkout,name="save_checkout"),
    path('yourorder/', views.yourorder, name="yourorder"),
    path('paymentpage/', views.paymentpage, name="paymentpage"),
    path("payment_success/", views.payment_success, name="payment_success"),

    path("order-history/", views.order_history, name="order_history"),
    # path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    # path('make_payment/<int:order_id>/', views.PaymentView.as_view(), name='make_payment'),
    # path('confirm_payment/<int:order_id>/', views.ConfirmPaymentView.as_view(), name='confirm_payment'),
    # path('payment_success/<int:order_id>/', views.PaymentSuccessView.as_view(), name='payment_success'),
    # path('paymentpage/', views.paymentpage, name="paymentpage")

]