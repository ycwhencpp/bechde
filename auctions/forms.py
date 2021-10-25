
from django import forms
from .models import auction_listing,bids,comments


# class create_form(forms.Form):
#     title=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control title","placeholder":"Enter the title","autocomplete":"off"}))
#     tag=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control title","placeholder":"Cateogry","autocomplete":"on"}))
#     description=forms.CharField(widget=forms.Textarea(attrs={"class":"form-control content","placeholder":"Item Description","autocomplete":"off"}))
#     amount=forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={"class":"form-control title","placeholder":"Bid Amount","autocomplete":"off"}))
#     url=forms.URLField(widget=forms.URLInput(attrs={"class":"form-control title","placeholder":"Image URL","autocomplete":"off"}))
#     image=forms.FileField(required=False,widget=forms.FileInput(attrs={"class":"form-control title"}))



class listing_form(forms.ModelForm):

    choice=[
        ("Art","Art"),
        ("Books","Books"),
        ("Clothing","Clothing"),
        ("Electronics","Electronics"),
        ("Health and Beauty","Health and Beauty"),
        ("Homeware","Homeware"),
        ("Music","Music"),
        ("Other","Other"),
        ("Shoe and Trainer","Shoe and Trainer"),
    
    ]
    Tag=forms.ChoiceField(choices=choice,initial="Other")

    Tag.widget.attrs.update({"class":"form-select"})
    
    class Meta:
        model=auction_listing
        fields=["Title","Description","Url","Tag","starting_bid"]
         

        widgets = {
            "Title":forms.TextInput(attrs={"class":"form-control title","placeholder":"Enter the title","autocomplete":"off"}),
            "Description":forms.Textarea(attrs={"class":"form-control content","placeholder":"Item Description","autocomplete":"off","maxlength":1000,"rows":7}),
            "Url":forms.URLInput(attrs={"class":"form-control title","placeholder":"Image URL","autocomplete":"off"}),
            "starting_bid":forms.NumberInput(attrs={"class":"form-control title","placeholder":"Bid amount","autocomplete":"off"})
        }

        labels={
            "Url":"Image URL",
            "Tag":"Category",
            "starting_bid":"Amount",
        }
        
       


        

class comment_form(forms.ModelForm):


    class Meta:
        model=comments
        fields=["comment"]


        widgets={
            "comment":forms.Textarea(attrs={"class":"form-control content","placeholder":"Your comment","autocomplete":"off","maxlength":200,"rows":2}),
        }

        labels={
            "comment":""
        }


class bid_form(forms.ModelForm):

    class Meta:

        model=bids

        fields=["amount"]

        widgets={
            "amount":forms.NumberInput(attrs={"class":"form-control title","placeholder":"Bid amount","autocomplete":"off","min":0})
        }

        labels={
            "amount":""
        }



