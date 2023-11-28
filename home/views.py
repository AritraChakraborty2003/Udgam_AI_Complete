from django.shortcuts import render
from django.contrib.auth.models import User
from skimage.metrics import structural_similarity
import os
import imutils
from django.conf import settings
import cv2
from PIL import Image
import requests
from django.shortcuts import redirect,HttpResponse
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout as logouts
from django.contrib.auth.decorators import login_required
from joblib import load
from home.models import UserDetails,offerDB,dailyExpense,Customers,VerifyDoc,loanDBs,salesDB
from home.models import ImageDB
from .forms import ImageForm
from django.contrib import messages
# Create your views here.
model=load('./savemodels/loanApproval.joblib')
offers_model=load('./savemodels/offersPredict.joblib')
cust_model=load('./savemodels/customer_segmentation_model.joblib')
invest_model=load('./savemodels/Investment_Decision.joblib')
sales_model=load('./savemodels/marketcampaign.joblib')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
    return render(request,"index.html")
def signupConsumer(request):
      if request.method=="POST":
        uname=request.POST.get("uname")
        email=request.POST.get("email")
        password=request.POST.get("password")
        age=request.POST.get("age")
        Client_id=request.POST.get("Client_id")
        dependents=request.POST.get("dependents")
        monthly_income=request.POST.get("salary")
        CIBIL_Score=request.POST.get("cibil")
        married=request.POST.get("married")
        credit_History=request.POST.get("credit")
        savings=request.POST.get("savings")
        print(age,dependents,monthly_income,CIBIL_Score,married,credit_History,savings)
        user=User.objects.create_user(uname,email,password)
        customer=Customers(name=uname,age=age,dependents=dependents,salary=monthly_income,cibil=CIBIL_Score,married=married,credit_history=credit_History,savings=savings)
        verdoc=VerifyDoc(name=uname,client_id=Client_id,verified="no")
        verdoc.save()
        customer.save()
        user.save()

        return redirect("/docVerify")
    
      return render(request,"signupConsumer.html")
@login_required(login_url="/loginConsumer")
def dashboard(request):
    return render(request,"dashboard.html")
def loginConsumer(request):
    if request.method=="POST":
        uname=request.POST.get("uname")
        password=request.POST.get("password")
        user=authenticate(request,username=uname,password=password)
        choice_dict={'yes':1,"no":2}
        cust=Customers.objects.filter(name=uname).values_list("name","age","dependents","salary","cibil","married","credit_history","savings")
        print(cust)
        age=cust[0][1]
        dependents=cust[0][2]
        salary=cust[0][3]
        cibil=cust[0][4]
        married=choice_dict[cust[0][5]]
        credit_history=choice_dict[cust[0][6]] 
        savings=cust[0][7]
        type=cust_model.predict([[age,dependents,salary,cibil,married,credit_history,savings]])
        print(type)
        data=UserDetails.objects.filter(name=uname).values_list("name","Client_Id","gender")
        if type[0]==0:
           cust_cat="Traditional"
           cust_symbol="I1"
        else:
             cust_cat="Risky"
             cust_symbol="I2"
        if(data[0][0]=="Shruti Patel"):
            name_val=2
        elif(data[0][0]=="Aman Verma"):
           name_val=0
        elif(data[0][0]=="Rakesh Singh"):
           name_val=1

        if(data[0][1]=="Female"):
            sex_val=0
        else:
            sex_val=1
        client_id=int(data[0][1])
        #print(client_id)
        y_pred=offers_model.predict([[name_val,sex_val,client_id]])     
        #print(y_pred)
        expense_data=dailyExpense.objects.filter(Client_Id=client_id).values_list("payment_date","amount")
        print(expense_data)
        payment_hist_date=[]
        amount_hist=[]
        for x in expense_data:
           date=x[0].strftime("%d")
           month=x[0].strftime("%m")
           year=x[0].strftime("%Y")
           curr_date=date+"/"+month+"/"+year
           payment_hist_date.append(curr_date)
           amount_hist.append(x[1])
        pred_category={0:"Food",1:"Gaming",2:"Cosmetics"}
        val=pred_category[y_pred[0]]
        offers_data=offerDB.objects.filter(code=y_pred[0]).all()
  
        if user is not None:
            login(request,user)
            return render(request,"dashboard.html",{"offers":val,"data":offers_data,"payment_date":payment_hist_date,"amount_history":amount_hist,"cust_type":type[0],"cust_cat":cust_cat,"cust_symbol":cust_symbol})
        else:
            return HttpResponse("Invalid username or password")
    return render(request,"loginConsumer.html")
    
