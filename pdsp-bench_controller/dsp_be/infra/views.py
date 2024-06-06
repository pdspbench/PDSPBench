# Create your views here.
import re
import subprocess
import json
import os
import shutil
import time
import requests
import yaml
from ansible import context
from ansible.cli import CLI
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory.manager import InventoryManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from yaml.loader import SafeLoader,BaseLoader

from infra.models import Cluster,Nodes
from utils.constants import WORD_COUNT, WORD_COUNT_PROGRAM, KAFKA, WORD_COUNT_INPUT, WORD_COUNT_OUTPUT, SMART_GRID, \
    SMART_GRID_PROGRAM, SMART_GRID_INPUT, SMART_GRID_OUTPUT, AD_ANALYTICS, AD_ANALYTICS_PROGRAM, AD_ANALYTICS_INPUT, AD_ANALYTICS_OUTPUT, \
    GOOGLE_CLOUD_MONITORING,GOOGLE_CLOUD_MONITORING_PROGRAM,GOOGLE_CLOUD_MONITORING_INPUT,GOOGLE_CLOUD_MONITORING_OUTPUT, \
    SENTIMENT_ANALYSIS, SENTIMENT_ANALYSIS_PROGRAM, SENTIMENT_ANALYSIS_INPUT, SENTIMENT_ANALYSIS_OUTPUT, SPIKE_DETECTION, SPIKE_DETECTION_PROGRAM, \
    SPIKE_DETECTION_INPUT, SPIKE_DETECTION_OUTPUT, LOG_ANALYZER, LOG_ANALYZER_PROGRAM, LOG_ANALYZER_INPUT, LOG_ANALYZER_OUTPUT, TRENDING_TOPICS, \
    TRENDING_TOPICS_PROGRAM,TRENDING_TOPICS_INPUT, TRENDING_TOPICS_OUTPUT,BARGAIN_INDEX,BARGAIN_INDEX_PROGRAM, BARGAIN_INDEX_OUTPUT, BARGAIN_INDEX_INPUT, \
    CLICK_ANALYTICS, CLICK_ANALYTICS_PROGRAM, CLICK_ANALYTICS_INPUT, CLICK_ANALYTICS_OUTPUT, LINEAR_ROAD, \
    LINEAR_ROAD_PROGRAM, LINEAR_ROAD_INPUT, LINEAR_ROAD_OUTPUT, \
    TPCH, TPCH_PROGRAM, TPCH_INPUT, TPCH_OUTPUT, \
    MACHINE_OUTLIER, MACHINE_OUTLIER_PROGRAM, MACHINE_OUTLIER_INPUT, MACHINE_OUTLIER_OUTPUT, \
    TRAFFIC_MONITORING, TRAFFIC_MONITORING_PROGRAM, TRAFFIC_MONITORING_INPUT, TRAFFIC_MONITORING_OUTPUT
    
def getprom_manipulataion(configs, getprompath):
    
    #TO DO: Change for report/views.py/nw utilization in get individualgraph()
    with open('hwtype.txt', 'w') as file1:
        file1.write('hardware_type=' + configs["hardware_cloudlab"])

    # Read the file
    with open(getprompath, 'r') as file:
        content = file.read()

    if configs["hardware_cloudlab"] == 'd710' or configs["hardware_cloudlab"] == 'm510':

        # Modify the string
        modified_content = re.sub(r'flink_taskmanager_System_Network_[a-zA-Z0-9_]+_SendRate', 'flink_taskmanager_System_Network_eno1_SendRate', content)
    
    if configs["hardware_cloudlab"] == 'xl170':
        modified_content = re.sub(r'flink_taskmanager_System_Network_[a-zA-Z0-9_]+_SendRate', 'flink_taskmanager_System_Network_eno49np0_SendRate', content)
    
    if configs["hardware_cloudlab"] == 'c6525-25g' or configs["hardware_cloudlab"] == 'c6525-100g':
        modified_content = re.sub(r'flink_taskmanager_System_Network_[a-zA-Z0-9_]+_SendRate', 'flink_taskmanager_System_Network_eno33np0_SendRate', content)
    
    # Write the updated content back to the file
    with open(getprompath, 'w') as file:
        file.write(modified_content)

    print("File updated successfully.")
def grafana_manipulation(configs, clusterjsonpath):
    
    # Read the JSON file
    with open(clusterjsonpath, 'r') as file:
        data = json.load(file)
    if configs["hardware_cloudlab"] == 'd710' or configs["hardware_cloudlab"] == 'm510':
        
        # Modify the value associated with the query
        data["panels"][3]["targets"][0]["expr"] = "flink_taskmanager_System_Network_eno1_SendRate"
    
    if configs["hardware_cloudlab"] == 'xl170':
        
        # Modify the value associated with the query
        data["panels"][3]["targets"][0]["expr"] = "flink_taskmanager_System_Network_eno49np0_SendRate"
    
    if configs["hardware_cloudlab"] == 'c6525-25g' or configs["hardware_cloudlab"] == 'c6525-100g':
        
        # Modify the value associated with the query
        data["panels"][3]["targets"][0]["expr"] = "flink_taskmanager_System_Network_eno33np0_SendRate"

    # Write the updated content back to the same file
    with open(clusterjsonpath, 'w') as file:
        json.dump(data, file, indent=2)

    print("File updated successfully.")
   

