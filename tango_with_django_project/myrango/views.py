#-*-coding: utf-8-*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from myrango.models import Category, Page
from myrango.forms import CategoryForm, PageForm, UserForm, UserProfileForm, User, UserProfile
from myrango.utils import decode_url
from myrango.bing_search import search_query
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)


def myfunction():
    logger.debug("this is a debug message!")


def myotherfunction():
    logger.error("this is an error message!!")


def index(request):
    context = RequestContext(request)

    context_variables = get_category_and_page_list()
    context_variables["boldmessage"] = "HERE WILL BE BOLD"

    if request.session.get("last_visit"):
        visits = request.session.get("visits")
        last_visit_time = request.session.get("last_visit")
        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).seconds > 5:
            request.session["visits"] = visits + 1
            request.session["last_visit"] = str(datetime.now())
    else:
        request.session["visits"] = 1
        request.session["last_visit"] = str(datetime.now())

    return render_to_response("myrango/index.html", context_variables, context)


def category(request, category_name_url):
    context = RequestContext(request)
    context_variables = get_category_and_page_list()
    # category_name = category_name_url.replace("_"," ")
    context_variables['category_name'] = category_name_url

    try:
        cat = Category.objects.get(name=category_name_url)
        c = Category.objects

        pages_of_category = Page.objects.filter(category=cat)
        context_variables["category"] = cat
        context_variables["pages_of_category"] = pages_of_category
    except:
        pass

    result_list = get_search_results(request)
    context_variables['result_list'] = result_list

    return render_to_response("myrango/category.html", context_variables, context)


@login_required
def add_category(request):
    context = RequestContext(request)
    context_variables = get_category_and_page_list()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print form.errors

    else:
        form = CategoryForm()

    context_variables["form"] = form

    return render_to_response("myrango/add_category.html", context_variables, context)


@login_required
def profile(request):
    context = RequestContext(request)
    context_variables = get_category_and_page_list()
    us = User.objects.get(username=request.user)
    try:
        us_profile = UserProfile.objects.get(user=us)

    except:
        us_profile = None
    context_variables["us_profile"] = us_profile
    context_variables["us"] = us

    return render_to_response("myrango/profile.html", context_variables, context)


@login_required
def add_page(request, category_name_url):
    context = RequestContext(request)
    context_variables = get_category_and_page_list()

    category_name = category_name_url

    try:

        cat = Category.objects.get(name=category_name)

    except Category.DoesNotExist:

        return render_to_response("myrango/add_category.html", context_variables, context)

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid:
            page = form.save(commit=False)
            page.category = cat
            page.views = 0
            page.save()
            return category(request, category_name)

        else:

            print form.errors

    else:
        form = PageForm()
        context_variables['category_name_url'] = category_name_url
        context_variables['category_name'] = category_name
        context_variables['form'] = form

        return render_to_response('myrango/add_page.html',
                                  context_variables,
                                  context)


def register(request):
    context = RequestContext(request)
    context_variables = get_category_and_page_list()

    already_registered = False

    if request.method != 'POST':
        user_form = UserForm()
        user_profile_form = UserProfileForm()
    else:

        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)

        if user_form.is_valid and user_profile_form.is_valid:

            user = user_form.save()

            user.set_password(user.password)

            user.save()

            user_profile = user_profile_form.save(commit=False)

            user_profile.user = user

            if "picture" in request.FILES:
                user_profile.picture = request.FILES["picture"]
            user_profile.save()

            already_registered = True
        else:
            print ">>>>>>>>>>>>>>>>  ", user_form.errors, user_profile_form.errors

    context_variables['user_form'] = user_form
    context_variables['user_profile_form'] = user_profile_form
    context_variables['already_registered'] = already_registered
    return render_to_response("myrango/register.html",
                              context_variables, context)


def user_login(request):
    context = RequestContext(request)

    context_variables = get_category_and_page_list()

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if not user:
            return HttpResponse("Username or Password could not be found ")
        else:

            if not user.is_active:


                return HttpResponse("Your Account is not active")

            else:

                login(request, user)
                return HttpResponseRedirect("/myrango")

    else:
        return render_to_response("myrango/login.html", context_variables, context)


@login_required
def restricted(request):
    return HttpResponse("If you are see here , you are already logged in ")


@login_required
def log_out(request):
    logout(request)

    return HttpResponseRedirect("/myrango/login")


def search(request):
    context = RequestContext(request)

    context_variables = get_category_and_page_list()
    result_list = get_search_results(request)
    context_variables['result_list'] = result_list

    return render_to_response("myrango/search.html", context_variables, context)


def track_url(request):
    context = RequestContext(request)
    url = "/myrango"

    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET["page_id"]
            try:
                tracked_page = Page.objects.get(id=page_id)
                tracked_page.views = tracked_page.views + 1
                url = tracked_page.url
                tracked_page.save()
            except:
                pass

    return HttpResponseRedirect(url)


@login_required
def like_category(request):
    context = RequestContext(request)
    like_count = 0

    if request.method == 'GET':
        if 'category_id' in request.GET:
            category_id = request.GET["category_id"]
            try:
                cat = Category.objects.get(id=int(category_id))
                cat.likes = cat.likes + 1
                like_count = cat.likes
                cat.save()
            except:
                pass
    return HttpResponse(like_count)


def suggest_category(request):
    context = RequestContext(request)
    categories = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']

    categories = get_category_list(8, starts_with)

    return render_to_response('myrango/category_list.html', {'categories': categories}, context)


def get_search_results(request):
    result_list = []
    if request.method == "POST":
        search_it = request.POST["query"].strip()
        if search_it:
            result_list = search_query(search_it)
    return result_list


@login_required
def auto_add_page(request):

    context = RequestContext(request)
    cat_id = None
    link = None
    title = None
    context_dict = {}
    print "REQUEST METHODU " , request.method
    if request.method == 'GET':
        cat_id = request.GET['cat_id']
        link = request.GET['link'].encode('utf-8').strip()
        title = request.GET['title'].encode('utf-8').strip()
        if cat_id:
            category = Category.objects.get(id=int(cat_id))
            p = Page.objects.get_or_create(category=category, title=title, url=link)

            pages = Page.objects.filter(category=category).order_by('-views')

            context_dict['pages'] = pages

    return render_to_response('myrango/page_list.html', context_dict, context)


def get_category_list(max_results=0, starts_with=''):
    if not max_results and not starts_with:

        categories = Category.objects.order_by("-likes")[:5]
        for category in categories:
            category.url = decode_url(category.name)
        return categories
    else:
        return get_suggested_category_list(max_results, starts_with)


def get_suggested_category_list(max_results, starts_with):
    if starts_with:
        categories = Category.objects.filter(name__istartswith=starts_with)
    else:
        categories = Category.objects.all()

    if max_results > 0:
        if len(categories) > max_results:
            categories = categories[:max_results]
    for cat in categories:
        cat.url = decode_url(cat.name)
    return categories


def get_page_list():
    return Page.objects.order_by("-views")[:5]


def get_category_and_page_list():
    context_variables = {}
    categories = get_category_list()
    context_variables["categories"] = categories
    pages = get_page_list()
    context_variables["pages"] = pages
    return context_variables













































