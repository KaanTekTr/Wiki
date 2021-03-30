from django.shortcuts import render
#from django import forms
import markdown2
from . import util
from django.http import HttpResponseRedirect
import random


#class NewEntryForm(forms.Form):
    #title = forms.CharField()
    #content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols':5}))



def index(request):
    if request.method == "POST":
        input = request.POST.get("q")

        if input in util.list_entries():
            item_info = markdown2.markdown(util.get_entry(input))
            return render(request, "encyclopedia/item.html", {
                "item" : input,
                "item_info" : item_info
        })
        filtered_list = []
        flag = False
        for entry in util.list_entries():
            if input in entry:
                flag = True
                filtered_list.append(entry)
        if flag:
            return render(request, "encyclopedia/search.html", {
                "filtered_list" : filtered_list
            })

        return render(request, "encyclopedia/error.html", {
            "item_name" : input
        })



    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view_item(request, item_name):

    if item_name in util.list_entries():
        item_info = markdown2.markdown(util.get_entry(item_name))
        return render(request, "encyclopedia/item.html", {
            "item_name" : item_name,
            "item_info" : item_info
        })
    elif item_name == "random":
        item = random.choice(util.list_entries())
        item_info = markdown2.markdown(util.get_entry(item))
        return render(request, "encyclopedia/random_page.html", {
            "item" : item,
            "item_info" : item_info
    })
    else:
        return render(request,"encyclopedia/error.html", {
            "item_name" : item_name
        })

def new(request):
    if request.method == "POST":
        name = request.POST.get("title")
        content = request.POST.get("content")
        if name not in util.list_entries():
            util.save_entry(name, content)
            return HttpResponseRedirect(f"/wiki/{name}")

        else:
            return render(request,"encyclopedia/error2.html", {
            "name" : name
        })
    return render(request, "encyclopedia/new.html")

def edit(request, item_name):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(item_name, content)
        return HttpResponseRedirect(f"/wiki/{item_name}")

    return render(request, "encyclopedia/edit.html", {
        "item_name" : item_name,
        "item_content" : util.get_entry(item_name)
    })


