from django.urls import re_path as url
from .views import query

urlpatterns=[
    # Full table
    url(r'^query/$', query), # type: ignore    
]