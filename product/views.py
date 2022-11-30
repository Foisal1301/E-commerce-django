from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer,CategorySerializer,OrderSerializer, MyOrderSerializer
from .models import Product,Category,Order, OrderItem
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes

class LatestProductList(APIView):
	def get(self,request,format=None):
		products = Product.objects.all()[:4]
		serializer = ProductSerializer(products,many=True)
		return Response(serializer.data)

class ProductDetail(APIView):
	def get_object(self,category_slug,product_slug):
		try:
			return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
		except Product.DoesNotExist:
			return False

	def get(self,request,category_slug,product_slug,format=None):
		product = self.get_object(category_slug,product_slug)
		if product:
			serializer = ProductSerializer(product)
			return Response(serializer.data)
		return Response({})

class CategoryDetail(APIView):
	def get_object(self,category_slug):
		try:
			return Category.objects.get(slug=category_slug)
		except Category.DoesNotExist:
			return False

	def get(self,request,category_slug,format=None):
		product = self.get_object(category_slug,)
		if product:
			serializer = CategorySerializer(product)
			return Response(serializer.data)
		return Response({})

@api_view(['POST'])
def search(request):
	query = request.data.get('query','')

	if query:
		products = Product.objects.filter(Q(name__icontains=query)|Q(description__icontains=query))
		serializer = ProductSerializer(products,many=True)
		return Response(serializer.data)
	else:
		return Response({"products":[]})

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
	serializer = OrderSerializer(data=request.data)

	if serializer.is_valid():
		paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])
		serializer.save(user=request.user,paid_amount=paid_amount)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrdersList(APIView):
	authentication_classes = [authentication.TokenAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	def get(self,request,format=None):
		orders = Order.objects.filter(user=request.user)
		serializer = MyOrderSerializer(orders,many=True)
		return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_username(request):
	return Response({
		'username':request.user.username
	})