def _configure_and_run_playbooks(ansible_script_name, extravar=None,distributed=False):
    """ Configure the playbook
    """
    
    
    context.CLIARGS = ImmutableDict(connection='local', syntax=False, module_path=None, start_at_task=None,
                                    forks=10, become=None,
                                    become_method=None, become_user=None, check=False, diff=False)
    if extravar is None:
        extravar = dict()
    basevars = dict()
    
    if distributed:
        context.CLIARGS = ImmutableDict(connection='ssh',verbosity=True, syntax=False, module_path=None, start_at_task=None,
                                    forks=10, become=True, become_method='sudo', check=False, diff=False)
        
    
    basevars["BASE_DIR"] = str(settings.BASE_DIR)
    basevars["INSTALLATION_DIR"] = "/home/playground"

    

    extravar.update(basevars)
    data_loader = DataLoader()
    # Setting the base directory for Dataloader()
    # refer dsp_be/settings.py to find how BASE_DIR is being set.
    data_loader.set_basedir(os.path.join(settings.BASE_DIR, 'utils', 'playbook'))

    # Ansible's context should take these CLI arguments. setting up the config for Ansible

    """context.CLIARGS = ImmutableDict(tags={}, listtags=False, listtasks=False, listhosts=False, syntax=False, 
    connection='ssh', module_path=None, forks=10, remote_user=None, private_key_file=None, ssh_common_args=None, 
    ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True, become_method=None, 
    become_user=None, verbosity=True, check=True, start_at_task=None) """

    # inventory is the yaml for storing target nodes ip address
    # inventory.yaml contains the host group and the corresponding ip addresses of the nodes
    inventory_path = os.path.join(data_loader._basedir, 'inventory.yml')

    # We will need password later when we need to deploy remote nodes.
    password = {}

    # InventoryManager is to manage the inventory(nodes ip addresses)

    inventory_manager = InventoryManager(loader=data_loader, sources=inventory_path)

    # Ansible has the property of taking variables that makes Ansible dynamic. for e.g. if we want to choose
    # different versions of Flink or Kafka etc.
    variable_manager = VariableManager(loader=data_loader, inventory=inventory_manager, version_info=CLI.version_info(gitinfo=False))

    # passing the extravar to the variable_manager
    variable_manager._options_vars = extravar

    playbook_executor = PlaybookExecutor([data_loader._basedir + ansible_script_name], inventory_manager, variable_manager, data_loader, password)

    playbook_executor.run()

def _flink_config_manipulation(configs,jobmgr,tmgr):
    """ Edit and save the configs
    """
    # Creating a flink conf file from a default conf file
    source = 'infra/flink_files/sample-flink-conf.yaml'
    target = 'infra/flink_files/flink-conf.yaml'

    # shell utility to perform shell file/directory commands
    shutil.copy(source, target)

    # Open and load the temporary flink conf yaml file
    with open(target) as f:
        # loading the yaml file to a python dictionary(flink_configs)
        flink_configs = yaml.load(f, Loader=SafeLoader)

    flink_configs["taskmanager.numberOfTaskSlots"] = int(configs["cluster_tm_slots"])
    flink_configs["jobmanager.rpc.address"] = jobmgr
    flink_configs["taskmanager.host"] = tmgr
    
        
        
    # Dump the new configs
    with open(target, 'w') as f:
        yaml.dump(flink_configs, f, sort_keys=False, default_flow_style=False)

    return target

def _prometheus_config_manipulation(tm_nodes):
    """ Edit and save the configs
    """
    # Creating a flink conf file from a default conf file
    source = 'infra/prometheus_files/sample_prometheus.yml'
    target = 'infra/prometheus_files/prometheus.yml'
    
    # shell utility to perform shell file/directory commands
    shutil.copy(source, target)

    tm_nodes = ['{0}:9250'.format(tm_node) for tm_node in tm_nodes]
    
    # Open and load the temporary flink conf yaml file
    with open(source) as f:
        # loading the yaml file to a python dictionary(flink_configs)
        prometheus_configs = yaml.load(f, Loader=BaseLoader)

    
    
    prometheus_configs['scrape_configs'][1]['static_configs'][0]['targets']=tm_nodes
    
       
    # Dump the new configs
    with open(target, 'w') as f:
        yaml.dump(prometheus_configs, f, sort_keys=False, default_flow_style=None)

    return target

def _inventory_manipulation(groups):
    """ Edit and save the configs
        hosts = { 
                    'alphas': [{
                        host_name: 'pc122.ee.com',
                        user: 'shu7812'
                    }],
                    'betas': [{
                        host_name: 'pc123.ee.com',
                        user: 'shu7812'
                    }, {
                        host_name: 'pc124.ee.com',
                        user: 'shu7812'
                    }]
                } 
    """
    
    
    target = 'utils/playbook/inventory.yml'

    inventory = dict()
    for group in groups:
        host_list = dict()
        for host in groups[group]:
            host_inventory_properties = {
                'ansible_user': host['user'],
                'ansible_ssh_private_key_file': '~/.ssh/id_rsa'
            }
            host_list[host['host_name']] = host_inventory_properties
        inventory[group] = { 'hosts': host_list }


    # Dump the new configs
    with open(target, 'w', encoding="utf-8") as f:
        yaml.dump(inventory, f, sort_keys=False, default_flow_style=False,allow_unicode=True,encoding= None)

    return target

