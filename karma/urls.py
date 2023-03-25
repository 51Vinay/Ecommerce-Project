"""karma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='home'),
    path('login/', views.loginPage,name='login'),
    path('logout/', views.logout,name='logout'),
    path('contact/', views.contactPage,name='contact'),
    path('cart/', views.cart),
    path('checkout/', views.checkOutPage,name='checkout'),
    path('product/<int:num>/', views.productDetails),
    path('shop/<str:mc>/<str:sc>/<str:br>/', views.shopPage),
    path('signup/', views.signup,name='signup'),
    path('profile/', views.profile,name='profile'),
    path('sellerprofile/', views.sellerProfile),
    path('editsellerprofile/', views.editSellerProfile),
    path('buyerprofile/', views.buyerProfile),
    path('editbuyerprofile/', views.editBuyerProfile),
    path('addproduct/', views.addProduct),
    path('editproduct/<int:num>/', views.editProduct),
    path('deleteproduct/<int:num>/', views.deleteProduct),
    path('wishlist/<int:num>/', views.wishlistPage),
    path('deletewishlist/<int:num>/', views.deletewishlist),
    path('forgotpassword/',views.changepass,name='pass'),
    path('payment/',views.payment,name='payment'),
    path('enterotp/',views.enterOtp),
    path('resetpassword/',views.resetPassword),
    
    # path('paymentsuccess/<str:rppid>/<str:rpoid>/<str:rpsid>',views.paymentSuccess),
    # path('paymentfail/',views.paymentFail)
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
