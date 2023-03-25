from rest_framework import serializers
from .models import Product , Department, DeliveryDetail, Order1,OrderProduct,Review,Profile
from django.contrib.auth.models import User


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department 
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    d_name = serializers.ReadOnlyField(source='p_type.d_name')
    d_desc = serializers.ReadOnlyField(source='p_type.d_desc')


    class Meta:

        model = Product 
        fields = ['p_name','p_created','id', 'p_desc', 'p_price', 'p_type', 'p_amount', 'p_image','d_name','d_desc']

    def create(self, validated_data):
        product = Product.objects.create(**validated_data) 
        return product


class ProfileSerializer(serializers.ModelSerializer):

    items = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all(), required=False)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        fields = '__all__'
        model = Profile 

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        items_data = profile_data.pop('items', [])
        profile = Profile.objects.create(user=user, **profile_data)
        for item_data in items_data:
            profile.items.add(item_data)
        return user

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


# class OrderProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderProduct
#         fields = ['id', 'product']
#         depth = 1
        
class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True,
    )

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'product_id', 'amount_selected']



# class OrderProductSerializer(serializers.ModelSerializer):
#     # product_id = serializers.PrimaryKeyRelatedField(source='product', queryset=Product.objects.all())
#     # order_id = serializers.PrimaryKeyRelatedField(source='order', queryset=Order1.objects.all(), many=False)

#     class Meta:
#         model = OrderProduct
#         fields = ['product_id', 'order_id', 'amount_selected']

#     def create(self, validated_data):
#         product_id = validated_data.pop('product_id')
#         order_id = validated_data.pop('order_id')
#         amount_selected = validated_data.pop('amount_selected')
#         order_product = OrderProduct.objects.create(product_id=product_id, order_id=order_id, amount_selected=amount_selected)
#         return order_product

# class OrderProductSerializer(serializers.ModelSerializer):
#     # product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

#     product_id = serializers.PrimaryKeyRelatedField(source='product', queryset=Product.objects.all())
#     order_id = serializers.PrimaryKeyRelatedField(source='order', queryset=Order1.objects.all(), many=False)

#     class Meta:
#         model = OrderProduct
#         fields = ['product_id', 'order_id', 'amount_selected'] 


class DeliveryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryDetail
        fields = '__all__'


class Order1Serializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)

    class Meta:
        model = Order1
        fields = ['id', 'buyer', 'delivery_details', 'total_price', 'products', 'total_product_amount', 'products_amount']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order1.objects.create(**validated_data)
        for product_data in products_data:
            OrderProduct.objects.create(order=order, **product_data)
        return order





















# class OrderSerializer(serializers.ModelSerializer):

#     name = serializers.ReadOnlyField(source='buyer.name')
#     email = serializers.ReadOnlyField(source='buyer.email')
#     p_name = serializers.ReadOnlyField(source='items.p_name')
#     p_price = serializers.ReadOnlyField(source='items.p_price')
#     p_amount = serializers.SerializerMethodField()
#     delivery_details = DeliveryDetailSerializer()

#     class Meta:
#         model = Order1
#         fields = ['buyer', 'id', 'delivery_details', 'products', 'total_price',
#         'total_product_amount','o_created','name','email','p_name','p_price','p_amount']


#     def create(self, validated_data):
#         if 'products' in validated_data:
#             product_ids = validated_data.pop('products')
#             products = [Product.objects.get(pk=id) for id in product_ids]
#             # create and return the order
#         else:
#             raise serializers.ValidationError("Missing 'products' key in request data")
#         delivery_details_data = validated_data.pop('delivery_details')
#         product_ids = validated_data.pop('products')
#         p_amount = validated_data.pop('p_amount')  # get the custom field value

#         delivery_details = DeliveryDetail.objects.create(**delivery_details_data)

#         products = Product.objects.filter(id__in=product_ids)

#         total_price = sum(product.price for product in products)

#         order = Order1.objects.create(
#             delivery_details=delivery_details,
#             products_amount=p_amount,
#             total_price=total_price,
#             **validated_data
#         )
#         order.products.set(products)
#         return order
    
    
    # def create(self, validated_data):
    #     delivery_details_data = validated_data.pop('delivery_details')
    #     products_data = validated_data.pop('products')
    #     p_amount = validated_data.pop('p_amount')  # get the custom field value
        
    #     delivery_details = DeliveryDetail.objects.create(**delivery_details_data)
    #     products = [Product.objects.get(pk=product_data['id']) for product_data in products_data]
        
    #     order = Order1.objects.create(delivery_details=delivery_details, products_amount=p_amount, **validated_data)
    #     order.products.set(products)
    #     return order


    def update(self, instance, validated_data):
        delivery_details_data = validated_data.pop('delivery_details', None)
        products_data = validated_data.pop('products', None)
        p_amount = validated_data.pop('p_amount', instance.products_amount)  # get the custom field value or default to the existing value
        
        if delivery_details_data:
            delivery_details_serializer = DeliveryDetailSerializer(instance.delivery_details, data=delivery_details_data)
            if delivery_details_serializer.is_valid():
                delivery_details = delivery_details_serializer.save()
                validated_data['delivery_details'] = delivery_details
            else:
                raise serializers.ValidationError(delivery_details_serializer.errors)

        if products_data:
            products = [Product.objects.get(pk=product_data['id']) for product_data in products_data]
            instance.products.set(products)

        instance.products_amount = p_amount  # set the custom field value
        instance.save()
        return instance

    def get_p_amount(self, obj):
        return obj.products_amount



