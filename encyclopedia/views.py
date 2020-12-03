from django.shortcuts import render
from django.template.defaulttags import register
from . import util
from django import forms
from markdown2 import Markdown
import random

markdown_page = Markdown()

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs = {
        'placeholder': 'Search'
    }))

class Write(forms.Form):
    title = forms.CharField(label = "Title")
    textarea = forms.CharField(widget = forms.Textarea(), label = '')

class Edit(forms.Form):
    textarea = forms.CharField(widget = forms.Textarea(), label = '')

def index(request):
    entries = util.list_entries()
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            found_pages = []
            for entry in entries:
                if item in entries:
                    page = util.get_entry(item)
                    HTML_page = markdown_page.convert(page)
                    
                    return render(request, "encyclopedia/entry.html", {
                        'page': HTML_page,
                        'title': item,
                        'form': Search()
                    })
                if item.lower() in entry.lower():
                    found_pages.append(entry)

            return render(request, "encyclopedia/search.html", {
                'found_pages': found_pages,
                'form': Search()
            })

        else:
            return render(request, "encyclopedia/index.html", {"form": form})
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "form":Search()
        })

def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        HTML_page = markdown_page.convert(page) 

        return render(request, "encyclopedia/entry.html", {
            'page': HTML_page,
            'title': title,
            'form': Search()
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "form": Search()
        })

def search_page(request):
    if request.method == "GET":
        form = Search(request.GET)

        if form.is_valid():
            query = form.form.cleaned_data["search"].lower()
            entries = util.list_entries()

            files = [filename for filename in entries if query in filename.lower()]

            if len(files) == 0:
                return render(request, "encyclopedia/search.html", {
                    'error': "No results found",
                    "form": form
                })
            elif len(files) == 1 and files[0].lower() == query:
                title = files[0]
                return util.get_entry(title)
            else:
                title = [filename for filename in files if query == filename.lower()]

                if len(title) > 0:
                    return util.get_entry(title[0])
                else:
                    return render(request, "encyclopedia/search.html", {
                        'results': files,
                        "form": form
                    })
        else:
            return index(request)

    return index(request)

def create_new_page(request):
    if request.method == 'POST':
        form = Write(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {"form": Search(), "message": "Page already exist"})
            else:
                util.save_entry(title,textarea)
                page = util.get_entry(title)
                HTML_page = markdown_page.convert(page)

                return render(request, "encyclopedia/entry.html", {
                    'form': Search(),
                    'page': HTML_page,
                    'title': title
                })
    else:
        return render(request, "encyclopedia/new.html", {"form": Search(), "post": Write()})#todo check form necessity / probably not needed 

def edit_page(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)
        
        return render(request, "encyclopedia/edit.html", {
            'form': Search(),
            'edit': Edit(initial={'textarea': page}),
            'title': title
        })
    else:
        form = Edit(request.POST) 
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title,textarea)
            page = util.get_entry(title)
            HTML_page = markdown_page.convert(page)

            return render(request, "encyclopedia/entry.html", {
                'form': Search(),
                'page': HTML_page,
                'title': title
            })

def get_random_page(request):
    if request.method == 'GET':
        entries = util.list_entries()
        max_value = len(entries) - 1
        random_number = random.randint(0, max_value)
        random_page = entries[random_number]
        page = util.get_entry(random_page)
        HTML_page = markdown_page.convert(page)

        return render(request, "encyclopedia/entry.html", {
            'form': Search(),
            'page': HTML_page,
            'title': random_page
        })