def _delete_tmp_config_file(flink_config_file):
    """ Delete temporary config file
    """

    os.remove(flink_config_file)

class AnsibleClusterCreate(View):
    """
    API endpoint that allows users to create cluster using ansible
    """

    @staticmethod
    def post(request):
        """ Upload configs and runs playbook
        """
        
        configs = json.loads(request.body)
        # checking if a clustername was provided
        if not configs["cluster_name"]:
            return JsonResponse(data={'status': 'Please check input configs', 'success': False},
                                status=400)

        # Iterating through all the Cluster objects from the DB and checking
        # if the provided cluster name already exists
        for cluster_instance in Cluster.objects.all():
            if configs["cluster_name"] == cluster_instance.name:
                return JsonResponse(data={'status': 'Another cluster with same name exists', 'success': False},
                                    status=406)
        
        if len(Nodes.objects.all()) == 0:
            return JsonResponse(data={'status': 'No nodes present', 'success': False},
                                    status=406)
        
        nodes_free = []                                    
        
        for node in Nodes.objects.all():
            node_occupied = False
            for cluster in Cluster.objects.all():
                if node.domain_name == cluster.main_node_ip:
                    node_occupied = True
                if node.domain_name in cluster.slave_node_ip.split(','):
                    node_occupied = True          
            if not node_occupied:        
                nodes_free.append(node)
                

        if len(nodes_free) < int(configs['cluster_num_tm'])+1:    
            return JsonResponse(data={'status': 'No free nodes present based on the requirements', 'success': False},
                                    status=406)
            
        # If no such cluster name exists, we create a new cluster object(row in the Cluster Table) 
        _flink_config_manipulation(configs,jobmgr=nodes_free[0].domain_name,tmgr="localhost")
        clusterjsonpath = os.path.abspath(os.path.join(settings.BASE_DIR, '../dsp_be/infra/grafana_files/cluster.json'))
        getprompath = os.path.abspath(os.path.join(settings.BASE_DIR, '../dsp_be/infra/reporting_scripts/getprom.py'))
        print(clusterjsonpath)
        print(getprompath)
        
        grafana_manipulation(configs, clusterjsonpath)
        getprom_manipulataion(configs, getprompath)
        hosts = dict()
        
        
        hosts = {'alpha':[{'host_name':nodes_free[0].domain_name,'user':nodes_free[0].user}]}
        _inventory_manipulation(hosts)
        
        tm_nodes = []
        for count in range(1, int(configs['cluster_num_tm'])+1):
            tm_nodes.append(nodes_free[count].domain_name)
        tmgr_list = ','.join(tm_nodes)

        _prometheus_config_manipulation(tm_nodes)
        _configure_and_run_playbooks("/cluster-complex-jm-create.yaml",distributed=True)
        
        for count in range(1, int(configs['cluster_num_tm'])+1):
            _flink_config_manipulation(configs,jobmgr=nodes_free[0].domain_name,tmgr=nodes_free[count].domain_name)
            #beta_nodes.append({'hosts':nodes_free[count].domain_name, 'user':nodes_free[count].user})
            hosts = {'betas':[{'host_name':nodes_free[count].domain_name, 'user':nodes_free[count].user}]}    
            _inventory_manipulation(hosts)
            _configure_and_run_playbooks("/cluster-complex-tm-create.yaml",distributed=True)
        

        Cluster.objects.create(name=configs["cluster_name"], main_node_ip=nodes_free[0].domain_name,slave_node_ip=tmgr_list)    
        
        return JsonResponse(data={'status': "Cluster created successfully",'success': True},
                            status=200)

class AnsibleClusterStart(View):
    """ API Endpoint to start the cluster
    """

    @staticmethod
    def get(request, **kwargs):
        """ Respond to GET requests 



            param kwargs: named URL parameters, part of the API
        """

        cluster_id = kwargs['id']
        
        cluster = Cluster.objects.get(id=cluster_id)
        
        main_domain_name = cluster.main_node_ip # Ex: 'pc555.emulab.net'
        slave_domain_names = cluster.slave_node_ip.split(',') # ['pc11.e.de','pc22.e.rt']
        main_node = Nodes.objects.get(domain_name=main_domain_name) # Node( domain_name ='pc555.emulab.net', user='shu7812')
        alpha = [{'host_name':main_node.domain_name,'user':main_node.user}]
        betas = []
        for slave_domain_name in slave_domain_names:
            slave_node = Nodes.objects.get(domain_name=slave_domain_name) 
            betas.append({'host_name':slave_node.domain_name, 'user':slave_node.user})
        hosts = {'alpha': alpha, 'betas':betas}
        _inventory_manipulation(hosts)

        
        _configure_and_run_playbooks('/cluster-complex-jm-start.yaml')
        _configure_and_run_playbooks('/cluster-complex-tm-start.yaml')
        response_status = 200
        data = {'message': 'Started cluster'}
        return JsonResponse(data, status=response_status)

