from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User


class Department(models.Model):
    d_name = models.CharField(max_length=50, unique=True)
    d_desc = models.CharField(max_length=1000, blank=True)
    d_image = models.ImageField(upload_to='static/images',default='/static/images/lion-fish.jpg')
    d_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.d_name

    class Meta:
        db_table = 'Department'

class Product(models.Model):
    p_name = models.CharField(max_length=50, unique=True)
    p_desc = models.CharField(max_length=1000, blank=True)
    p_price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)])
    p_type = models.ForeignKey(Department, on_delete=models.CASCADE)
    p_amount= models.PositiveIntegerField()
    p_image = models.ImageField(upload_to='static/images',default='/static/images/lion-fish.jpg')
    p_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.p_name
    
    class Meta:
        db_table = 'Product'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30) 
    email = models.EmailField(unique=True)
    items = models.ManyToManyField(Product,blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    profile_created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Profile'


class Review(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    review= models.CharField(max_length=1000, blank=True,null=True)
    rating = models.PositiveSmallIntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    r_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.item}  {self.rating}'
    
    class Meta:
        db_table = 'Review'


class DeliveryDetail(models.Model):
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=30)
    house=models.CharField(max_length=10)
    zip = models.CharField(max_length=16,null=True,blank=True)
    phone = models.CharField(max_length=30)
    special_notes=models.CharField(max_length=100,blank=True,null=True)
    dd_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} Delivery Detail'

    class Meta:
        db_table = 'Delivery Detail'


class Order1(models.Model):
    buyer = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True)
    delivery_details = models.ForeignKey(DeliveryDetail, on_delete=models.SET_NULL,null=True)
    total_price = models.DecimalField(max_digits=12,decimal_places=2, validators=[MinValueValidator(0)])
    products = models.ManyToManyField(Product, through="OrderProduct",related_name="orders")
    total_product_amount = models.PositiveIntegerField(default=0)
    products_amount = models.PositiveIntegerField(default=0)    
    o_created = models.DateField(auto_now_add=True)


    def __str__(self):
        return f'{self.buyer} Order'
    
    class Meta:
        db_table = 'Orders1'



class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order1, on_delete=models.CASCADE)
    amount_selected = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f'{self.product} in {self.order}'
    
    class Meta:
        unique_together = ('product', 'order')

# products_price=models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)]) 
