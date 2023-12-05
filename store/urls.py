from django.urls import path
from.views import CustomerListCreateView,CustomerRetrieveUpdateView,ProductListCreateView,OrderListCreateView,OrderRetrieveUpdateView



urlpatterns = [
    path('customers/',CustomerListCreateView.as_view(),name='cust-create-list-view'),
    path('customers/<int:pk>/',CustomerRetrieveUpdateView.as_view()),
    path('products/',ProductListCreateView.as_view()),
    path('orders/',OrderListCreateView.as_view()),
    path('orders/<int:pk>/', OrderRetrieveUpdateView.as_view()),
    
]