class AnsibleClusterStop(View):
    """ API Endpoint to stop the cluster
    """

    @staticmethod
    def get(request, **kwargs):
        """ Respond to GET requests 

            param kwargs: named URL parameters, part of the API
        """

        cluster_id = kwargs['id']

        cluster = Cluster.objects.get(id=cluster_id)
        
        main_domain_name = cluster.main_node_ip # Ex: 'pc555.emulab.net'
        slave_domain_names = cluster.slave_node_ip.split(',') # ['pc11.e.de','pc22.e.rt']
        main_node = Nodes.objects.get(domain_name=main_domain_name) # Node( domain_name ='pc555.emulab.net', user='shu7812')
        alpha = [{'host_name':main_node.domain_name,'user':main_node.user}]
        betas = []
        for slave_domain_name in slave_domain_names:
            slave_node = Nodes.objects.get(domain_name=slave_domain_name) 
            betas.append({'host_name':slave_node.domain_name, 'user':slave_node.user})
        hosts = {'alpha': alpha, 'betas':betas}
        _inventory_manipulation(hosts)


        _configure_and_run_playbooks('/cluster-complex-jm-stop.yaml')
        _configure_and_run_playbooks('/cluster-complex-tm-stop.yaml')
        response_status = 200
        data = {'message': 'Stopped cluster'}
        return JsonResponse(data, status=response_status)

class AnsibleClusterDelete(View):
    """ API Endpoint to delete the cluster
    """

    @staticmethod
    def delete(request, **kwargs):
        """ Respond to GET requests 

            param kwargs: named URL parameters, part of the API
        """

        cluster_id = kwargs['id']

        cluster = Cluster.objects.get(id=cluster_id)
        try:
            main_domain_name = cluster.main_node_ip # Ex: 'pc555.emulab.net'
            slave_domain_names = cluster.slave_node_ip.split(',') # ['pc11.e.de','pc22.e.rt']
            main_node = Nodes.objects.get(domain_name=main_domain_name) # Node( domain_name ='pc555.emulab.net', user='shu7812')
            alpha = [{'host_name':main_node.domain_name,'user':main_node.user}]
            betas = []
            for slave_domain_name in slave_domain_names:
                slave_node = Nodes.objects.get(domain_name=slave_domain_name) 
                betas.append({'host_name':slave_node.domain_name, 'user':slave_node.user})
            hosts = {'alpha': alpha, 'betas':betas}
            _inventory_manipulation(hosts)



            _configure_and_run_playbooks('/cluster-simple-delete.yaml')
            Cluster.objects.get(id=cluster_id).delete()
        except:
            Cluster.objects.get(id=cluster_id).delete()
        response_status = 200
        data = {'message': 'Deleted cluster'}
        return JsonResponse(data=data, status=response_status)

# noinspection PyBroadException
class AnsibleClusterGetAllCluster(View):
    """ API Endpoint to get all the cluster
    """

    @staticmethod
    def get(request, **kwargs):
        """ Respond to GET requests

            param kwargs: named URL parameters, part of the API endpoint
        """

        user_id = kwargs['id']
        
        list_of_all_clusters = list()
        for cluster_instance in Cluster.objects.all():
            
            data = dict()
            data['name'] = cluster_instance.name
            data['id'] = cluster_instance.id
            data['creation_date'] = cluster_instance.creation_date
            data['main_node_ip'] = cluster_instance.main_node_ip
            print(data)

            try:
                requests.get("http://" + data['main_node_ip'] + ":8086")

                data['status'] = 'Running'
            except:
                data['status'] = 'Stopped'
            
            list_of_all_clusters.append(data)
        prepared_data = {"list_of_cluster": list_of_all_clusters}
        print('prepared data is:::::::::::::::::::')
        print(prepared_data)
        
        return JsonResponse(data=prepared_data, status=200)

# noinspection PyBroadException
class AnsibleClusterGetCluster(View):
    """ API Endpoint to delete the cluster
    """

    @staticmethod
    def get(request, **kwargs):
        """ Respond to GET requests

            param kwargs: named URL parameters, part of the API endpoint
        """

        cluster_id = kwargs['id']

        data = Cluster.objects.get(id=cluster_id)

        prepared_data = dict()
        prepared_data['id'] = data.id
        prepared_data['name'] = data.name
        try:
            requests.get("http://" + data.main_node_ip + ":8086")

            prepared_data['status'] = 'Running'
        except:
            prepared_data['status'] = 'Stopped'
        return JsonResponse(data=prepared_data, status=200)