def payment(request):
    return render(request,"payment.html")
def Loan(request):
    if request.method=="POST":

      dependents=request.POST.get("dependents")
      Education=request.POST.get("Education")
      employed=request.POST.get("employed")
      income=request.POST.get("income")
      loan=request.POST.get("loan")
      term=request.POST.get("term")
      cibil_score=request.POST.get("cibil")
      commercial=request.POST.get("commercial")
      resedentail=request.POST.get("resedential")
      luxury=request.POST.get("luxury")
      bank=request.POST.get("bank")
      designation=request.POST.get("designation")
      if(Education=="Graduate"):
        edu_val=1
      else:
        edu_val=0
      if(employed=="yes"):
        employed_val=1
      else: 
        employed_val=0
      y_pred=model.predict([[dependents,edu_val,employed_val,income,loan,term,cibil_score,commercial,resedentail,luxury,bank]])
      print(Education)
      if y_pred[0]==1:
         val="Approved"
         color="green"
       
         loan=loanDBs(name=request.user.username,dependents=dependents,selfEmployed=employed,salary=income,loanAmount=loan,loanTerm=term,cibilScore=cibil_score,resedentialValue=resedentail,commercialValue=commercial,luxuryValue=luxury,bankAssets=bank,designation=designation,verified="no")
         loan.save()
      else:
         val="Rejected"
         color="red"
      return render(request,"LoanApproval.html",{'value':val,'color':color})
    return render(request,"LoanApproval.html")
def logout(request):
     logouts(request)
     return redirect("/")
def docVerify(request):
     form=ImageForm(request.POST,request.FILES)
     if form.is_valid():
        messages.success(request, "Image uploaded successfully...")
        form.save()
        return redirect("/verification")
     form=ImageForm()
     return render(request,"doc_verification.html",{'form':form})   
def verification(request):
   original=Image.open(settings.MEDIA_ROOT+"original.png")
   image=ImageDB.objects.all()
   img_val=""
   n=len(image)
   x=image[n-1]
   img_val=x.photo.url[6:]
   entered_image=Image.open(settings.MEDIA_ROOT+img_val)
   original=cv2.imread(settings.MEDIA_ROOT+"original.png")
   tampered=cv2.imread(settings.MEDIA_ROOT+img_val)
   original_grayscale=cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
   tampered_grayscale=cv2.cvtColor(tampered,cv2.COLOR_BGR2GRAY)
   (score,diff) = structural_similarity(original_grayscale,tampered_grayscale,full=True)
   diff=(diff*255).astype("uint8")
   if(score>0.5): 
      val="Document Verified Successfully"
   else:
      val="Document not Verified seems to be Tampered"  
   if request.method=="POST":
      if  score>0.5:
       client_id=request.POST.get("client_id")
       verdoc=VerifyDoc.objects.filter(client_id=client_id).update(verified="yes")
       print(verdoc)
       return redirect("/loginConsumer")
      else:
         return redirect("/docVerify")


   return render(request,"verification.html",{"value":val})
def bankSide(request):
  return render(request,"bankSide.html")
