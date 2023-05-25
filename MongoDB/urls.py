from django.urls import re_path as url
from .views import *

urlpatterns=[
    # Full table
    url(r'^query/$', query), # type: ignore    

    # Update table
    url(r'^update/$', updateDocument), # type: ignore    
    
    # First connection of UGV
    url(r'^ugv/firstConnection$', firstConnection), # type: ignore    

    # Chart query
    url(r'^chart/$', chart, name='chart'), # type: ignore   

    # Robot query
    url(r'^robot/$', robot, name='robot'), # type: ignore   

    # Robot query
    url(r'^script/$', script, name='robot'), # type: ignore       
]