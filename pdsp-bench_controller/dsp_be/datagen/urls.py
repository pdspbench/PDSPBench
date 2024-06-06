from django.urls import path

from . import views



urlpatterns = [
    path('clusterdeploy', views.DataGenInitialization.as_view(), name='Data Gen Initialization'),
    path('clustercreate', views.DatagenClusterCRUD.as_view(), name='Data Generator Cluster CRUD'),
    path('runplangenerator', views.RunPlanGenerator.as_view(), name='Run Data Generator'),
    path('download/local', views.DownloadResults.as_view(), name='Download Data'),
    path('download/distributed', views.DownloadDistResults.as_view(), name='Download Distributed cluster Data'),
    
    
]
