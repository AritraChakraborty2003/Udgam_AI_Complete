from django.db import models


class ImageDB(models.Model):
   photo=models.FileField(upload_to="media",max_length=250,null=True,default=None)
# Create your models here.
class UserDetails(models.Model):
    name=models.TextField()
    Client_Id=models.TextField()
    gender=models.TextField()

class offerDB(models.Model):
    code=models.IntegerField()
    brand=models.TextField()
    domain=models.TextField()
    discount=models.TextField()
    logo=models.ImageField()

class Customers(models.Model):
   name=models.TextField()
   age=models.IntegerField()
   dependents=models.IntegerField()
   salary=models.IntegerField()
   cibil=models.IntegerField()
   married=models.TextField()
   credit_history=models.TextField()
   savings=models.IntegerField()

class dailyExpense(models.Model):
  name=models.TextField()
  Client_Id=models.TextField()
  brand=models.TextField()
  domain=models.TextField()
  payment_date=models.DateField()
  amount=models.IntegerField()


class VerifyDoc(models.Model):
   client_id=models.TextField()
   name=models.TextField()
   verified=models.TextField()

class loanDBs(models.Model):
   name=models.TextField()
   dependents=models.IntegerField()
   selfEmployed=models.TextField()
   salary=models.IntegerField()
   loanAmount=models.IntegerField()
   loanTerm=models.IntegerField()
   cibilScore=models.IntegerField()
   resedentialValue=models.IntegerField()
   commercialValue=models.IntegerField()
   luxuryValue=models.IntegerField()
   bankAssets=models.IntegerField()
   designation=models.TextField()
   verified=models.TextField()

class salesDB(models.Model):
   name=models.TextField()
   number=models.TextField()
   email=models.TextField()
   age=models.IntegerField()
   marital=models.IntegerField()
   education=models.IntegerField()
   dfault=models.IntegerField()
   housing=models.IntegerField()
   loan=models.IntegerField()
   contact=models.IntegerField()
   day=models.IntegerField()
   duration=models.IntegerField()
   campaign=models.IntegerField()
   pdays=models.IntegerField()
   previous=models.IntegerField()
    

