from rest_framework import serializers
from django.utils import timezone
from .models import Customer, Product, Order, OrderItem

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product','quantity')

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)  

    class Meta:
        model = Order
        fields = ('id', 'customer', 'order_date', 'address', 'order_items')
        extra_kwargs = {
            'order_number': {'required': False},
        }

    def validate_order_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Order date cannot be in the past.")
        return value
    def validate_order_items(self, order_items):
        total_weight = 0

        for order_item in order_items:
            product = order_item['product']
            quantity = order_item['quantity']
            total_weight += product.weight * quantity

        if total_weight > 150:
            raise serializers.ValidationError("Cumulative weight of products in the order cannot exceed 150kg.")

        return order_items

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items') 
        print(order_items_data)
        order = Order.objects.create(**validated_data)

        for order_item_data in order_items_data:
            product_data = order_item_data.pop('product')
            product = Product.objects.get(pk=product_data.id)
            OrderItem.objects.create(order=order, product=product, **order_item_data)

        return order
    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items')
        print(order_items_data)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        instance.order_items.all().delete()
        # Create new order items
        for order_item_data in order_items_data:
            product_data = order_item_data.pop('product')
            product = Product.objects.get(pk=product_data.id)
            OrderItem.objects.create(order=instance, product=product, **order_item_data)

        return instance
