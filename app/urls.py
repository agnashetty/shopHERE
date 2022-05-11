from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import Login, changepassword


urlpatterns = [
    path('', views.home.as_view(), name= "home"),
    path('product-detail/<int:pk>', views.ProductDetail.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cartpage/', views.cartpage, name='cartpage'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', auth_view.PasswordChangeView.as_view(template_name = 'app/changepassword.html', form_class = changepassword, success_url = '/passwordchangesuccess/'), name='changepassword'),
    path('passwordchangesuccess/', auth_view.PasswordChangeDoneView.as_view(template_name = 'app/passwordchangesuccess.html'), name = 'passwordchangesuccess' ),
    path('mobile/', views.mobile, name='mobile'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name = 'app/login.html', authentication_form = Login), name='login'),
    path('logout/', auth_view.LogoutView.as_view(next_page = 'login') , name = 'logout'),
    path('signup/', views.signup, name='signup'),
    path('pluscart/', views.pluscart, name='pluscart'),
    path('minuscart/', views.minuscart, name='minuscart'),
    path('removeproduct/', views.removeproduct, name='remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.paymentdone, name='paymentdone'),
    path('laptop/', views.laptop, name='laptop'),
    path('traditional/', views.traditional, name='traditional'),
    path('western/', views.western, name='western'),
    

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
