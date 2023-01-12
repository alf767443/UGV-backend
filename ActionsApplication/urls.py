#from django.conf.urls import url
from django.urls import include,re_path as url
from ActionsApplication import views

urlpatterns=[
    url(r'^actions/table=actions$', views.actionsApi),
    url(r'^actions/table=actions/([0-9]+)$', views.actionsApi),

    url(r'^actions/table=queue$', views.queueApi),
    url(r'^actions/table=queue/([0-9]+)$', views.queueApi),


    url(r'^actions/actions$', views.actionsApi),
    url(r'^actions/actions/([0-9]+)$', views.actionsApi),

    url(r'^actions/queue$', views.queueApi),
    url(r'^actions/queue/([0-9]+)$', views.queueApi)
]