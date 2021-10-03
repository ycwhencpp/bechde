from django.contrib import admin


from .models import User,auction_listing,comments,bids
# Register your models here.


# class listingadmin(admin.ModelAdmin):
#     list_display=('id','Title','Description','Tag','Url','user','date_time')



admin.site.register(User)
admin.site.register(auction_listing)
admin.site.register(comments)
admin.site.register(bids)
# admin.site.register(User)