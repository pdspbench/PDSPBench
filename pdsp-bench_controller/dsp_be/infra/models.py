from django.db import models
import uuid

#add the metrics model on database


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=30)
    registration_complete = models.BooleanField(default=False)
    registration_token = models.CharField(max_length=200)
    jwt = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date published')


class Cluster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)
    main_node_ip = models.CharField(max_length=200)
    slave_node_ip = models.CharField(max_length=1000,blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)


class UserClusterMap(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cluster_id = models.ForeignKey(Cluster, on_delete=models.CASCADE)

class Nodes(models.Model):
    
    domain_name = models.CharField(primary_key=True,max_length=30, unique=True)
    user = models.CharField(max_length=30, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)