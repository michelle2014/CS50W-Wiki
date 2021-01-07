from django.shortcuts import render
from . import util
import markdown2
import random
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

class EntryForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)


def index(request):
    entries = util.list_entries()
    rand = random.choice(entries)
    return render(request, "encyclopedia/index.html", {
        "random": rand,
        "entries": entries
    })


def entry(request, title):
    entries = util.list_entries()
    rand = random.choice(entries)
    try: 
        mark_content = util.get_entry(title)
        output = markdown2.markdown(mark_content)
        return render(request, "encyclopedia/title.html", {
            "content": output,
            "random": rand,
            "title": title
        })

    except TypeError:
        return render(request, "encyclopedia/error.html", {
            "random": rand
        })

def search(request):
    # get search input from user
    search_entry = request.GET['q']
    # results = list()

    # get entries list
    entries = util.list_entries()
    rand = random.choice(entries)
    # search list
    results = []
    
    # try to search if there is such entry in entries
    if request.method == "GET":
        if search_entry in entries:
            return HttpResponseRedirect("/wiki/" + request.GET.get("q"))
        
        else: 
            for entry in entries: 
                if search_entry in entry: 
                    results.append(entry)
                    return render(request, "encyclopedia/search.html", {
                        "results": results,
                        "random": rand
                    })



def edit(request, title):
    data = {
        'title': title, 
        'content': util.get_entry(title)
    }

    original_form = EntryForm(data)
    entries = util.list_entries()
    rand = random.choice(entries)

    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=(title,)))

        else: 
                form.title = request.POST['title']
                form.content = request.POST['content']
                if not form.title: 
                    return render(request, "encyclopedia/edit.html",{
                        "no_title": "Title is required.",
                        "form": form,
                        "random": rand
                    })
                elif not form.content:
                    return render(request, "encyclopedia/edit.html",{
                        "no_title": "Content is required.",
                        "form": form,
                        "random": rand
                    })
        
    return render(request, "encyclopedia/edit.html", {
        "form": original_form,
        "random": rand
    })
    


def create(request):
    entries = util.list_entries()
    rand = random.choice(entries)

    if request.method == "POST":
        form = EntryForm(request.POST)
        title = request.POST['title']
        
        if title in entries:
            return render(request, "encyclopedia/create.html",{
                "message": "Page already exists.",
                "form": EntryForm(),
                "random": rand
            })
            
        else:
            if form.is_valid():
                title = form.cleaned_data["title"]
                content = form.cleaned_data["content"]
                
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", args=(title,)))

            else: 
                title = request.POST['title']
                content = request.POST['content']
                if not title: 
                    return render(request, "encyclopedia/create.html",{
                        "no_title": "Title is required.",
                        "form": EntryForm(),
                        "random": rand
                    })
                elif not content:
                    return render(request, "encyclopedia/create.html",{
                        "no_title": "Content is required.",
                        "form": EntryForm(),
                        "random": rand
                    })
    

    return render(request, "encyclopedia/create.html",{
        "form": EntryForm(),
        "random": rand
    })

  

