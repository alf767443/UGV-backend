from django.urls import re_path as url
from .views import *

urlpatterns=[
    # Full table
    url(r'^query/$', query), # type: ignore    

    # Update table
    url(r'^update/$', updateDocument), # type: ignore    
    
    # First connection of UGV
    url(r'^ugv/firstConnection$', firstConnection), # type: ignore    
]