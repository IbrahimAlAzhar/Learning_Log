from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('topics/',views.topics,name='topics'),
    path('topics/<int:topic_id>/',views.topic,name='topic'), # this url is for topic detail,topic_id pass to view function as a argument and view fucntion find out the related id of topic_id
    #url(r'^topics/(?P<topic_id>\d+)/$', views.topic,name='topic'),
    path('new_topics/',views.new_topic,name='new_topic'),
    path('new_entry/<int:topic_id>',views.new_entry,name='new_entry'), # include a topic_id argument in the url for adding a new entry because the entry must be associated with particular topic
    # /new_entry/id/,where id is a number matching the topic ID,this url captures the numerical value and stores it in the variable topic_id,when a url matching this pattern is requested,django sends the request and the id of the topic to the new_entry() view function
    path('edit_entry/<int:entry_id>',views.edit_entry,name='edit_entry'), # take argument entry_id from user
]
