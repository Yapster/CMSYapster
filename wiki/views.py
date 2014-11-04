from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q
from django.template.base import token_kwargs
from django.views.decorators.csrf import csrf_exempt
from wiki.models import *
import operator
from wiki.models import WikiPage


def search_results(request):
    """
    Results search for articles
    """
    categories = WikiCategory.objects.all()
    articles = WikiPage.objects.filter(is_current=True)
    text_search = ""
    if 'search_btn' in request.POST:
        if request.POST['search_text']:
            text_search = request.POST['search_text']
            l_words = text_search.split()
            articles = articles.filter(reduce(operator.and_, (Q(title__contains=x) for x in l_words)))
        if request.POST['category_search'] != "0":
            articles = articles.filter(categories__in=WikiCategory.objects.filter(pk=request.POST['category_search']))
        if request.POST['tags_search_text']:
            text_search = request.POST['tags_search_text']
            l_words = text_search.split()
            for word in l_words:
                articles = articles.filter(tags__in=WikiTag.objects.filter(name=word))

    return render(request,
                  "wiki/results.html",
                  {"categories": categories,
                   "articles": articles,
                   "text_search": text_search})


def bookmarks(request):
    """
    Boorkmarks user logged in
    """
    categories = WikiCategory.objects.all()
    bookmarks = request.user.favorites.all()
    folders = request.user.favorites_folders.all()
    return render(request,
                  "wiki/favorites.html",
                  {"categories": categories,
                   "articles": bookmarks,
                   "folders": folders})


def recently_viewed(request):
    """
    TODO
    """
    categories = WikiCategory.objects.all()

    return render(request,
                  "",
                  {"categories": categories})


def new_section(request, page):
    """
    New Section
    """
    categories = WikiCategory.objects.all()

    if 'save_section' in request.POST:
        kwargs = request.POST.copy()
        WikiSection.objects.create(page=WikiPage.objects.get(pk=page),
                                   title=kwargs['title'],
                                   content=kwargs['content'],
                                   writer=request.user)
        return redirect('/wiki/' + page + '/edit/')
    return render(request,
                  "",
                  {"categories": categories,
                   "article": WikiPage.objects.get(pk=page)})


def edit_section(request, page, section):
    categories = WikiCategory.objects.all()

    if "cancel_section" in request.POST:
        return render(request,
                      "wiki/edit_article.html",
                      {"article": WikiPage.objects.get(pk=page)})
    if "save_section" in request.POST:
        kwargs = request.POST.copy()
        current_section = WikiSection.objects.get(pk=section)
        if WikiSection.objects.create(page=current_section,
                                      title=kwargs['title'],
                                      content=kwargs['content'],
                                      writer=request.user,
                                      order=current_section.order):
            current_section.is_current = False
            current_section.save()
    return render(request,
                  "",
                  {"categories": categories,
                   "section": WikiSection.objects.get(pk=section),
                   "article": WikiPage.objects.get(pk=page)})


@login_required(login_url='/login')
@csrf_exempt
def edit_article(request, page):
    categories = WikiCategory.objects.all()

    if request.POST:
        current_page = WikiPage.objects.get(pk=page)
        if "save_article" in request.POST:
            kwargs = request.POST.copy()
            for key, value in kwargs.iteritems():
                print key, value
            current_page = WikiPage.objects.get(pk=page)
            # Create new Page
            new_page = WikiPage.objects.create(title=kwargs['title'], description=kwargs['description'])

            # New sections
            new_sections = []
            for section in current_page.sections.all():
                section_id = str(section.id)
                params = {}
                new_param_flag = False
                key = 'params[' + section_id + ']'
                if key in kwargs:
                    params['content'] = kwargs[key]
                    new_param_flag = True
                else:
                    params['content'] = section.content
                key = 'params[' + section_id + '_title]'
                if key in kwargs:
                    params['title'] = kwargs[key]
                    new_param_flag = True
                else:
                    params['title'] = section.title
                if new_param_flag:
                    params['page'] = new_page
                    params['order'] = section.order
                    params['writer'] = request.user
                    new_sections.append(WikiSection.objects.create(**params))
                    section.is_current = False
                    section.save()

            # Add sections to new_page
            for section in current_page.sections.all():
                if (section.is_current):
                    new_page.sections.add(section)
            for section in new_sections:
                new_page.sections.add(section)

            # Update Tags
            if 'params[tags]' in kwargs:
                new_tags = kwargs['params[tags]']
                for new_tag_name in new_tags.split():
                    tag_query = WikiTag.objects.filter(name=new_tag_name)
                    if tag_query.exists():
                        t = tag_query[0]
                    else:
                        t = WikiTag.objects.create(name=new_tag_name)
                    new_page.tags.add(t)

            # Update Categories
            for category in current_page.categories.all():
                new_page.categories.add(category)
            current_page.is_current = False
            current_page.save()
            current_page = new_page
        return HttpResponseRedirect('/wiki/' + str(current_page.id))
    else:
        return render(request,
                      "wiki/edit_article.html",
                      {"categories": categories,
                       "article": WikiPage.objects.get(pk=page)})


@login_required(login_url='/login')
def article(request, page):
    page = WikiPage.objects.get(pk=page)
    categories = WikiCategory.objects.all()
    is_favorite = page in request.user.favorites.all()
    return render(request,
                  "wiki/article.html",
                  {"categories": categories,
                   "page": page,
                   "is_favorite": is_favorite,
                   "user": request.user})

def new_article(request):
    return render(request,
                  "wiki/new_article.html",
                  {"user": request.user,
                   "categories": WikiCategory.objects.all()})


@login_required(login_url='/login')
@csrf_exempt
def save_bookmark(request):
    if request.POST:
        dic = request.POST.copy()
        if 'new_folder' in dic and request.POST['new_folder'] != "":
            f = WikiFolder.objects.create(name=dic['new_folder'],
                                          user=request.user)
        else:
            f = WikiFolder.objects.get(pk=dic['folder_id'])
        article = WikiPage.objects.get(pk=dic['page_id'])
        f.articles.add(article)
        if article not in request.user.favorites.all():
            request.user.favorites.add(article)
    return HttpResponse("Bookmarked")


@login_required(login_url='/login')
@csrf_exempt
def del_bookmark(request):
    if request.POST:
        article = WikiPage.objects.get(pk=request.POST['page_id'])
        request.user.favorites.remove(article)
        for folder in request.user.favorites_folders.all():
            if article in folder.articles.all():
                folder.articles.remove(article)
    return HttpResponse("UnBookmarked")

@login_required(login_url='/login')
def home(request):
    """
    Homepage wiki
    Display search bar / Bookmarks / Last Viewed / Categories / Tags
    """
    articles = WikiPage.objects.filter(is_current=True)[:5]
    categories = WikiCategory.objects.all()
    tags = WikiTag.objects.all()
    bookmarks = request.user.favorites.all()

    return render(request,
                  "wiki/home.html",
                  {"categories": categories,
                   "tags": tags,
                   "bookmarks": bookmarks,
                   "articles": articles})