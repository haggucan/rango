from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from myrango.models import Category, Page
from myrango.forms import CategoryForm, PageForm ,UserForm, UserProfileForm
from myrango.utils import decode_url
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)


def myfunction():
    logger.debug("this is a debug message!")


def myotherfunction():
    logger.error("this is an error message!!")


def index(request):
    context = RequestContext(request)

    categories = Category.objects.order_by("-likes")[:5]

    pages = Page.objects.order_by("-views")[:5]

    for category in categories:
        category.url = category.name.replace(' ', '_')
    context_variables = {"boldmessage": "HERE WILL BE BOLD", "categories": categories}
    context_variables["pages"] = pages
    return render_to_response("myrango/index.html", context_variables, context)


def category(request, category_name_url):
    context = RequestContext(request)
    #category_name = category_name_url.replace("_"," ")
    context_variables = {"category_name": category_name_url}
    try:
        cat = Category.objects.get(name=category_name_url)
        c = Category.objects

        pages = Page.objects.filter(category=cat)
        context_variables["category"] = cat
        context_variables["pages"] = pages
    except:
        pass

    return render_to_response("myrango/category.html", context_variables, context)

@login_required
def add_category(request):
    context = RequestContext(request)
    context_variables = {}

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
def add_page(request, category_name_url):
    context = RequestContext(request)

    category_name = decode_url(category_name_url)

    try:

        cat = Category.objects.get(name=category_name)

    except Category.DoesNotExist:

        return render_to_response("myrango/add_category.html", {}, context)

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
        return render_to_response('myrango/add_page.html',
                          {'category_name_url': category_name_url,
                           'category_name': category_name, 'form': form},
                          context)

def register(request):

    context = RequestContext(request)

    already_registered = False

    if request.method != 'POST' :
        user_form = UserForm()
        user_profile_form = UserProfileForm()
    else:

        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)

        if user_form.is_valid and user_profile_form.is_valid :

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
            print user_form.errors,user_profile_form.errors

    return render_to_response("myrango/register.html",{"user_form":user_form,"user_profile_form":user_profile_form,"already_registered":already_registered},context)




def user_login(request):

    context = RequestContext(request)

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username,password=password)

        if not user:
            return HttpResponse("Username or Password could not be found ")
        else:

            if not user.is_active:


                return HttpResponse("Your Account is not active")

            else : 

                login(request,user)
                return HttpResponseRedirect("/myrango")

    else :
        return render_to_response("myrango/login.html",{},context)


@login_required
def restricted(request):
    return HttpResponse("If you are see here , you are already logged in ")

@login_required
def log_out(request):
    logout(request)

    return HttpResponseRedirect("/myrango/login")













































