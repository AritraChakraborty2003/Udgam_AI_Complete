from django.contrib import admin
from home.models import UserDetails,offerDB,dailyExpense,ImageDB,Customers,VerifyDoc,loanDBs,salesDB
# Register your models here.
admin.site.register(UserDetails)
admin.site.register(offerDB)
admin.site.register(dailyExpense)
admin.site.register(ImageDB)
admin.site.register(Customers)
admin.site.register(VerifyDoc)
admin.site.register(loanDBs)
admin.site.register(salesDB)