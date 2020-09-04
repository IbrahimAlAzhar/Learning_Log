from django import forms
from .models import Topic, Entry


class TopicForm(forms.ModelForm): # inherit modelform which is build from the Model
    class Meta: # in modelform consists of a nested meta class telling django which model to base the form on and which fields to include in the form
        model = Topic
        fields = ['text'] # we can use also '__all__'
        labels = {'text':''} # using dictionary to generate a label for the text field


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''} # here define the label of 'text' field is blank,we can use any label of this text field
        widgets = {'text': forms.Textarea(attrs={'cols':80})} # widget is an html form element such as single line text box,multi line text area or drop down list
        # by including widget attributes you can override django default which is 40 columns
