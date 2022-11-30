from rest_framework import serializers
from .models import Category,Product,Order,OrderItem

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = (
			'id',
			'name',
			'get_absolute_url',
			'description',
			'price',
			'get_image',
			'get_thumbnail'
			)

class CategorySerializer(serializers.ModelSerializer):
	products = serializers.SerializerMethodField()

	def get_products(self,obj):
		prods = Product.objects.filter(category=obj)
		return ProductSerializer(prods,many=True).data

	class Meta:
		model = Category
		fields = (
			'id',
			'name',
			'slug',
			'get_absolute_url',
			'products'
		)

class MyOrderItemSerializer(serializers.ModelSerializer):    
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",
        )

class MyOrderSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "zipcode",
            "phone",
            "items",
            "paid_amount"
        )

class OrderItemSerializer(serializers.ModelSerializer):    
    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",
        )

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "zipcode",
            "phone",
            "items",
        )
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            
        return order