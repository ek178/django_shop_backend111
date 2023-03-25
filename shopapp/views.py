from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .models import Product, Department,Order1,OrderProduct,Review,DeliveryDetail,Profile
from .serializers import ReviewSerializer, ProductSerializer,DeliveryDetailSerializer,UserSerializer,ProfileSerializer, DepartmentSerializer,OrderProductSerializer,Order1Serializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import mixins

def index(req):
    return JsonResponse('hello', safe=False)



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['emaillll'] = user.email
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OrderCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Order1Serializer




    
class OrderSerView(APIView):
    """
    This class handle the CRUD operations for MyModel
    """
    def get(self, request, pk):
        order = Order1.objects.get(id=pk)
        order_products = order.orderproduct_set.all()

        order_serializer = Order1Serializer(order)
        order_products_serializer = OrderProductSerializer(order_products, many=True)
        data = {
            'order': order_serializer.data,
            'order_products': order_products_serializer.data,
        }
        return Response(data)

    def post(self, request):
        serializer = Order1Serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            order_products_serializer = OrderProductSerializer(data=request.data['products'], many=True)
            if order_products_serializer.is_valid():
                order_products_serializer.save(order=order)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                order.delete()
                return Response(order_products_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    # def post(self, request):
    #     serializer = NewOrderSerializer(data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

#    class OrderCreateView(generics.CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = OrderSerializer

    # def post(self, request):
    #     print(request.data)
    #     order_serializer = OrderSerializer(data=request.data['order'])
    #     order_products_serializer = OrderProductSerializer(data=request.data['order_products'], many=True)

        
    #     if order_serializer.is_valid() and order_products_serializer.is_valid():
    #         order = order_serializer.save()
    #         order_products_serializer.save(order=order)
    #         return Response(order_serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def get(self, request, pk):
    #     order = Order1.objects.get(id=pk)
    #     order_products = OrderProduct.objects.filter(order=order)
    #     order_serializer = OrderSerializer(order)
    #     order_products_serializer = OrderProductSerializer(order_products, many=True)
    #     data = {
    #         'order': order_serializer.data,
    #         'order_products': order_products_serializer.data,
    #     }
    #     return Response(data)
    



class DeliveryView(APIView):
    """
    This class handle the CRUD operations for MyModel
    """
    def get(self, request,pk=-1):
        """
        Handle GET requests to return a list of MyModel objects
        """
        if (pk > -1):
            my_model = DeliveryDetail.objects.get(id=pk)
            serializer = DeliveryDetailSerializer(my_model)
        else:
            my_model = DeliveryDetail.objects.all()
            serializer = DeliveryDetailSerializer(my_model, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Handle POST requests to create a new Task object
        """
        serializer = DeliveryDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        """
        Handle PUT requests to update an existing Task object
        """
        my_model = DeliveryDetail.objects.get(pk=pk)
        serializer = DeliveryDetailSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Handle DELETE requests to delete a Task object
        """
        my_model = DeliveryDetail.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ReviewView(APIView):
    """
    This class handle the CRUD operations for Review model
    """
    def get(self, request, pk):
        """
        Handle GET requests to return a list of Review objects related to a Product
        """
        reviews = Review.objects.filter(item=pk)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Handle POST requests to create a new Task object
        """
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        """
        Handle PUT requests to update an existing Task object
        """
        my_model = Review.objects.get(pk=pk)
        serializer = ReviewSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Handle DELETE requests to delete a Task object
        """
        my_model = Review.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryView(APIView):
    """
    This class handle the CRUD operations for MyModel
    """
    def get(self, request,pk=-1):
        """
        Handle GET requests to return a list of MyModel objects
        """
        if (pk > -1):
            my_model = Department.objects.get(id=pk)
            serializer = DepartmentSerializer(my_model)
        else:
            my_model = Department.objects.all()
            serializer = DepartmentSerializer(my_model, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        """
        Handle PUT requests to update an existing Task object
        """
        my_model = Department.objects.get(pk=pk)
        serializer = DepartmentSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Handle DELETE requests to delete a Task object
        """
        my_model = Department.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductView(APIView):
    """
    This class handle the CRUD operations for MyModel
    """
    def get(self, request,pk=-1):
        """
        Handle GET requests to return a list of MyModel objects
        """
        if (pk > -1):
            my_model = Product.objects.filter(id=pk) #category
            serializer = ProductSerializer(my_model, many=True)
        else:
            my_model = Product.objects.all()
            serializer = ProductSerializer(my_model, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Handle POST requests to create a new Task object
        """

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        """
        Handle PUT requests to update an existing Task object
        """
        my_model = Product.objects.get(pk=pk)
        serializer = ProductSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Handle DELETE requests to delete a Task object
        """
        my_model = Product.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# class OrderView(APIView):

#     def get(self, request, pk=-1):
#         if request.user.profile:
#             if pk > -1:
#                 my_model = Order1.objects.get(id=pk)
#                 serializer = OrderSerializer(my_model)
#             else: 
#                 profile = request.user.profile
#                 my_model = Order1.objects.filter(buyer=profile)
#                 serializer = OrderSerializer(my_model, many=True)
#             return Response(serializer.data)
    
#     def post(self, request):

#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def put(self, request, pk):

#         my_model = Order1.objects.get(pk=pk)
#         serializer = OrderSerializer(my_model, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):

#         my_model = Order1.objects.get(pk=pk)
#         my_model.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        
# class OrderStaff(APIView):
#     def get(self, request, pk=-1):
#         if pk > -1:
#             my_model = Order1.objects.get(id=pk)
#             serializer = OrderSerializer(my_model)
#         else:
#             my_model = Order1.objects.all()
#             serializer = OrderSerializer(my_model, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):

#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def put(self, request, pk):

#         my_model = Order1.objects.get(pk=pk)
#         serializer = OrderSerializer(my_model, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):

#         my_model = Order1.objects.get(pk=pk)
#         my_model.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(APIView):

    def get(self, request, pk=-1):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request, pk):
        my_model = Profile.objects.get(pk=pk)
        serializer = ProfileSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        my_model = Profile.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileStaff(APIView):
    
    def get(self, request, pk=-1):
        if pk > -1:
            my_model = Profile.objects.get(id=pk)
            serializer = ProfileSerializer(my_model)
        else:
            my_model = Profile.objects.all()
            serializer = ProfileSerializer(my_model, many=True)
        return Response(serializer.data)
    
    def put(self, request, pk):
        my_model = Profile.objects.get(pk=pk)
        serializer = ProfileSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        my_model = Profile.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
