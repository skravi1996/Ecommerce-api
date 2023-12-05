from django.shortcuts import render
from .models import Customer,Product,Order,OrderItem
from .serializers import CustomerSerializer,ProductSerializer,OrderSerializer,OrderItemSerializer
from rest_framework import generics


# Create your views here.

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def get_queryset(self):
        product_names = self.request.query_params.get('products', '').split(',')
        customer_name = self.request.query_params.get('customer', '')
        print(customer_name)
        if product_names[0] !='' :
            return Order.objects.filter(order_items__product__name__in=product_names).distinct().order_by('-id')
        elif customer_name:
            return Order.objects.filter(customer__name=customer_name).distinct()
        return Order.objects.all().order_by('-id')
        
        # If product names are provided, filter orders based on products
        
        
    #def perform_create(self, serializer):
    #    # Automatically generate order number with prefix 'ORD'
    #    serializer.save(order_number=f'ORD{Order.objects.count() + 1:05d}')
    

class OrderRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class =  OrderSerializer

"""class OrderListByProductView(generics.ListAPIView):
    serializer_class = OrderSerializer"""