from django.urls import path
from .import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import signup_view, CustomLoginView, product_list, cart_view

urlpatterns = [
    path('', views.product_list, name='product_list'),        # Homepage showing products
    path('login/', LoginView.as_view(template_name='store/login.html'), name='login'),  # Login page
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),        
    path('signup/', signup_view, name='signup'), 
    path('cart/', cart_view, name='cart'),  # Cart page 
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('cart/increase/<int:product_id>/', views.increment_quantity, name='increment_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrement_quantity, name='decrement_quantity'),
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),



]

