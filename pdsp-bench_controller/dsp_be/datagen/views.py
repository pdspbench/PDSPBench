import json
from datetime import datetime
import os
import shutil 
import subprocess
import signal
import time
import paramiko

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.conf import settings
from datagen.models import DataGenCluster

import zipfile
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class DataGenInitialization(View):

    @staticmethod
    def post(request, **kwargs):
        configs = json.loads(request.body)
        print(configs)
        # checking if a clustername was provided
        if not configs["cluster_name"]:
            return JsonResponse(data={'status': 'Please check input configs', 'success': False},
                                status=400)
        workerNodesAll = configs['cluster_worker_nodes']
        print(workerNodesAll)
        """ for workerNodesConfig in configs['cluster_worker_nodes']:
            print(workerNodesConfig['worker_node'])
            workerNodesAll.append(workerNodesConfig['worker_node'])  """
        _create_remote_cluster_key(configs["cluster_private_key"])
        _create_master_node_file(configs["cluster_master_node"])
        _create_worker_node_file(workerNodesAll)
        _pgf_env_file(user_name=configs["cluster_username"]
                      ,dockerhub_repo=configs["cluster_dockerhub_repo_name"]
                      ,dockerhub_username=configs["cluster_dockerhub_username"]
                      ,dockerhub_rw_key=configs["cluster_dockerhub_registry_readwrite_key"]
                      ,dockerhub_read_key=configs["cluster_dockerhub_registry_readonly_key"])
       
        #time.sleep(20)
        return_val =_deployk8s()

        #time.sleep(20)
        if return_val['return_code'] == 0:

            return JsonResponse(data={'status': "Cluster is deployed",'success': True, 'output':return_val['value']},
                           status=200)
        else:

            return JsonResponse(data={'status': "Cluster is  not deployed because of some error",'success': False},
                           status=200)
class DatagenClusterCRUD(View):
    @staticmethod
    def post(request, **kwargs):
        configs = json.loads(request.body)
        print(configs)
        # checking if a clustername was provided
        if not configs["cluster_name"]:
            return JsonResponse(data={'status': 'Please check input configs', 'success': False},
                                status=400)

        # Iterating through all the DataGen Cluster objects from the DB and checking
        # if the provided cluster name already exists
        for datagen_cluster_instance in DataGenCluster.objects.all():
            if configs["cluster_name"] == datagen_cluster_instance.cluster_name:
                return JsonResponse(data={'status': 'Another cluster with same name exists', 'success': False},
                                    status=406)
        
        workerNodesAll = []
        for workerNodesConfig in configs['cluster_worker_nodes']:          
            workerNodesAll.append(workerNodesConfig['worker_node'])
        print(workerNodesAll) 
        cluster_worker_nodes = ','.join(workerNodesAll)

        DataGenCluster.objects.create(
            cluster_name=configs["cluster_name"], 
            cluster_username=configs["cluster_username"],
            cluster_dockerhub_username=configs["cluster_dockerhub_username"],
            cluster_dockerhub_repo_name=configs["cluster_dockerhub_repo_name"], 
            cluster_dockerhub_registry_readwrite_key=configs["cluster_dockerhub_registry_readwrite_key"],
            cluster_dockerhub_registry_readonly_key=configs["cluster_dockerhub_registry_readonly_key"],
            cluster_master_node=configs["cluster_master_node"], 
            cluster_worker_nodes=cluster_worker_nodes,
            cluster_private_key=configs["cluster_private_key"],
        )    
        
        
        return JsonResponse(data={'status': "Cluster details saved and necessary files were created successfully. Now move on to selecting one of the clusters from the cluster list to deploy the cluster",'success': True},
                            status=200) 
        
    
    @staticmethod
    def get(request, **kwargs):
        allData = DataGenCluster.objects.all()
        finalPrepared = []
        for data in allData:
            prepared_data = dict()
            prepared_data['cluster_name'] = data.cluster_name
            prepared_data['cluster_username'] = data.cluster_username
            prepared_data['cluster_dockerhub_username'] = data.cluster_dockerhub_username
            prepared_data['cluster_dockerhub_repo_name'] = data.cluster_dockerhub_repo_name
            prepared_data['cluster_dockerhub_registry_readwrite_key'] = data.cluster_dockerhub_registry_readwrite_key
            prepared_data['cluster_dockerhub_registry_readonly_key'] = data.cluster_dockerhub_registry_readonly_key
            prepared_data['cluster_master_node'] = data.cluster_master_node
            prepared_data['cluster_worker_nodes'] = data.cluster_worker_nodes.split(',')
            prepared_data['cluster_private_key'] = data.cluster_private_key
            prepared_data['action'] = ''
            finalPrepared.append(prepared_data)
        return JsonResponse(data={'list_of_clusters':finalPrepared}, status=200)
        
    
    @staticmethod
    def delete(request, **kwargs):
        configs = json.loads(request.body)
        DataGenCluster.objects.get(cluster_name=configs['cluster_name']).delete()
        response_status = 200
        data = {'message': 'Deleted cluster'}
        return JsonResponse(data=data, status=response_status)

