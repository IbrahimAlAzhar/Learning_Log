from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    """The home page for learning log"""
    return render(request,'learning_logs/index.html')

@login_required # each topic will be owned by a user,so only registered users should be able to request the topics page,if the user is not logged in,they're redirected to the login page for that reason we set it into settings.py file as a 'LOGIN_URL'(where to find the login page)
def topics(request):  # receive one parameter 'request' object Django received from the server
    """Show all topics"""
    # request object has request.user attribute set that stores information about the user,this filter tells django to retrive only the Topic objects from the database whose owner attribute matches the current user,but if anyone use link like 'topics/1' then it can't prevents
    topics = Topic.objects.filter(owner=request.user).order_by("id") # we can't use 'date_added' in django 2.0,in place we have to use "id", query the database by asking for the topic objects,take all topic which is sorted by the 'date_added' attribute
    context = {
        'topics': topics  # pass the topics to html page which stores all topics
    }
    return render(request,"learning_logs/topics.html",context)


@login_required # here using login_required for the user must login if he access topic,for that reason we set 'LOGIN_URL' path in settings.py file
def topic(request,topic_id): # this parameter value come from urls file on user request,the function accepts the value captured by the <int:topic_id> and stores it in topic_id
    """show a single topic and all its entries"""
    # where this function tries to get the requested object from database,but if that object doesn't exist,it raises a 404 exception
    topic = Topic.objects.get_object_or_404(id=topic_id) # take these id which matches with 'topic_id'
    # make sure the topic belongs to the current user
    if topic.owner != request.user: # owner is the attribute of Topic class(which is the owner of a topic) and request.user is current user,if the current user is same as the owner of topic then he can see the topic detail
        raise Http404
    entries = topic.entry_set.order_by("id")  # take all entries related to this topic using 'entry_set'(modelname_set) and most recent entries display first,we can't use order_by 'date_added' in here,we use "id"
    context = {
        'topic': topic,
        'entries': entries
    }
    return render(request,'learning_logs/topic.html',context)

@login_required # here using login_required for the user must login if he access new_topic,for that reason we set 'LOGIN_URL' path in settings.py file
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # no data submitted,create a blank form
        form = TopicForm() # make an isntance of TopicForm() and put it into form vairable, using get,put method show the blank form,get requests for pages that only read data from the server
    else:
        # post data submitted,process data
        form = TopicForm(request.POST) # make an instance of the topic form and pass it the data entered by the user,stored in request.POST,the form object that's returned contains the information submitted by the user,use post requests when the user needs to submit information through a form
        if form.is_valid(): # check the validation like length of the text is less than 200 characters(define in models.py)
            # these three line because if we create a topic then it takes the current user for 'owner' attribute in 'Topic' model
            new_topic = form.save(commit=False) # we create a instance of 'form' class which is 'new_topic' but we have not save yet into database
            new_topic.owner = request.user # we set request.user(current user) to owner attribute of new_topic instance(new_topic is a instance of form class)
            new_topic.save() # save the instance and set the owner attribute to current user
            return HttpResponseRedirect(reverse('topics')) # use reverse() to get the url for the topics page and pass the url to HttpResponseRedirect,which redirects the user's browser to the topics page, after add topic then return the url name 'topics',# import the class HttpResponseRedirect,which we'll use to redirect the reader back to the topics page after they submit their topic,
# the reverse() function determines the url from a named url pattern,meaning that django will generate the url when the page is requested
    context = {'form': form}
    return render(request,"learning_logs/new_topic.html",context)


@login_required # here using login_required for the user must login if he access new_entry,for that reason we set 'LOGIN_URL' path in settings.py file
def new_entry(request,topic_id): # the topic is argument come from urls.py file,where a user request to topic_id
    """Add a new entry for a particular topic"""
    topic = Topic.objects.get(id=topic_id)  # use topic_id to get the correct topic object at
    if request.method != 'POST':
        # no data submitted,create a blank form
        form = EntryForm() # if the request is get,put method then create a instance of 'EntryForm' class and store it to 'form' variable,and pass the 'form' variable using 'context' dictionary in template
    else:
        # post data submitted,process data
        form = EntryForm(data=request.POST) # populated with the post data from the request object
        if form.is_valid():
            new_entry = form.save(commit=False) # create a 'new_entry' from form and don't save it into database yet,to tell django to create a new entry object and store it in new_entry without saving it to the database yet
            new_entry.topic = topic  # need to set the entry object's topic attribute before saving it to the database,'new_entry' is instance of form means Topic model and store the 'topic' in 'topic' attribute of 'new_entry' instance
            new_entry.save()
            return HttpResponseRedirect(reverse('topic',args=[topic_id])) # reverse need two argument-the name of the url and args list containing any arguments that need to be included in the url, HttpResponseRedirect() call then redirects the user to the topic url name
    context = {
        'topic': topic,
        'form': form
    }
    return render(request,"learning_logs/new_entry.html",context)


@login_required # if the unauthorized user try to access then it show login page which path define on settings file,for that reason we set 'LOGIN_URL' path in settings.py file
def edit_entry(request,entry_id): # take the argument from urls.py file which one pass from user
    """Edit an existing entry"""
    entry = Entry.objects.get(id=entry_id) # we get the entry object that the user wants to edit and the topic associated with this entry,take the entry using this entry_id,id is build in attribute in Entry model
    topic = entry.topic # using topic attribute of entry model and store it to topic variable
    if topic.owner != request.user: # here a user can access other edit_entry url,to prevent this we check this, if the owner of the topic are not matches with the currently logged-in user then raise Htttp404 error
        raise Http404
    if request.method != 'POST':
        # initial request,pre-fill form with the current entry,"instance=entry",this argument tells django to create the form prefilled with information from the existing entry object,the user will see their existing data and be able to edit the data
        form = EntryForm(instance=entry) # create a instance of EntryForm and store it to form variable where instance is entry(pre fill)
    else:
        # post data submitted,process data
        form = EntryForm(instance=entry,data=request.POST) # to tell django to create a form instance based on the information associated with the existing entry object,updated with any relevant data from request.POST
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic',args=[topic.id])) # return the url name where needs topic.id
    context = {
        'entry': entry,
        'topic': topic,
        'form': form
    }
    return render(request,"learning_logs/edit_entry.html",context)