def salesLogin(request):
      if request.method=="POST":
       uname=request.POST.get("uname")
       password=request.POST.get("password")
       user=authenticate(request,username=uname,password=password)
       if user is not None:
            login(request,user)
            return redirect("/marketingCampaign")
      return render(request,"loginBank.html")
@login_required(login_url="/salesLogin")
def marketingCampaign(request):
   data=salesDB.objects.values_list("name","number","email","age","marital","education","dfault","housing","loan","contact","day","duration","campaign","pdays","previous")
   model_data=salesDB.objects.values_list("age","marital","education","dfault","housing","loan","contact","day","duration","campaign","pdays","previous")
   print(model_data)
   predict_arr=[]
   for i in model_data:
        predict_arr.append(sales_model.predict([list(i)]))
   print(predict_arr)
   high_chance_name=[]
   high_chance_email=[]
   high_chance_number=[]
   low_chance_name=[]
   low_chance_email=[]
   low_chance_number=[]
   count=0
   for i in predict_arr:
      if i==1:
         high_chance_name.append(data[count][0])
         high_chance_email.append(data[count][2])
         high_chance_number.append(data[count][1])
         count=count+1
      else:
         low_chance_name.append(data[count][0])
         low_chance_email.append(data[count][2])
         low_chance_number.append(data[count][1])
         count=count+1
   print(low_chance_name)
   return render(request,"marketingCampaign.html",{"high_chance_name":high_chance_name,"high_chance_email":high_chance_email,"high_chance_number":high_chance_number,"low_chance_name":low_chance_name,"low_chance_email":low_chance_email,"low_chance_number":low_chance_number})
def investLogin(request):
   if request.method=="POST":
       uname=request.POST.get("uname")
       password=request.POST.get("password")
       
       user=authenticate(request,username=uname,password=password)

       if user is not None:
            login(request,user)
            return redirect("/investDashboard")

   return render(request,"loginBank1.html")
@login_required(login_url="/investLogin")
def investDashboard(request):
 city_dict={"Bengaluru":0,     
"Gurgaon":1,           
"New Delhi":2,         
"India/US":3,          
"Singapore":4,         
"Kormangala":5,        
"Jaipur":6,           
"New York":7,          
"Haryana":8,
"Andheri":9,           
"Santa Monica":10,     
"Pune":11,       
"Gurugram":12,          
"Menlo Park":13,    
"Mumbai":14,            
"San Francisco":15,     
"Faridabad":16,         
"Delhi":17 , 
          }
 inv_arr={
    "Series A":0,
    "Series B":1,
    "Series C":2,
    "Series D":3,
    "Series E":4,
    "Series F":5,
    "Series G":6,
    "Series H":7,
    "Series J":8,
    "Angel":9,
    "Seed Funding":10,
    "Private Equity":11
    
}
 arr={"E-Commerce":0,                     
"Finance":1,                         
"FinTech":2,                       
"Technology":3,                    
"Automobile":4,                      
"Health and Wellness":5,            
"Transport":6,                                       
"Transportation":7,                                    
"Social Media":8,                    
"Tech":9,
"Software":10,
"SaaS":2}
 if request.method=="POST":
      vertical=request.POST.get("vertical")
      city=request.POST.get("city")
      round=request.POST.get("round")
      v=arr[vertical]
      c=city_dict[city]
      i=inv_arr[round]
      res=invest_model.predict([[v,c,i]])
      return render(request,"investDashboard.html",{"amount":res[0]/10,"currency":"USD","color":"green","unit":"Million"})

 return render(request,"investDashboard.html")
def loanLogin(request):
    uname=request.POST.get("uname")
    password=request.POST.get("password")
    user=authenticate(request,username=uname,password=password)
    data=loanDBs.objects.all()
    if user is not None:
      login(request,user)
      return render(request,"LoanDashboard.html",{"data":data})
    return render(request,"loginBank2.html")

def logoutBank(request):
     logouts(request)
     return redirect("/bankSide")