from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Owner(models.Model):
    GENDER = (
        (1,'Male'),
        (2,'female'),
    )
    
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    username = models.CharField(max_length=10)
    email = models.EmailField()
    gender = models.IntegerField(choices=GENDER)
    phone_no = models.IntegerField()
    code = models.IntegerField()
    address = models.IntegerField()
    county = models.CharField(max_length=20)
    town = models.CharField(max_length=20)

    def __str__(self) -> str:
        return str(self.first_name)

       
class Income(models.Model):
    owner = models.ForeignKey(Owner,on_delete=models.CASCADE,blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=30)
    planned_amount = models.IntegerField()
    actual_amount = models.IntegerField()

    def __str__(self) -> str:
        return str(self.owner)


class Debt(models.Model):
    owner = models.ForeignKey(Owner,on_delete=models.CASCADE,blank=True,null=True)
    paid_to = models.CharField(max_length=30)
    planned_amount = models.IntegerField()
    actual_amount = models.IntegerField()

    def __str__(self) -> str:
        return str(self.owner) + str(self.actual_amount)

class Expenses(models.Model):

    CATEGORIES = [
        (1,'HouseHold'),
        (2,'Food'),
        (3,'Transportation'),
        (4,'Personal'),
        (5,'Subscriptions'),
        (6,'Savings'),
        (7,'Medical'),
    ]
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Owner,on_delete=models.CASCADE,blank=True,null=True)
    name_of_expense = models.CharField(max_length=10)
    category = models.IntegerField(choices=CATEGORIES)  
    planned_amount = models.IntegerField()
    actual_amount = models.IntegerField()

    def __str__(self):
        return self.get_category_display()

class UserProfile(models.Model):
    owner = models.OneToOneField(Owner,on_delete=models.CASCADE,blank=True,null=True)
    image = models.ImageField(upload_to='media',default='default.png',blank=True,null=True)

    def __str__(self) -> str:
        return self.owner.username + ' profile pic'

class EmailConfirmation(models.Model):
    owner = models.OneToOneField(Owner,on_delete=models.CASCADE,blank=True,null=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.owner.username + str(self.email_confirmed)