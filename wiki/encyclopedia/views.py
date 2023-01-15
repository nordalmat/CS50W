from django.shortcuts import render
from django import forms
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if util.get_entry(title) is not None:
        return render(request, "encyclopedia/entry.html", {
            "content": util.get_entry(title), 
            'title': title,
        })
    else:
        return render(request, 'encyclopedia/error404.html')


def search(request):
    if request.method == 'POST':
        entry_search = request.POST["q"]
        allEntries = util.list_entries()
        if entry_search in allEntries:
            return render(request, "encyclopedia/entry.html", {
            "content": util.get_entry(entry_search), 
            'title': entry_search,
        })
        else:
            result = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    result.append(entry)
            if len(result) == 0:
                return render(request, 'encyclopedia/error404.html')
            return render(request, "encyclopedia/search.html", {
                'result': result
            })


def add(request):
    if request.method == "POST":
        title = request.POST['title']
        entry = request.POST.get('entry')
        if title not in util.list_entries():
            util.save_entry(title, entry)
            return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
        else:
            return render(request, 'encyclopedia/add.html', {
                'title': title,
                'entry': entry, 
                'msg': 'Entry with the given title already exists!!!'     
            })
    return render(request, 'encyclopedia/add.html')


def edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        entry = util.get_entry(title)
        return render(request, 'encyclopedia/edit.html', {
            'title': title,
            'entry': entry 
        })


def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        entry = request.POST.get('entry')
        util.save_entry(title, entry)
        return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
    else:
        return render(request, 'encyclopedia/edit.html', {
            'title': title,
            'entry': entry 
        })


def random_page(request):
    allEntries = util.list_entries()
    k = random.randint(0, len(allEntries) - 1)
    title = allEntries[k]
    return render(request, "encyclopedia/entry.html", {
            "content": util.get_entry(title), 
            'title': title,
        })
