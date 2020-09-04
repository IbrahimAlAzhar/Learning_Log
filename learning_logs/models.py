from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Topic(models.Model):
    """A topic the user is learning about"""
    text = models.CharField(max_length=200) # in charfield we define how much space it should reserve in the database
    date_ad = models.DateTimeField(auto_now_add=True) # auto_now_add is True means django is automatically set the attribute to the current date and time whenever the user creates a new topic
    # we modify some of the views so they only show the data associated with the current logged-in user
    owner = models.ForeignKey(User,on_delete=models.CASCADE) # here using foreign key relationship,each topic has a 'owner' attribute which is foreign key of User,we create owner attribute of Topic class because we set each owner see his own topic only,we can also do this work by using "PermisionRequiredMixin" in class based view

    def __str__(self):
        """Return a string representation of the model"""
        return self.text

    def get_absolute_url(self):
        return reverse('topic',args=[str(self.id)]) # id is build in django provides for each model,here 'topic' is detailview name and pass 'id' for each detail view


class Entry(models.Model):
    """Something specific learned about a topic"""
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE) # class Entry is foreignkey of Topic means one to many relation,one topic has multiple entries but one entry is in one topic
    text = models.TextField() # this field doesn't need a size limit
    date_field = models.DateTimeField(auto_now_add=True) # automatically dateTime added when each entry added

    class Meta:
        verbose_name_plural = 'entries' # meta holds extra information for managing a model,it use 'entries' in place of 'entrys' when it needs to refer to more than one entry

    def __str__(self):
        """Return a string representation of the model"""
        return self.text[:50] # the string representation of this model is show first 50 charachters on text