class RunPlanGenerator(View):
    @staticmethod
    def post(request, **kwargs):
        configs = json.loads(request.body)
        print(configs)
        return_val =_run_plan_generator(configs)
        if return_val['return_code'] == 0:
            if configs["deployMode"] == 'Local':

                return JsonResponse(data={'status': "Data gen ran successfully on your local cluster",'success': True, 'output':return_val['value']},
                            status=200)
        
            if configs["deployMode"] == 'Distributed':

                return JsonResponse(data={'status': "Data gen ran successfully on your remote cluster",'success': True, 'output':return_val['value']},
                           status=200)
        else:
            return JsonResponse(data={'status': "Data gen failed",'success': False},
                           status=500)

class DownloadResults(View):

    @staticmethod
    def get(request, **kwargs):
        folder_path = settings.DSP_PGF_LOGS
        zip_filename = 'local.zip'

        with zipfile.ZipFile(zip_filename, 'w') as zip_file:
            # Add the parent directory itself to the ZIP archive
            zip_file.write(folder_path, os.path.basename(folder_path))
            # Recursively add files and subdirectories to the ZIP archive
            add_folder_to_zip(zip_file, folder_path)
        # Create an HTTP response with the ZIP archive as content
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
        with open(zip_filename, 'rb') as f:
            response.write(f.read())

        # Delete the ZIP archive
        os.remove(zip_filename)

        return response

class DownloadDistResults(View):
    @staticmethod
    def get(request, **kwargs):

        masternode_file_path = settings.DSP_MANAGMENT_DIR + "/masterNode"
        username_masternode_file_path = settings.DSP_MANAGMENT_DIR + "/pgf-env"

        with open(masternode_file_path, 'r') as f:
            content = f.read()
            hostname = content.split('=')[1].strip()
            print(hostname)

        with open(username_masternode_file_path, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            for line in lines:
                if line.startswith('usernameNodes='):
                    nodeusername = line.split('=')[1].strip()
            print(nodeusername)
        
        # Remote folder path
        remote_dir = '/users/'+nodeusername+'/pgf-results'

        # Local temporary folder to store the compressed file
        local_folder = settings.BASE_DIR

        # Connect to remote node using ssh
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=nodeusername)

        # Create an SFTP client
        sftp = ssh.open_sftp()

        # Create a list to store the file paths of downloaded files
        file_paths = []

        # Download all files in the remote directory to a local directory
        for file_name in sftp.listdir(remote_dir):
            remote_file_path = os.path.join(remote_dir, file_name)
            local_file_path = os.path.join(local_folder, file_name)
            sftp.get(remote_file_path, local_file_path)
            file_paths.append(local_file_path)

        # Close the SFTP client and SSH session
        sftp.close()
        ssh.close()

        # Create a zip file containing all downloaded files
        zip_file_path = os.path.abspath(os.path.join(settings.BASE_DIR, '../file.zip'))
        #zip_file_path = settings.BASE_DIR +'/file.zip'
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            for file_path in file_paths:
                zip_file.write(file_path, os.path.basename(file_path))

        # Open the zip file and create a response with its content to trigger a file download
        with open(zip_file_path, 'rb') as zip_file:
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=distributed.zip'

        # Delete the zip file from the server
        os.remove(zip_file_path)

        return response
        
