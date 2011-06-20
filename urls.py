from django.conf.urls.defaults import *

urlpatterns = patterns('sentimental.views',
    url(r'^$',
        view='index',
        name='sentimental_index'),
    
    url(r'^register/$',
        view='register',
        name='sentimental_register'),
    
    url(r'^project_detail(?P<project_id>\d+)/$',
        view='project_detail',
        name='sentimental_project_detail'),
        
    url(r'^trainer/(?P<project_id>\d+)/$',
        view='trainer',
        name='sentimental_trainer'),
    
    url(r'^trainer_register/$',
        view='trainer_register',
        name='sentimental_trainer_register'),
    
    url(r'^trainer_fetch/$',
        view='trainer_fetch',
        name='sentimental_trainer_fetch'),
    
)