class AnsibleClusterJobCreation(View):
    """ API Endpoint to create a job
    """

    @staticmethod
    def post(request, **kwargs):
        cluster_id = kwargs['id']
        
        
        configs = json.loads(request.body)
        print("Here")
        print(configs)
        cluster = Cluster.objects.get(id=cluster_id)
        
        main_domain_name = cluster.main_node_ip # Ex: 'pc555.emulab.net'
        configs['main_node_ip'] = cluster.main_node_ip
        slave_domain_names = cluster.slave_node_ip.split(',') # ['pc11.e.de','pc22.e.rt']
        main_node = Nodes.objects.get(domain_name=main_domain_name) # Node( domain_name ='pc555.emulab.net', user='shu7812')
        alpha = [{'host_name':main_node.domain_name,'user':main_node.user}]
        betas = []
        for slave_domain_name in slave_domain_names:
            slave_node = Nodes.objects.get(domain_name=slave_domain_name) 
            betas.append({'host_name':slave_node.domain_name, 'user':slave_node.user})
        hosts = {'alpha': alpha, 'betas':betas}
        _inventory_manipulation(hosts)

        ansible_variables = _config_manipulation_ansible(configs)
        
        #_configure_and_run_playbooks('/cluster-simple-job.yaml', extravar=ansible_variables, distributed=True)
        print("Number of times job is running" +str( configs['num_of_times_job_run'])    )
        for num in range(int(configs['num_of_times_job_run'])):
            
            _configure_and_run_playbooks('/cluster-simple-job.yaml', extravar=ansible_variables, distributed=True)
            url = "http://"+ configs['main_node_ip'] + ":8086/v1/jobs/overview"
            requested_cluster_jobs = requests.get(url)
            for job_in_cluster in requested_cluster_jobs.json()["jobs"]:
                state = job_in_cluster['state']
                if state == 'RUNNING':
                    jobId = job_in_cluster['jid']
                    break
            
            time.sleep(int(configs['job_run_time'])*60)
            # run the script with job Id and main node ip
            script_loc = os.path.join(settings.BASE_DIR, 'infra/reporting_scripts')
            script_name = os.path.join(script_loc, 'getprom.py')
            script_arguments = ["--main_node_ip", main_domain_name, 
                            "--job_id", jobId,
                            '--job_run_time', str(configs['job_run_time']), 
                            '--job_parallelization', ','.join(configs['job_pds']), 
                            '--job_query_number', str(configs['job_query_name']), 
                            '--job_window_size', str(configs['job_window_size']), 
                            '--job_window_slide_size', str(configs['job_window_slide_size']), 
                            '--producer_event_per_second', str(configs['job_class_input'])
            ]
        
            # Use subprocess to run the script with arguments
            try:
                subprocess.run(["python3", script_name] + script_arguments, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running the script: {e}")

            _configure_and_run_playbooks('/trigger-topic-deletion.yaml', extravar=ansible_variables, distributed=True)

        return JsonResponse({'status': 'Cluster Job created successfully', 'success': True})

def _config_manipulation_ansible(configurations):
    
    ansible_vars = dict()
    ansible_vars["job_run_time"] = int(configurations['job_run_time'])*60

    print(configurations)
    
    ansible_vars['partition'] = configurations['job_pds'][0]
    print("partition#################################################",ansible_vars['partition'])
    
    if configurations['job_class'] == WORD_COUNT:
        ansible_vars["job_program"] = WORD_COUNT_PROGRAM
        ansible_vars["google_lateness"] = configurations['job_google_lateness']
        ansible_vars["job_parallelization"] = ','.join(configurations['job_pds'])
        ansible_vars["job_query_number"] = configurations['job_query_name']
        ansible_vars["job_mode"] = configurations['job_class_input_type']
        ansible_vars["job_window_size"] = configurations['job_window_size']
        ansible_vars["job_window_slide_size"] = configurations['job_window_slide_size']
        ansible_vars["producer_program"] = "Word_Count"
        ansible_vars["producer_event_per_second"] = configurations['job_class_input']
        ansible_vars["job_threshold"] = configurations['job_threshold']

        if configurations['job_class_input_type'] == KAFKA:
            ansible_vars["producer_bootstrap_server"] = configurations['main_node_ip'] + ':9092'
            ansible_vars["job_input"] = WORD_COUNT_INPUT
            ansible_vars["job_output"] = WORD_COUNT_OUTPUT
        else:
            ansible_vars["job_input"] = configurations['job_class_input']
            ansible_vars["job_output"] = configurations['job_class_input']

    elif configurations['job_class'] == SMART_GRID:
        ansible_vars["job_program"] = SMART_GRID_PROGRAM
        ansible_vars["job_parallelization"] = ','.join(configurations['job_pds'])
        ansible_vars["google_lateness"] = configurations['job_google_lateness']
        ansible_vars["job_query_number"] = configurations['job_query_name']
        ansible_vars["job_mode"] = configurations['job_class_input_type']
        ansible_vars["job_window_size"] = configurations['job_window_size']
        ansible_vars["job_window_slide_size"] = configurations['job_window_slide_size']
        
        ansible_vars["producer_program"] = "Smart_Grid"
        ansible_vars["producer_event_per_second"] = configurations['job_class_input']
        ansible_vars["job_threshold"] = configurations['job_threshold']
        if configurations['job_class_input_type'] == KAFKA:
            ansible_vars["producer_bootstrap_server"] = configurations['main_node_ip']+":9092"
            ansible_vars["job_input"] = SMART_GRID_INPUT
            ansible_vars["job_output"] = SMART_GRID_OUTPUT
        else:
            ansible_vars["job_input"] = configurations['job_class_input']
            ansible_vars["job_output"] = configurations['job_class_input']

    elif configurations['job_class'] == AD_ANALYTICS:
        ansible_vars["job_program"] = AD_ANALYTICS_PROGRAM
        ansible_vars["job_parallelization"] = ','.join(configurations['job_pds'])
        ansible_vars["google_lateness"] = configurations['job_google_lateness']
        ansible_vars["job_query_number"] = configurations['job_query_name']
        ansible_vars["job_mode"] = configurations['job_class_input_type']
        ansible_vars["job_window_size"] = configurations['job_window_size']
        ansible_vars["job_window_slide_size"] = configurations['job_window_slide_size']
        ansible_vars["producer_program"] = "Ad_Analytics"
        ansible_vars["producer_event_per_second"] = configurations['job_class_input']
        ansible_vars["job_threshold"] = configurations['job_threshold']
        if configurations['job_class_input_type'] == KAFKA:
            ansible_vars["producer_bootstrap_server"] = configurations['main_node_ip']+":9092"
            ansible_vars["job_input"] = AD_ANALYTICS_INPUT
            ansible_vars["job_output"] = AD_ANALYTICS_OUTPUT

    elif configurations['job_class'] == GOOGLE_CLOUD_MONITORING:
        ansible_vars["job_program"] = GOOGLE_CLOUD_MONITORING_PROGRAM
        ansible_vars["job_parallelization"] = ','.join(configurations['job_pds'])
        ansible_vars["job_query_number"] = configurations['job_query_name']
        ansible_vars["google_lateness"] = configurations['job_google_lateness']
        ansible_vars["job_mode"] = configurations['job_class_input_type']
        ansible_vars["job_window_size"] = configurations['job_window_size']
        ansible_vars["job_window_slide_size"] = configurations['job_window_slide_size']
        ansible_vars["producer_program"] = "Google_Cloud_Monitoring"
        ansible_vars["producer_event_per_second"] = configurations['job_class_input']
        ansible_vars["job_threshold"] = configurations['job_threshold']
        if configurations['job_class_input_type'] == KAFKA:
            ansible_vars["producer_bootstrap_server"] = configurations['main_node_ip']+":9092"
            ansible_vars["job_input"] = GOOGLE_CLOUD_MONITORING_INPUT
            ansible_vars["job_output"] = GOOGLE_CLOUD_MONITORING_OUTPUT
    
    elif configurations['job_class'] == SENTIMENT_ANALYSIS:
        ansible_vars["job_program"] = SENTIMENT_ANALYSIS_PROGRAM
        ansible_vars["job_parallelization"] = ','.join(configurations['job_pds'])
        ansible_vars["job_query_number"] = configurations['job_query_name']
        ansible_vars["google_lateness"] = configurations['job_google_lateness']
        ansible_vars["job_mode"] = configurations['job_class_input_type']
        ansible_vars["job_window_size"] = configurations['job_window_size']
        ansible_vars["job_window_slide_size"] = configurations['job_window_slide_size']
        ansible_vars["producer_program"] = "Sentiment_Analysis"
        ansible_vars["producer_event_per_second"] = configurations['job_class_input']
        ansible_vars["job_threshold"] = configurations['job_threshold']
        if configurations['job_class_input_type'] == KAFKA:
            ansible_vars["producer_bootstrap_server"] = configurations['main_node_ip']+":9092"
            ansible_vars["job_input"] = SENTIMENT_ANALYSIS_INPUT
            ansible_vars["job_output"] = SENTIMENT_ANALYSIS_OUTPUT

    elif configurations['job_class'] == SPIKE_DETECTION:
        ansible_vars["job_program"] = SPIKE_DETECTION_PROGRAM
        ansible_vars["job_parallelization"] = ','.join(configurations['job_pds'])
        ansible_vars["job_query_number"] = configurations['job_query_name']
        ansible_vars["google_lateness"] = configurations['job_google_lateness']
        ansible_vars["job_mode"] = configurations['job_class_input_type']
        ansible_vars["job_window_size"] = configurations['job_window_size']
        ansible_vars["job_window_slide_size"] = configurations['job_window_slide_size']
        ansible_vars["producer_program"] = "Spike_detection"
        ansible_vars["producer_event_per_second"] = configurations['job_class_input']
        ansible_vars["job_threshold"] = configurations['job_threshold']
        if configurations['job_class_input_type'] == KAFKA:
            ansible_vars["producer_bootstrap_server"] = configurations['main_node_ip']+":9092"
            ansible_vars["job_input"] = SPIKE_DETECTION_INPUT
            ansible_vars["job_output"] = SPIKE_DETECTION_OUTPUT

    elif configurations['job_class'] == LOG_ANALYZER:
        ansible_vars["job_program"] = LOG_ANALYZER_PROGRAM
        ansible_vars["job_parallelization"] = ','.join(configurations['job_pds'])
        ansible_vars["job_query_number"] = configurations['job_query_name']
        ansible_vars["google_lateness"] = configurations['job_google_lateness']
        ansible_vars["job_mode"] = configurations['job_class_input_type']
        ansible_vars["job_window_size"] = configurations['job_window_size']
        ansible_vars["job_window_slide_size"] = configurations['job_window_slide_size']
        ansible_vars["producer_program"] = "Log_Processing"
        ansible_vars["producer_event_per_second"] = configurations['job_class_input']
        ansible_vars["job_threshold"] = configurations['job_threshold']
        if configurations['job_class_input_type'] == KAFKA:
            ansible_vars["producer_bootstrap_server"] = configurations['main_node_ip']+":9092"
            ansible_vars["job_input"] = LOG_ANALYZER_INPUT
            ansible_vars["job_output"] = LOG_ANALYZER_OUTPUT

    elif configurations['job_class'] == TRENDING_TOPICS:
        ansible_vars["job_program"] = TRENDING_TOPICS_PROGRAM
        ansible_vars["job_parallelization"] = ','.join(configurations['job_pds'])
        ansible_vars["job_query_number"] = configurations['job_query_name']
        ansible_vars["google_lateness"] = configurations['job_google_lateness']
        ansible_vars["job_mode"] = configurations['job_class_input_type']
        ansible_vars["job_window_size"] = configurations['job_window_size']
        ansible_vars["job_window_slide_size"] = configurations['job_window_slide_size']
        ansible_vars["producer_program"] = "Trending_Topic"
        ansible_vars["producer_event_per_second"] = configurations['job_class_input']
        ansible_vars["job_threshold"] = configurations['job_threshold']
        if configurations['job_class_input_type'] == KAFKA:
            ansible_vars["producer_bootstrap_server"] = configurations['main_node_ip']+":9092"
            ansible_vars["job_input"] = TRENDING_TOPICS_INPUT
            ansible_vars["job_output"] = TRENDING_TOPICS_OUTPUT

    
    elif configurations['job_class'] == BARGAIN_INDEX:
        ansible_vars["job_program"] = BARGAIN_INDEX_PROGRAM
        ansible_vars["job_parallelization"] = ','.join(configurations['job_pds'])
        ansible_vars["job_query_number"] = configurations['job_query_name']
        ansible_vars["google_lateness"] = configurations['job_google_lateness']
        ansible_vars["job_mode"] = configurations['job_class_input_type']
        ansible_vars["job_window_size"] = configurations['job_window_size']
        ansible_vars["job_window_slide_size"] = configurations['job_window_slide_size']
        ansible_vars["producer_program"] = "Bargain_Index"
        ansible_vars["producer_event_per_second"] = configurations['job_class_input']
        ansible_vars["job_threshold"] = configurations['job_threshold']
        if configurations['job_class_input_type'] == KAFKA:
            ansible_vars["producer_bootstrap_server"] = configurations['main_node_ip']+":9092"
            ansible_vars["job_input"] = BARGAIN_INDEX_INPUT
            ansible_vars["job_output"] = BARGAIN_INDEX_OUTPUT

    
    elif configurations['job_class'] == CLICK_ANALYTICS:
        ansible_vars["job_program"] = CLICK_ANALYTICS_PROGRAM
        ansible_vars["job_parallelization"] = ','.join(configurations['job_pds'])
        ansible_vars["job_query_number"] = configurations['job_query_name']
        ansible_vars["google_lateness"] = configurations['job_google_lateness']
        ansible_vars["job_mode"] = configurations['job_class_input_type']
        ansible_vars["job_window_size"] = configurations['job_window_size']
        ansible_vars["job_window_slide_size"] = configurations['job_window_slide_size']
        ansible_vars["producer_program"] = "Click_Analytics"
        ansible_vars["producer_event_per_second"] = configurations['job_class_input']
        ansible_vars["job_threshold"] = configurations['job_threshold']
        if configurations['job_class_input_type'] == KAFKA:
            ansible_vars["producer_bootstrap_server"] = configurations['main_node_ip']+":9092"
            ansible_vars["job_input"] = CLICK_ANALYTICS_INPUT
            ansible_vars["job_output"] = CLICK_ANALYTICS_OUTPUT

    elif configurations['job_class'] == LINEAR_ROAD:
        ansible_vars["job_program"] = LINEAR_ROAD_PROGRAM
        ansible_vars["job_parallelization"] = ','.join(configurations['job_pds'])
        ansible_vars["job_query_number"] = configurations['job_query_name']
        ansible_vars["google_lateness"] = configurations['job_google_lateness']
        ansible_vars["job_mode"] = configurations['job_class_input_type']
        ansible_vars["job_window_size"] = configurations['job_window_size']
        ansible_vars["job_window_slide_size"] = configurations['job_window_slide_size']
        ansible_vars["producer_program"] = "LRB"
        ansible_vars["producer_event_per_second"] = configurations['job_class_input']
        ansible_vars["job_threshold"] = configurations['job_threshold']
        if configurations['job_class_input_type'] == KAFKA:
            ansible_vars["producer_bootstrap_server"] = configurations['main_node_ip']+":9092"
            ansible_vars["job_input"] = LINEAR_ROAD_INPUT
            ansible_vars["job_output"] = LINEAR_ROAD_OUTPUT

    elif configurations['job_class'] == TPCH:
        ansible_vars["job_program"] = TPCH_PROGRAM
        ansible_vars["job_parallelization"] = ','.join(configurations['job_pds'])
        ansible_vars["job_query_number"] = configurations['job_query_name']
        ansible_vars["google_lateness"] = configurations['job_google_lateness']
        ansible_vars["job_mode"] = configurations['job_class_input_type']
        ansible_vars["job_window_size"] = configurations['job_window_size']
        ansible_vars["job_window_slide_size"] = configurations['job_window_slide_size']
        ansible_vars["producer_program"] = "Tpch"
        ansible_vars["producer_event_per_second"] = configurations['job_class_input']
        ansible_vars["job_threshold"] = configurations['job_threshold']
        if configurations['job_class_input_type'] == KAFKA:
            ansible_vars["producer_bootstrap_server"] = configurations['main_node_ip']+":9092"
            ansible_vars["job_input"] = TPCH_INPUT
            ansible_vars["job_output"] = TPCH_OUTPUT
    
    elif configurations['job_class'] == MACHINE_OUTLIER:
        ansible_vars["job_program"] = MACHINE_OUTLIER_PROGRAM
        ansible_vars["job_parallelization"] = ','.join(configurations['job_pds'])
        ansible_vars["job_query_number"] = configurations['job_query_name']
        ansible_vars["google_lateness"] = configurations['job_google_lateness']
        ansible_vars["job_mode"] = configurations['job_class_input_type']
        ansible_vars["job_window_size"] = configurations['job_window_size']
        ansible_vars["job_window_slide_size"] = configurations['job_window_slide_size']
        ansible_vars["producer_program"] = "Machine_Outlier"
        ansible_vars["producer_event_per_second"] = configurations['job_class_input']
        ansible_vars["job_threshold"] = configurations['job_threshold']
        if configurations['job_class_input_type'] == KAFKA:
            ansible_vars["producer_bootstrap_server"] = configurations['main_node_ip']+":9092"
            ansible_vars["job_input"] = MACHINE_OUTLIER_INPUT
            ansible_vars["job_output"] = MACHINE_OUTLIER_OUTPUT

    elif configurations['job_class'] == TRAFFIC_MONITORING:
        ansible_vars["job_program"] = TRAFFIC_MONITORING_PROGRAM
        ansible_vars["job_parallelization"] = ','.join(configurations['job_pds'])
        ansible_vars["job_query_number"] = configurations['job_query_name']
        ansible_vars["google_lateness"] = configurations['job_google_lateness']
        ansible_vars["job_mode"] = configurations['job_class_input_type']
        ansible_vars["job_window_size"] = configurations['job_window_size']
        ansible_vars["job_window_slide_size"] = configurations['job_window_slide_size']
        ansible_vars["producer_program"] = "Traffic_Monitoring"
        ansible_vars["producer_event_per_second"] = configurations['job_class_input']
        ansible_vars["job_threshold"] = configurations['job_threshold']
        if configurations['job_class_input_type'] == KAFKA:
            ansible_vars["producer_bootstrap_server"] = configurations['main_node_ip']+":9092"
            ansible_vars["job_input"] = TRAFFIC_MONITORING_INPUT
            ansible_vars["job_output"] = TRAFFIC_MONITORING_OUTPUT

        
    print(ansible_vars)
    return ansible_vars

class AnsibleNodeGetAll(View):

    @staticmethod
    def get(request, **kwargs):
        list_of_all_nodes = list()
        for node in Nodes.objects.all():
            
            data = dict()
            data['domain_name'] = node.domain_name
            data['creation_date'] = node.creation_date
            data['user'] = node.user

                
            
            list_of_all_nodes.append(data)
        prepared_data = {"list_of_nodes": list_of_all_nodes}
        
        return JsonResponse(data=prepared_data, status=200)

class CreateNode(View):
    
    @staticmethod
    def post(request,**kwargs):

        # loading request.body to a python dictionary(configs)
        configs = json.loads(request.body)
        
        # checking if a clustername was provided
        if not configs["domain_name"]:
            return JsonResponse(data={'status': 'Please check node names', 'success': False},
                                status=406)

        # Iterating through all the Cluster objects from the DB and checking
        # if the provided cluster name already exists
        for node in Nodes.objects.all():
            if configs["domain_name"] == node.domain_name:
                return JsonResponse(data={'status': 'Another node with same domain-name exists', 'success': False},
                                    status=406)
        # If no such cluster name exists, we create a new cluster object(row in the Cluster Table)
        Nodes.objects.create(domain_name=configs["domain_name"],user=configs["user"])
        
        return JsonResponse(data={'status': "Node created successfully",'success': True},
                            status=200)

class DeleteNode(View):
    
    @staticmethod
    def delete(request,**kwargs):
        node_domain_name = kwargs['domain_name']

        Nodes.objects.get(domain_name=node_domain_name).delete()
        
        response_status = 200
        data = {'message': 'Deleted node'}
        return JsonResponse(data=data, status=response_status)