# a func to add sub dir and files from 'pgf-logs' folder
def add_folder_to_zip(zip_file, folder_path):
    """
    Recursively add files and subdirectories to the ZIP archive.
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            zip_file.write(file_path, os.path.relpath(file_path, folder_path))
        for directory in dirs:
            dir_path = os.path.join(root, directory)
            zip_file.write(dir_path, os.path.relpath(dir_path, folder_path))


def _create_remote_cluster_key(private_key):
    
    with open('datagen/files/remote_cluster.key', 'w') as f:
        f.write(private_key) 
    # Creating a flink conf file from a default conf file
    source = 'datagen/files/remote_cluster.key'
    target = os.path.join(settings.DSP_MANAGMENT_DIR, 'remote_cluster.key')

    # shell utility to perform shell file/directory commands
    shutil.copy(source, target)

def _create_master_node_file(master_node):
    processed_master_node = 'masterNode='+master_node
    with open('datagen/files/masterNode', 'w') as f:
        f.write(processed_master_node) 
    # Creating a flink conf file from a default conf file
    source = 'datagen/files/masterNode'
    target = os.path.join(settings.DSP_MANAGMENT_DIR, 'masterNode')

    # shell utility to perform shell file/directory commands
    shutil.copy(source, target)

def _create_worker_node_file(worker_nodes):
    processed_worker_nodes = ' '.join(worker_nodes)            
    with open('datagen/files/workerNodes', 'w') as f:
        f.write(processed_worker_nodes) 
    # Creating a flink conf file from a default conf file
    source = 'datagen/files/workerNodes'
    target = os.path.join(settings.DSP_MANAGMENT_DIR, 'workerNodes')

    # shell utility to perform shell file/directory commands
    shutil.copy(source, target)

def _pgf_env_file(user_name, dockerhub_repo, dockerhub_username, dockerhub_rw_key, dockerhub_read_key):
    
    processed_pgf_env = 'usernameNodes=' + user_name + '\n'+\
        'privateRegistryRepoName=' + dockerhub_repo + '\n'+\
        'privateRegistryUsername='+ dockerhub_username + '\n' + \
        'privateRegistryReadWriteKey='+ dockerhub_rw_key + '\n' + \
        'privateRegistryReadOnlyKey='+ dockerhub_read_key

    with open('datagen/files/pgf-env', 'w') as f:
        f.write(processed_pgf_env) 
    # Creating a flink conf file from a default conf file
    source = 'datagen/files/pgf-env'
    target = os.path.join(settings.DSP_MANAGMENT_DIR, 'pgf-env')

    # shell utility to perform shell file/directory commands
    shutil.copy(source, target)

def _deployk8s():

    cmd = os.path.join(settings.DSP_MANAGMENT_DIR, 'setupPlanGeneratorFlink.sh')
   
    process = subprocess.Popen([cmd], stdin=subprocess.PIPE, cwd=settings.DSP_MANAGMENT_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    # Provide the first input
    process.stdin.write(b'12\n')
    process.stdin.flush()

    # Provide the second input
    process.stdin.write(b'\n')
    process.stdin.flush()

    # Provide the third input
    process.stdin.write(b'1\n')
    process.stdin.flush()

    stdout, stderr = process.communicate()

    # Print the output
    output = "Standard Output:\n{}".format(stdout.decode())
    print("Standard Error:\n{}".format(stderr.decode()))

    return_code = process.wait()
    if return_code != 0:
        print(f'Error: The subprocess exited with return code {return_code}')
    else:
        print('The subprocess completed successfully')

    return {'return_code':return_code, 'value':output}

def _run_plan_generator(plan_gen_config):
    print(plan_gen_config)
    if plan_gen_config["deployMode"] == 'Local':
        cmd = settings.DSP_FLINK_BUILD + " " + "run" + " " + settings.DSP_PLANGEN_JAR + " " + "--logdir" + " " + settings.DSP_PGF_LOGS + " " + "--mode" + " " + plan_gen_config["mode"] + " " + "--numTopos" + " " + plan_gen_config["numberOfTopol"] + " " + "--environment" + " " + "localCommandLine" + " " + "--enumerationStrategy" + " " + plan_gen_config["enumerationStrategy"]+ " " + "--duration" + " " + plan_gen_config["executionTime"]
    elif plan_gen_config["deployMode"] == 'Distributed':  
        cmd = "~/flink/bin/flink run --target kubernetes-session -Dkubernetes.cluster-id=plangeneratorflink-cluster -Dkubernetes.namespace=plangeneratorflink-namespace -Dkubernetes.rest-service.exposed.type=NodePort ~//flink/lib/plangeneratorflink-1.0-SNAPSHOT.jar --logdir ~/pgf-results" + " " + "--mode" + " " + plan_gen_config["mode"] + " " + "--numTopos" + " " + plan_gen_config["numberOfTopol"] + " " + "--environment" + " " + "kubernetes" + " " + "--enumerationStrategy" + " " + plan_gen_config["enumerationStrategy"]+ " " + "--duration" + " " + plan_gen_config["executionTime"]
    if plan_gen_config["mode"] == 'train':
        templstring = ','.join(plan_gen_config["traintempl"])        
        cmd = cmd + " " + "--templates" + " " + templstring

        if "deterministic" in plan_gen_config and plan_gen_config["deterministic"] == 'true':
            cmd = cmd + " " + "--deterministic"

        if "useAllOperators" in plan_gen_config and  plan_gen_config["useAllOperators"] == 'true':
            cmd = cmd + " " + "--UseAllOps"
    if plan_gen_config["mode"] == 'test':
        cmd = cmd + " " + "--templates" + " " + plan_gen_config["testtempl"]     
            
    if plan_gen_config["enumerationStrategy"] == 'EXHAUSTIV':
        cmd = cmd + " " + "--exhaustiveParallelismStepSize" + " " + plan_gen_config["exhaustiveParallelismStepSize"]       
            
    if plan_gen_config["enumerationStrategy"] == 'PARAMETERBASED':
        cmd = cmd + " " + "--parallelism" + " " + plan_gen_config["parallelism"]   
    print(cmd)
    cmdSplit = cmd.split(' ')
    

    if plan_gen_config["deployMode"] == 'Local':
        process = subprocess.Popen(cmdSplit, cwd=settings.DSP_MANAGMENT_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True )
        
        stdout, stderr = process.communicate()

        # Print the output
        output = "Standard Output:\n{}".format(stdout.decode())
        print("Standard Error:\n{}".format(stderr.decode()))
        
        return_code = process.wait()
        if return_code != 0:
            print(f'Error: The subprocess exited with return code {return_code}')
        else:            
            print('The subprocess completed successfully')

        return {'return_code':return_code, 'value':output}
        
        
        """ # Wait for 5 seconds
        time.sleep(20)

        # Send the SIGTERM signal to stop the command
        process.send_signal(signal.SIGTERM)
        print(process.stdout)

        return "success"
 """
        # Provide the first input
    elif plan_gen_config["deployMode"] == 'Distributed':

        masternode_file_path = settings.DSP_MANAGMENT_DIR + "/masterNode"
        username_masternode_file_path = settings.DSP_MANAGMENT_DIR + "/pgf-env"

        with open(masternode_file_path, 'r') as f:
            content = f.read()
            hostname = content.split('=')[1].strip()
            print(hostname)

        with open(username_masternode_file_path, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            for line in lines:
                if line.startswith('usernameNodes='):
                    nodeusername = line.split('=')[1].strip()
            print(nodeusername)

        # Connect to remote node using ssh
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=nodeusername)

        # Run command on remote node
        stdin, stdout, stderr = ssh.exec_command(cmd)

        output = stdout.read().decode()
        print('printing the output again')
        print(output)

        # Close the SSH connection
        ssh.close()

        return {'return_code':0, 'value': output }
