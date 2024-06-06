from django.urls import path

from . import views

# To Do : complete Start and Delete cluster endpoints.

urlpatterns = [
    path('create', views.AnsibleClusterCreate.as_view(), name='create cluster'),
    path('start/<str:id>', views.AnsibleClusterStart.as_view(), name='start cluster'),
    path('stop/<str:id>', views.AnsibleClusterStop.as_view(), name='stop cluster'),
    path('delete/<str:id>', views.AnsibleClusterDelete.as_view(), name='delete cluster'),
    path('jobcreate/<str:id>', views.AnsibleClusterJobCreation.as_view(), name='create job'),
    path('getAll/<str:id>', views.AnsibleClusterGetAllCluster.as_view(), name='Get all cluster'),
    path('getCluster/<str:id>', views.AnsibleClusterGetCluster.as_view(), name='Get a particular cluster'),
    path('getAll/nodes/<str:id>', views.AnsibleNodeGetAll.as_view(), name='Get all nodes'),
    path('create/node/<str:id>', views.CreateNode.as_view(), name='Create a node'),
    path('node/delete/<str:domain_name>', views.DeleteNode.as_view(), name='Delete a node')
    
]
