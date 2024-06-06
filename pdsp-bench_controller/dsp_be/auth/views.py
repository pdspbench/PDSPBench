from django.shortcuts import render
from django.views import View
from infra.models import Cluster
from django.http import JsonResponse
import json
# Create your views here.
class RegisterUser(View):
    """
    API endpoint that allows users to register for the dsp benchmarking
    """
    
    def post(self, request, *args, **kwargs):
        """ Upload configs and runs playbook
        """
        
        configs = json.loads(request.body)
        
        return JsonResponse({'status':'Registered successfully', 'success': True})


class LoginUser(View):
    """
    API endpoint that allows users to login to dsp benchmark tool
    """
    
    def post(self, request, *args, **kwargs):
        """ Upload configs and runs playbook
        """
        
        configs = json.loads(request.body)
        
        return JsonResponse({'status':'Registered successfully', 'success': True})

class HealthyChecker(View):
    """
        API Endpoint to check if app is connecting to DB and working fine
    """
    def get(self,request,*args,**kwargs):
        try:
            clusters = Cluster.objects.all()
            
        except:
            return JsonResponse(data={'status': 'APP incorrectly initialized as DB cannot be connected', 'success': False},
                                    status=406)
        return JsonResponse(data={'status': 'APP correctly initalized', 'success': True},
                                    status=200)