# Create your models here.
from django.db import models
import uuid

class DataGenCluster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cluster_name = models.CharField(max_length=30, unique=True)
    cluster_username = models.CharField(max_length=30)
    cluster_dockerhub_username = models.CharField(max_length=30)
    cluster_dockerhub_repo_name = models.CharField(max_length=30)
    cluster_private_key = models.CharField(max_length=2000)
    cluster_dockerhub_registry_readwrite_key = models.CharField(max_length=2000)
    cluster_dockerhub_registry_readonly_key = models.CharField(max_length=2000)
    cluster_master_node = models.CharField(max_length=200)
    cluster_worker_nodes = models.CharField(max_length=20000)
    
