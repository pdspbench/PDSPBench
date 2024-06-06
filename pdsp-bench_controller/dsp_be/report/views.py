import json
from datetime import datetime
import os
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from infra.models import Cluster
from confluent_kafka import Consumer, KafkaError
from django.conf import settings
from utils.constants import  WORD_COUNT_OUTPUT, SMART_GRID_OUTPUT, AD_ANALYTICS_OUTPUT, \
    GOOGLE_CLOUD_MONITORING_OUTPUT, SENTIMENT_ANALYSIS_OUTPUT, \
    SPIKE_DETECTION_OUTPUT, TRENDING_TOPICS_OUTPUT, LOG_ANALYZER_OUTPUT, BARGAIN_INDEX_OUTPUT, CLICK_ANALYTICS_OUTPUT, LINEAR_ROAD_OUTPUT, \
    TPCH_OUTPUT, MACHINE_OUTLIER_OUTPUT, TRAFFIC_MONITORING_OUTPUT


# Create your views here.
class GetSinkTopicResults(View):
   @staticmethod
   def get(request, **kwargs):

        response_status = 200
        cluster_id = kwargs["cluster_id"]
        job_id = kwargs["job_id"]
        data_size = kwargs["data_size"]
        print("Cluster id is" + cluster_id)

        try:
            cluster_obj = Cluster.objects.get(id=cluster_id)
            print('cluster found in DB')
        except Exception as e:
            print(e)
            return JsonResponse(e, status=response_status, safe=False)

        cluster = cluster_obj.main_node_ip
        verticeResponse = requests.get(
            "http://" + cluster + ":8086/v1/jobs/"+job_id)
        jsonVertice = verticeResponse.json()

        #print(jsonVertice)
        if jsonVertice["name"] == 'Google Cloud Monitoring':
            topic = GOOGLE_CLOUD_MONITORING_OUTPUT
        elif jsonVertice["name"] == 'Ads Analytics':
            topic = AD_ANALYTICS_OUTPUT
        elif jsonVertice["name"] == 'Flink smart grid job':
            topic = SMART_GRID_OUTPUT
        elif jsonVertice["name"] == 'Flink word count job':
            topic = WORD_COUNT_OUTPUT
        elif jsonVertice["name"] == "Sentiment Analysis":
            topic = SENTIMENT_ANALYSIS_OUTPUT
        elif jsonVertice["name"] == "Spike Detection":
            topic = SPIKE_DETECTION_OUTPUT
        elif jsonVertice["name"] == "Trending Topics":
            topic = TRENDING_TOPICS_OUTPUT
        elif jsonVertice["name"] == "Logs Processing":
            topic = LOG_ANALYZER_OUTPUT
        elif jsonVertice["name"] == "Bargain Index":
            topic = BARGAIN_INDEX_OUTPUT
        elif jsonVertice["name"] == "Click Analytics":
            topic = CLICK_ANALYTICS_OUTPUT
        elif jsonVertice["name"] == "Linear Road":
            topic = LINEAR_ROAD_OUTPUT
        elif jsonVertice["name"] == "TPCH":
            topic = TPCH_OUTPUT
        elif jsonVertice["name"] == "Machine Outlier":
            topic = MACHINE_OUTLIER_OUTPUT
        elif jsonVertice["name"] == "Traffic Monitoring":
            topic = TRAFFIC_MONITORING_OUTPUT
            
        bootstrap_servers = cluster+':9092'
        group_id = 'your-consumer-group'  # Replace with your consumer group ID
        print(topic)
        consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False
        })

        consumer.subscribe([topic])

        messages = []
        if data_size == 'partial':
            print('parital')
            while len(messages) < 100:
                msg = consumer.poll(1.0)
                msgcount = 0
                if msg is None:
                    msgcount += 1
                    if msgcount < 20:
                        continue
                    else:
                        break
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        continue
                    else:   
                        print("Consumer error: {}".format(msg.error()))
                        break
                    # Process the Kafka message as needed
                message = msg.value().decode('utf-8')
                messages.append(message)
        else:
            msgcount = 0
            while True:
                msg = consumer.poll(1.0)
                print(msg)
                
                if msg is None:
                    msgcount += 1
                    if msgcount < 20:
                        continue
                    else:
                        break
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        continue
                    else:
                        print("Consumer error: {}".format(msg.error()))
                        break
                    # Process the Kafka message as needed
                message = msg.value().decode('utf-8')
                messages.append(message)
        print("Output kafka stream messages")
        print(messages)
        return JsonResponse(data={'messages': messages}, status = 200)
       
class GetAllJobs(View):

    @staticmethod
    def get(request, **kwargs):
        response_status = 200
        user_id = kwargs["user_id"]

        list_of_all_clusters = list()
        for cluster_instance in Cluster.objects.all():
            
            data = dict()
            data['name'] = cluster_instance.name
            data['id'] = cluster_instance.id
            data['creation_date'] = cluster_instance.creation_date
            data['main_node_ip'] = cluster_instance.main_node_ip

            # Requesting cluster specific details by making an API call to
            # Flink using specific node id.

            try:
                requests.get("http://" + data['main_node_ip'] + ":8086")

                data['status'] = 'Running'
            except:
                data['status'] = 'Stopped'
            
            list_of_all_clusters.append(data)

        list_of_all_jobs = []

        # Get the list of jobs for each cluster
        for cluster in list_of_all_clusters:
            if cluster["status"] == 'Running':
                requested_cluster_jobs = requests.get("http://"+cluster["main_node_ip"] + ":8086/v1/jobs/overview")
                for job_in_cluster in requested_cluster_jobs.json()["jobs"]:
                    
                    job_in_cluster['cluster'] = cluster['id']
                    job_in_cluster['main_node_ip'] = cluster['main_node_ip']
                    list_of_all_jobs.append(job_in_cluster)
        
        return JsonResponse({"jobs":list_of_all_jobs}, status=response_status, safe=False)

class GetThisClusterJobs(View):


    @staticmethod
    def get(request, **kwargs):
        response_status = 200
        cluster_id = kwargs["cluster_id"]

        
        # Get the list of clusters from DB
        list_of_all_jobs = []

        cluster = Cluster.objects.get(id=cluster_id)
        cluster_main_node_ip = cluster.main_node_ip
        requested_cluster_jobs = requests.get("http://" + cluster_main_node_ip + ":8086/v1/jobs/overview")

        for job_in_cluster in requested_cluster_jobs.json()["jobs"]:
                    
            job_in_cluster['cluster_id'] = cluster_id
            job_in_cluster['main_node_ip'] = cluster_main_node_ip
            job_in_cluster['full_name'] = job_in_cluster['name'] +':'+ job_in_cluster['jid']
            list_of_all_jobs.append(job_in_cluster)

        print(list_of_all_jobs)
        
        
        return JsonResponse({"jobs":list_of_all_jobs}, status=response_status, safe=False)

class StopJob(View):

    @staticmethod
    def get(request, **kwargs):
        response_status = 200
        user_id = kwargs["user_id"]
        
        list_of_all_clusters = ['http:localhost:8086']

        list_of_all_jobs = []

        # Get the list of jobs for each cluster
        for cluster in list_of_all_clusters:
            requested_cluster_jobs = requests.get(cluster + "/v1/jobs")
            
        data = {'list': list_of_all_jobs}
        return JsonResponse(data, status=response_status)

class GetJobInfo(View):

    @staticmethod
    def get(request, **kwargs):
        response_status = 200
        cluster_id = kwargs["cluster_id"]
        job_id = kwargs["job_id"]
        list_of_all_clusters = []
        for cluster_instance in Cluster.objects.all():
            list_of_all_clusters.append(cluster_instance.main_node_ip)
        
        # Get the list of jobs for each cluster
        for cluster in list_of_all_clusters:
            requested_cluster_job = requests.get("http://"+ cluster + ":8086/v1/jobs/"+job_id)
            
            
        print("JobInfo was succesful")
        return JsonResponse(json.dumps(requested_cluster_job.json()), status=response_status, safe=False)

class GetOperatorInfo(View):

    @staticmethod
    def get(request, **kwargs):
        response_status = 200
        cluster_id = kwargs["cluster_id"]
        job_id = kwargs["job_id"]
        
        # Get the list of operators for specific cluster's specific job.
        
        requested_clusters_jobs_operators = requests.get("http://"+ cluster_id + ":8086/v1/jobs/"+job_id)
        print(requested_clusters_jobs_operators)  
            

        return JsonResponse(json.dumps(requested_clusters_jobs_operators.json()), status=response_status, safe=False)

def getOperatorMetrics(op_parallelism, cluster, job_id, verticeIdoperator, op_name):
    dict_metrtics = {}
    dict_metrtics[op_name] = []
    for num in range(0,op_parallelism):
        #framing endpoint addresses numRecordsOutPerSecond
        
            endpointrecOutPerSecoperator = cluster + ":8086/v1/jobs/"+job_id + "/vertices/" + verticeIdoperator + "/metrics?get="+ str(num) +".numRecordsOutPerSecond"

        #calling end point 
        
            resprecOutPerSecoperator = requests.get("http://"+endpointrecOutPerSecoperator)
            jsonrecOutPerSecoperator = resprecOutPerSecoperator.json()
            out_value = float(jsonrecOutPerSecoperator[0]["value"])
            
        #framing endpoint addresses numRecordsInPerSecond
        
            endpointrecInPerSecoperator = cluster + ":8086/v1/jobs/"+job_id + "/vertices/" + verticeIdoperator + "/metrics?get="+str(num)+".numRecordsInPerSecond"

        #calling end point for  operator metrics numRecordsInPerSecond)
        
            resprecInPerSecoperator = requests.get("http://"+endpointrecInPerSecoperator)
            jsonrecInPerSecoperator = resprecInPerSecoperator.json()
            in_value = float(jsonrecInPerSecoperator[0]["value"])

        #framing endpoint addresses for  SmartGrid operator (0.SlidingProcessingTimeWindows.numBytesInPerSecond)
            endpointBytesInPerSecoperator = cluster + ":8086/v1/jobs/"+job_id + "/vertices/" + verticeIdoperator + "/metrics?get="+str(num)+".numBytesInPerSecond"
        #calling end point for SmartGrid operator metrics  (0.SlidingProcessingTimeWindows.numBytesInPerSecond)
            respBytesInPerSecoperator = requests.get("http://"+endpointBytesInPerSecoperator)
            jsonBytesInPerSecoperator = respBytesInPerSecoperator.json()
            
            bytes_in_value = float(jsonBytesInPerSecoperator[0]["value"])

        #calculating size in bytes of each record at the operator
            if in_value != 0.0:
                size_eachRecord = bytes_in_value / in_value
            else:
                size_eachRecord = 0.0
            str_size_eachRecord = str(size_eachRecord)

        #calculating selectivity
            if in_value != 0.0:
                selectivity = out_value / in_value
            else:
                selectivity = 0.0
            str_selectivity = str(selectivity)

            operator_dict = {'persecondout'+op_name+'.'+str(num)+'': jsonrecOutPerSecoperator[0],'selectivity'+op_name+'.'+str(num)+'': str_selectivity,'BytesOfeachrecord'+op_name+'.'+str(num)+'' : str_size_eachRecord}
            dict_metrtics[op_name].append(operator_dict)

    return dict_metrtics    

def getTrendingTopics(jsonVertice, cluster, job_id):
    verticeIdTrendingTopicsParser = None
    verticeIdTrendingTopicsExtractor = None
    verticeIdTrendingTopicsPopularityDetector = None
    
    dictTrendingTopicsParser = {}
    dictTrendingTopicsExtractor = {}
    dictTrendingTopicsPopularityDetector = {}
    
    dictCombo = {}
    jobName = jsonVertice["name"]

    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "twitter-parser" in vertice["name"]:
                TrendingTopicsParser_name = "twitter-parser"
                verticeIdTrendingTopicsParser = vertice["id"] 
                numOfTrendingTopicsParser = int(vertice["parallelism"])
            elif "name" in vertice and "topic-extractor" in vertice["name"]:
                TrendingTopicsExtractor_name = "topic-extractor"
                verticeIdTrendingTopicsExtractor = vertice["id"]
                numOfTrendingTopicsExtractor = int(vertice["parallelism"])
            elif "name" in vertice and "popularity-detector" in vertice["name"]:
                TrendingTopicsPopularityDetector_name = "popularity-detector"
                verticeIdTrendingTopicsPopularityDetector = vertice["id"]
                numOfTrendingTopicsPopularityDetector = int(vertice["parallelism"])
            
    job_dict = {"job_name": jobName}
    dictCombo = job_dict.copy()

    dictTrendingTopicsParser = getOperatorMetrics(numOfTrendingTopicsParser,cluster,job_id,verticeIdTrendingTopicsParser,TrendingTopicsParser_name)
    dictCombo.update(dictTrendingTopicsParser)

    dictTrendingTopicsExtractor = getOperatorMetrics(numOfTrendingTopicsExtractor,cluster,job_id,verticeIdTrendingTopicsExtractor,TrendingTopicsExtractor_name)
    dictCombo.update(dictTrendingTopicsExtractor)

    dictTrendingTopicsPopularityDetector = getOperatorMetrics(numOfTrendingTopicsPopularityDetector,cluster,job_id,verticeIdTrendingTopicsPopularityDetector,TrendingTopicsPopularityDetector_name)
    dictCombo.update(dictTrendingTopicsPopularityDetector)
        
    
    return dictCombo

def getMachineOutlier(jsonVertice, cluster, job_id):
    verticeIdMachineUsageParser = None
    verticeIdMachineUsageGrouper = None
    verticeIdOutlierDetector = None
    
    dictMachineUsageParser = {}
    dictMachineUsageGrouper = {}
    dictOutlierDetector = {}
    
    dictCombo = {}
    jobName = jsonVertice["name"]
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "machine-usage-parser" in vertice["name"]:
                    #print(vertice)
                MachineUsageParser_name = "machine-usage-parser"
                verticeIdMachineUsageParser = vertice["id"] 
                numOfMachineUsageParser = int(vertice["parallelism"])
            elif "name" in vertice and "machine-usage-grouper" in vertice["name"]:
                MachineUsageGrouper_name = "machine-usage-grouper"
                verticeIdMachineUsageGrouper = vertice["id"]
                numOfMachineUsageGrouper = int(vertice["parallelism"])
            elif "name" in vertice and "outlier-detector" in vertice["name"]:
                OutlierDetector_name = "outlier-detector"
                verticeIdOutlierDetector = vertice["id"]
                numOfOutlierDetector = int(vertice["parallelism"])
            
    job_dict = {"job_name": jobName}
    dictCombo = job_dict.copy()

    dictMachineUsageParser = getOperatorMetrics(numOfMachineUsageParser,cluster,job_id,verticeIdMachineUsageParser,MachineUsageParser_name)
    dictCombo.update(dictMachineUsageParser)

    dictMachineUsageGrouper = getOperatorMetrics(numOfMachineUsageGrouper,cluster,job_id,verticeIdMachineUsageGrouper,MachineUsageGrouper_name)
    dictCombo.update(dictMachineUsageGrouper)

    dictOutlierDetector = getOperatorMetrics(numOfOutlierDetector,cluster,job_id,verticeIdOutlierDetector,OutlierDetector_name)
    dictCombo.update(dictOutlierDetector)
        
    
    return dictCombo


def getLinearRoad(jsonVertice, cluster, job_id):
    verticeIdVehicleEventParser = None
    verticeIdTollNotification = None
    verticeIdFormatterTollNotification = None
    verticeIdAccidentNotification = None
    verticeIdFormatterAccidentNotification = None
    verticeIdDailyExpenditure = None
    verticeIdVehicleReportMapper = None


    dictVehicleEventParser = {}
    dictTollNotification = {}
    dictFormatterTollNotification = {}
    dictAccidentNotification = {}
    dictFormatterAccidentNotification = {}
    dictDailyExpenditure = {}
    dictVehicleReportMapper = {}
    
    dictCombo = {}
    jobName = jsonVertice["name"]
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "Vehicle-event-parser" in vertice["name"]:
                VehicleEventParser_name = "Vehicle-event-parser"
                verticeIdVehicleEventParser = vertice["id"] 
                numOfVehicleEventParser = int(vertice["parallelism"])
            elif "name" in vertice and "toll-notification" in vertice["name"]:
                TollNotification_name = "toll-notification"
                verticeIdTollNotification = vertice["id"]
                numOfTollNotification = int(vertice["parallelism"])
            elif "name" in vertice and "formatter-toll-notification" in vertice["name"]:
                FormatterTollNotification_name = "formatter-toll-notification"
                verticeIdFormatterTollNotification = vertice["id"]
                numOfFormatterTollNotification = int(vertice["parallelism"])
            elif "name" in vertice and "accident-notification" in vertice["name"]:
                AccidentNotification_name = "accident-notification"
                verticeIdAccidentNotification = vertice["id"]
                numOfAccidentNotification = int(vertice["parallelism"])
            elif "name" in vertice and "formatter-accident-notification" in vertice["name"]:
                FormatterAccidentNotification_name = "formatter-accident-notification"
                verticeIdFormatterAccidentNotification = vertice["id"]
                numOfFormatterAccidentNotification = int(vertice["parallelism"])
            elif "name" in vertice and "daily-expenditure" in vertice["name"]:
                DailyExpenditure_name = "daily-expenditure"
                verticeIdDailyExpenditure = vertice["id"]
                numOfDailyExpenditure = int(vertice["parallelism"])
            elif "name" in vertice and "vehicle-report-mapper" in vertice["name"]:
                VehicleReportMapper_name = "vehicle-report-mapper"
                verticeIdVehicleReportMapper = vertice["id"]
                numOfVehicleReportMapper = int(vertice["parallelism"])
            
    job_dict = {"job_name": jobName}
    dictCombo = job_dict.copy()

    dictVehicleEventParser = getOperatorMetrics(numOfVehicleEventParser, cluster, job_id, verticeIdVehicleEventParser, VehicleEventParser_name)
    dictCombo.update(dictVehicleEventParser)
    if verticeIdTollNotification is not None:
        dictTollNotification = getOperatorMetrics(numOfTollNotification, cluster, job_id, verticeIdTollNotification, TollNotification_name)
        dictCombo.update(dictTollNotification)

    if verticeIdFormatterTollNotification is not None:
        dictFormatterTollNotification = getOperatorMetrics(numOfFormatterTollNotification, cluster, job_id, verticeIdFormatterTollNotification, FormatterTollNotification_name)
        dictCombo.update(dictFormatterTollNotification)

    if verticeIdAccidentNotification is not None:
        dictAccidentNotification = getOperatorMetrics(numOfAccidentNotification, cluster, job_id, verticeIdAccidentNotification, AccidentNotification_name)
        dictCombo.update(dictAccidentNotification)

    if verticeIdFormatterAccidentNotification is not None:
        dictFormatterAccidentNotification = getOperatorMetrics(numOfFormatterAccidentNotification, cluster, job_id, verticeIdFormatterAccidentNotification, FormatterAccidentNotification_name)
        dictCombo.update(dictFormatterAccidentNotification)
    if verticeIdDailyExpenditure is not None:
        dictDailyExpenditure = getOperatorMetrics(numOfDailyExpenditure, cluster, job_id, verticeIdDailyExpenditure, DailyExpenditure_name)
        dictCombo.update(dictDailyExpenditure)
    if verticeIdVehicleReportMapper is not None:
        dictVehicleReportMapper = getOperatorMetrics(numOfVehicleReportMapper, cluster, job_id, verticeIdVehicleReportMapper, VehicleReportMapper_name)
        dictCombo.update(dictVehicleReportMapper)
        
    
    return dictCombo

def getTrafficMonitoring(jsonVertice, cluster, job_id):
    print("Reached Traffic monitoring")
    verticeIdTrafficEventParser = None
    verticeIdRoadMatcher = None
    verticeIdAvgSpeed = None
    verticeIdFormatter = None
    
    dictTrafficEventParser = {}
    dictRoadMatcher = {}
    dictAvgSpeed = {}
    dictFormatter = {}
    
    dictCombo = {}
    jobName = jsonVertice["name"]
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "traffic-event-parser" in vertice["name"]:
                TrafficEventParser_name = "traffic-event-parser"
                verticeIdTrafficEventParser = vertice["id"] 
                numOfTrafficEventParser = int(vertice["parallelism"])
            elif "name" in vertice and "road-matcher" in vertice["name"]:
                RoadMatcher_name = "road-matcher"
                verticeIdRoadMatcher = vertice["id"]
                numOfRoadMatcher = int(vertice["parallelism"])
            elif "name" in vertice and "avg-speed" in vertice["name"]:
                AvgSpeed_name = "avg-speed"
                verticeIdAvgSpeed = vertice["id"]
                numOfAvgSpeed = int(vertice["parallelism"])
            elif "name" in vertice and "formatter" in vertice["name"]:
                Formatter_name = "formatter"
                verticeIdFormatter = vertice["id"]
                numOfFormatter = int(vertice["parallelism"])
            
    job_dict = {"job_name": jobName}
    dictCombo = job_dict.copy()

    dictTrafficEventParser = getOperatorMetrics(numOfTrafficEventParser,cluster,job_id,verticeIdTrafficEventParser,TrafficEventParser_name)
    dictCombo.update(dictTrafficEventParser)

    dictRoadMatcher = getOperatorMetrics(numOfRoadMatcher,cluster,job_id,verticeIdRoadMatcher,RoadMatcher_name)
    dictCombo.update(dictRoadMatcher)

    dictAvgSpeed = getOperatorMetrics(numOfAvgSpeed,cluster,job_id,verticeIdAvgSpeed,AvgSpeed_name)
    dictCombo.update(dictAvgSpeed)

    dictFormatter = getOperatorMetrics(numOfFormatter,cluster,job_id,verticeIdFormatter,Formatter_name)
    dictCombo.update(dictFormatter)
        
    
    return dictCombo

def getTpch(jsonVertice, cluster, job_id):
   
    verticeIdTpchEventParser = None
    verticeIdTpchDataFilter = None
    verticeIdTpchFlatMapper = None
    verticeIdPriorityCounter = None
    verticeIdFormatter = None
    
    dictTpchEventParser = {}
    dictTpchDataFilter = {}
    dictTpchFlatMapper = {}
    dictPriorityCounter = {}
    dictFormatter = {}

    
    
    dictCombo = {}
    jobName = jsonVertice["name"]
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "tpch-event-parser" in vertice["name"]:
                TpchEventParser_name = "tpch-event-parser"
                verticeIdTpchEventParser = vertice["id"] 
                numOfTpchEventParser = int(vertice["parallelism"])
            elif "name" in vertice and "tpch-data-filter" in vertice["name"]:
                TpchDataFilter_name = "tpch-data-filter"
                verticeIdTpchDataFilter = vertice["id"]
                numOfTpchDataFilter = int(vertice["parallelism"])
            elif "name" in vertice and "tpch-flat-mapper" in vertice["name"]:
                TpchFlatMapper_name = "tpch-flat-mapper"
                verticeIdTpchFlatMapper = vertice["id"]
                numOfTpchFlatMapper = int(vertice["parallelism"])    
            elif "name" in vertice and "priority-counter" in vertice["name"]:
                PriorityCounter_name = "priority-counter"
                verticeIdPriorityCounter = vertice["id"]
                numOfPriorityCounter = int(vertice["parallelism"])
            elif "name" in vertice and "formatter" in vertice["name"]:
                Formatter_name = "formatter"
                verticeIdFormatter = vertice["id"]
                numOfFormatter = int(vertice["parallelism"])
            
            
    job_dict = {"job_name": jobName}
    dictCombo = job_dict.copy()

    dictTpchEventParser = getOperatorMetrics(numOfTpchEventParser,cluster,job_id,verticeIdTpchEventParser,TpchEventParser_name)
    dictCombo.update(dictTpchEventParser)

    dictTpchDataFilter = getOperatorMetrics(numOfTpchDataFilter,cluster,job_id,verticeIdTpchDataFilter,TpchDataFilter_name)
    dictCombo.update(dictTpchDataFilter)

    dictTpchFlatMapper = getOperatorMetrics(numOfTpchFlatMapper,cluster,job_id,verticeIdTpchFlatMapper,TpchFlatMapper_name)
    dictCombo.update(dictTpchFlatMapper)

    dictPriorityCounter = getOperatorMetrics(numOfPriorityCounter,cluster,job_id,verticeIdPriorityCounter,PriorityCounter_name)
    dictCombo.update(dictPriorityCounter)

    dictFormatter = getOperatorMetrics(numOfFormatter,cluster,job_id,verticeIdFormatter,Formatter_name)
    dictCombo.update(dictFormatter)
        
    return dictCombo


def getLogsProcessing(jsonVertice, cluster, job_id):
    verticeIdLogProcessorParser = None
    verticeIdLogProcessorVolumeCounter = None
    verticeIdLogProcessorStatusCounter = None
    
    dictLogProcessorParser = {}
    dictLogProcessorVolumeCounter = {}
    dictLogProcessorStatusCounter = {}
    
    dictCombo = {}
    jobName = jsonVertice["name"]
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "Log-parser" in vertice["name"]:
                LogProcessorParser_name = "Log-parser"
                verticeIdLogProcessorParser = vertice["id"] 
                numOfLogProcessorParser = int(vertice["parallelism"])
            elif "name" in vertice and "volume-counter" in vertice["name"]:
                LogProcessorVolumeCounter_name = "volume-counter"
                verticeIdLogProcessorVolumeCounter = vertice["id"]
                numOfLogProcessorVolumeCounter = int(vertice["parallelism"])
            elif "name" in vertice and "status-counter" in vertice["name"]:
                LogProcessorStatusCounter_name = "status-counter"
                verticeIdLogProcessorStatusCounter = vertice["id"]
                numOfLogProcessorStatusCounter = int(vertice["parallelism"])
            
    job_dict = {"job_name": jobName}
    dictCombo = job_dict.copy()

    dictLogProcessorParser = getOperatorMetrics(numOfLogProcessorParser, cluster, job_id, verticeIdLogProcessorParser, LogProcessorParser_name)
    dictCombo.update(dictLogProcessorParser)
    if verticeIdLogProcessorVolumeCounter is not None:
        dictLogProcessorVolumeCounter = getOperatorMetrics(numOfLogProcessorVolumeCounter, cluster, job_id, verticeIdLogProcessorVolumeCounter, LogProcessorVolumeCounter_name)
        dictCombo.update(dictLogProcessorVolumeCounter)

    if verticeIdLogProcessorStatusCounter is not None:
        dictLogProcessorStatusCounter = getOperatorMetrics(numOfLogProcessorStatusCounter, cluster, job_id, verticeIdLogProcessorStatusCounter, LogProcessorStatusCounter_name)
        dictCombo.update(dictLogProcessorStatusCounter)
        
    
    return dictCombo

def getBargainIndex(jsonVertice, cluster, job_id):
    verticeIdBargainIndexParser = None
    verticeIdBargainIndexVWAP = None
    verticeIdBargainIndexCalc = None
    
    dictBargainIndexParser = {}
    dictBargainIndexVWAP = {}
    dictBargainIndexCalc = {}
    
    dictCombo = {}
    jobName = jsonVertice["name"]
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "quote-parser" in vertice["name"]:
                BargainIndexParser_name = "quote-parser"
                verticeIdBargainIndexParser = vertice["id"] 
                numOfBargainIndexParser = int(vertice["parallelism"])
            elif "name" in vertice and "VWAP-operator" in vertice["name"]:
                BargainIndexVWAP_name = "VWAP-operator"
                verticeIdBargainIndexVWAP = vertice["id"]
                numOfBargainIndexVWAP = int(vertice["parallelism"])
            elif "name" in vertice and "bargain-index-calculator" in vertice["name"]:
                BargainIndexCalc_name = "bargain-index-calculator"
                verticeIdBargainIndexCalc = vertice["id"]
                numOfBargainIndexCalc = int(vertice["parallelism"])
            
    job_dict = {"job_name": jobName}
    dictCombo = job_dict.copy()

    dictBargainIndexParser = getOperatorMetrics(numOfBargainIndexParser,cluster,job_id,verticeIdBargainIndexParser,BargainIndexParser_name)
    dictCombo.update(dictBargainIndexParser)

    dictBargainIndexVWAP = getOperatorMetrics(numOfBargainIndexVWAP,cluster,job_id,verticeIdBargainIndexVWAP,BargainIndexVWAP_name)
    dictCombo.update(dictBargainIndexVWAP)

    dictBargainIndexCalc = getOperatorMetrics(numOfBargainIndexCalc,cluster,job_id,verticeIdBargainIndexCalc,BargainIndexCalc_name)
    dictCombo.update(dictBargainIndexCalc)
        
    
    return dictCombo

def getClickAnalytics(jsonVertice, cluster, job_id):
    verticeIdClickAnalyticsParser = None
    verticeIdClickAnalyticsRepeat = None
    verticeIdClickAnalyticsReduce = None
    verticeIdClickAnalyticsGeo = None
    
    dictClickAnalyticsParser = {}
    dictClickAnalyticsRepeat = {}
    dictClickAnalyticsReduce = {}
    dictClickAnalyticsGeo = {}

    dictCombo = {}
    jobName = jsonVertice["name"]
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "click-log-parser" in vertice["name"]:
                ClickAnalyticsParser_name = "click-log-parser"
                verticeIdClickAnalyticsParser = vertice["id"] 
                numOfClickAnalyticsParser = int(vertice["parallelism"])
            elif "name" in vertice and "repeat-visit" in vertice["name"]:
                ClickAnalyticsRepeat_name = "repeat-visit"
                verticeIdClickAnalyticsRepeat = vertice["id"]
                numOfClickAnalyticsRepeat = int(vertice["parallelism"])
            elif "name" in vertice and "reduce-operation" in vertice["name"]:
                ClickAnalyticsReduce_name = "reduce-operation"
                verticeIdClickAnalyticsReduce = vertice["id"]
                numOfClickAnalyticsReduce = int(vertice["parallelism"])
            elif "name" in vertice and "geography-visit" in vertice["name"]:
                ClickAnalyticsGeo_name = "geography-visit"
                verticeIdClickAnalyticsGeo = vertice["id"]
                numOfClickAnalyticsGeo = int(vertice["parallelism"])
            
    job_dict = {"job_name": jobName}
    dictCombo = job_dict.copy()

    if verticeIdClickAnalyticsParser is not None:
        dictClickAnalyticsParser = getOperatorMetrics(numOfClickAnalyticsParser,cluster,job_id,verticeIdClickAnalyticsParser,ClickAnalyticsParser_name)
        dictCombo.update(dictClickAnalyticsParser)

    if verticeIdClickAnalyticsRepeat is not None:
        dictClickAnalyticsRepeat = getOperatorMetrics(numOfClickAnalyticsRepeat,cluster,job_id,verticeIdClickAnalyticsRepeat,ClickAnalyticsRepeat_name)
        dictCombo.update(dictClickAnalyticsRepeat)

    if verticeIdClickAnalyticsReduce is not None:
        dictClickAnalyticsReduce = getOperatorMetrics(numOfClickAnalyticsReduce,cluster,job_id,verticeIdClickAnalyticsReduce,ClickAnalyticsReduce_name)
        dictCombo.update(dictClickAnalyticsReduce)

    if verticeIdClickAnalyticsGeo is not None:
        dictClickAnalyticsGeo = getOperatorMetrics(numOfClickAnalyticsGeo,cluster,job_id,verticeIdClickAnalyticsGeo,ClickAnalyticsGeo_name)
        dictCombo.update(dictClickAnalyticsGeo)
        
    
    return dictCombo


def getSpikeDetection(jsonVertice, cluster, job_id):
    verticeIdSpikeParser = None
    verticeIdAvgCal = None
    verticeIdSpikeDetector = None
    
    dictSpikeParser = {}
    dictAvgCal = {}
    dictSpikeDetector = {}
    
    dictCombo = {}
    jobName = jsonVertice["name"]
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "parser" in vertice["name"]:
                SpikeParser_name = "parser"
                verticeIdSpikeParser = vertice["id"] 
                numOfSpikeParser = int(vertice["parallelism"])
            elif "name" in vertice and "average-calculator" in vertice["name"]:
                AvgCal_name = "average-calculator"
                verticeIdAvgCal = vertice["id"]
                numOfAvgCal = int(vertice["parallelism"])
            elif "name" in vertice and "spike-detector" in vertice["name"]:
                SpikeDetector_name = "spike-detector"
                verticeIdSpikeDetector = vertice["id"]
                numOfSpikeDetector = int(vertice["parallelism"])
            
    job_dict = {"job_name": jobName}
    dictCombo = job_dict.copy()

    dictSpikeParser = getOperatorMetrics(numOfSpikeParser,cluster,job_id,verticeIdSpikeParser,SpikeParser_name)
    dictCombo.update(dictSpikeParser)

    dictAvgCal = getOperatorMetrics(numOfAvgCal,cluster,job_id,verticeIdAvgCal,AvgCal_name)
    dictCombo.update(dictAvgCal)

    dictSpikeDetector = getOperatorMetrics(numOfSpikeDetector,cluster,job_id,verticeIdSpikeDetector,SpikeDetector_name)
    dictCombo.update(dictSpikeDetector)
        
    
    return dictCombo

def getSentimentAnalysis(jsonVertice, cluster, job_id):

    verticeIdTwitterParser = None
    verticeIdTwitterAnalyser = None
    
    dictTwitterParser = {}
    dictTwitterAnalyser = {}
    
    dictCombo = {}
    jobName = jsonVertice["name"]
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "twitter-parser" in vertice["name"]:
                TwitterParser_name = "twitter-parser"
                verticeIdTwitterParser = vertice["id"] 
                numOfTwitterParser = int(vertice["parallelism"])
            elif "name" in vertice and "twitter-analyser" in vertice["name"]:
                TwitterAnalyser_name = "twitter-analyser"
                verticeIdTwitterAnalyser = vertice["id"]
                numOfTwitterAnalyser = int(vertice["parallelism"])
            
    job_dict = {"job_name": jobName}
    dictCombo = job_dict.copy()

    dictTwitterParser = getOperatorMetrics(numOfTwitterParser,cluster,job_id,verticeIdTwitterParser,TwitterParser_name)
    dictCombo.update(dictTwitterParser)

    dictTwitterAnalyser = getOperatorMetrics(numOfTwitterAnalyser,cluster,job_id,verticeIdTwitterAnalyser,TwitterAnalyser_name)
    dictCombo.update(dictTwitterAnalyser)
        
    
    return dictCombo

def getGoogleCloudmonitoringMetrics(jsonVertice, cluster, job_id):
    verticeIdParser = None
    verticeIdAvgCpuPerCat = None
    verticeIdAvgCpuPerJob = None
    dictParser = {}
    dictAvgCpuPerCat = {}
    dictAvgCpuPerJob = {}
    dictCombo = {}
    jobName = jsonVertice["name"]
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "parser" in vertice["name"]:
                Parser_name = "parser"
                verticeIdParser = vertice["id"] 
                numOfParser = int(vertice["parallelism"])
            elif "name" in vertice and "average-cpu-per-category" in vertice["name"]:
                AvgCpuPerCat_name = "average-cpu-per-category"
                verticeIdAvgCpuPerCat = vertice["id"]
                numOfAvgCpuPerCat = int(vertice["parallelism"])
            elif "name" in vertice and "average-cpu-per-job" in vertice["name"]:
                AvgCpuPerJob_name = "average-cpu-per-job"
                verticeIdAvgCpuPerJob = vertice["id"]
                numOfAvgCpuPerJob = int(vertice["parallelism"])
    job_dict = {"job_name": jobName}
    dictCombo = job_dict.copy()
    dictParser = getOperatorMetrics(numOfParser,cluster,job_id,verticeIdParser,Parser_name)
    dictCombo.update(dictParser)

    if verticeIdAvgCpuPerCat is not None:
        dictAvgCpuPerCat = getOperatorMetrics(numOfAvgCpuPerCat,cluster,job_id,verticeIdAvgCpuPerCat,AvgCpuPerCat_name)
        dictCombo.update(dictAvgCpuPerCat)
        
    if verticeIdAvgCpuPerJob is not None:
        dictAvgCpuPerJob = getOperatorMetrics(numOfAvgCpuPerJob,cluster,job_id,verticeIdAvgCpuPerJob,AvgCpuPerJob_name)
        dictCombo.update(dictAvgCpuPerJob)
    
    return dictCombo

def getAdanalytics(jsonVertice, cluster, job_id):
    verticeIdClickParser = None
    verticeIdImpressionParser = None
    verticeIdClicksCounter = None
    verticeIdImpressionsCounter = None
    verticeIdRollingCTR = None
    print("Ad Analytics")
    dictClickParser = {}
    dictImpressionParser = {}
    dictClicksCounter = {}
    dictImpressionsCounter = {}
    dictRollingCTR = {}

    dictCombo = {}
    jobName = jsonVertice["name"]
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "click-parser" in vertice["name"]:
                ClickParser_name = "click-parser"
                verticeIdClickParser = vertice["id"] 
                numOfClickParser = int(vertice["parallelism"])
            elif "name" in vertice and "impression-parser" in vertice["name"]:
                ImpressionParser_name = "impression-parser"
                verticeIdImpressionParser = vertice["id"]
                numOfImpressionParser = int(vertice["parallelism"])
            elif "name" in vertice and "clicks-counter" in vertice["name"]:
                ClicksCounter_name = "clicks-counter"
                verticeIdClicksCounter = vertice["id"]
                numOfClicksCounter = int(vertice["parallelism"])
            elif "name" in vertice and "impressions-counter" in vertice["name"]:
                ImpressionsCounter_name = "impressions-counter"
                verticeIdImpressionsCounter = vertice["id"]
                numOfImpressionsCounter = int(vertice["parallelism"])
            elif "name" in vertice and "rollingCTR" in vertice["name"]:
                RollingCTR_name = "rollingCTR"
                verticeIdRollingCTR = vertice["id"]
                numOfRollingCTR = int(vertice["parallelism"])

    job_dict = {"job_name": jobName}
    dictCombo = job_dict.copy()
    dictClickParser = getOperatorMetrics(numOfClickParser,cluster,job_id,verticeIdClickParser,ClickParser_name)
    dictImpressionParser = getOperatorMetrics(numOfImpressionParser,cluster,job_id,verticeIdImpressionParser,ImpressionParser_name)
    dictClicksCounter = getOperatorMetrics(numOfClicksCounter,cluster,job_id,verticeIdClicksCounter,ClicksCounter_name)
    dictImpressionsCounter = getOperatorMetrics(numOfImpressionsCounter,cluster,job_id,verticeIdImpressionsCounter,ImpressionsCounter_name)
    dictRollingCTR = getOperatorMetrics(numOfRollingCTR,cluster,job_id,verticeIdRollingCTR,RollingCTR_name)

    dictCombo.update(dictClickParser)
    dictCombo.update(dictImpressionParser)
    dictCombo.update(dictClicksCounter)
    dictCombo.update(dictImpressionsCounter)
    dictCombo.update(dictRollingCTR)
        
   
    
    return dictCombo
    
def getSmartGrid(jsonVertice, cluster, job_id):
    verticeIdglobalavgload = None
    verticeIdlocalavgload = None
    dictGlobalload = {}
    dictLocalload = {}
    dictCombo = {}
    jobName = jsonVertice["name"]
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "global average load" in vertice["name"]:
                globalAvgLoad_name = "global average load"
                verticeIdglobalavgload = vertice["id"] 
                numOfGlobalAvgLoad = int(vertice["parallelism"])
            elif "name" in vertice and "local average load" in vertice["name"]:
                localAvgLoad_name = "local average load"
                verticeIdlocalavgload = vertice["id"]
                numOfLocalAvgLoad = int(vertice["parallelism"])
    job_dict = {"job_name": jobName}
    dictCombo = job_dict.copy()
    if verticeIdglobalavgload is not None:
        dictGlobalload = getOperatorMetrics(numOfGlobalAvgLoad,cluster,job_id,verticeIdglobalavgload,globalAvgLoad_name)
        dictCombo.update(dictGlobalload)
        
    if verticeIdlocalavgload is not None:
        dictLocalload = getOperatorMetrics(numOfLocalAvgLoad,cluster,job_id,verticeIdlocalavgload,localAvgLoad_name)
        dictCombo.update(dictLocalload)
    
    return dictCombo

def getWordCount(jsonVertice, cluster, job_id):
    
    verticeIdtokenizer = None
    verticeIdcounter = None
    dictTokenizer = {}
    dictCounter = {}
    dictCombo = {}
    jobName = jsonVertice["name"]
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "tokenizer" in vertice["name"]:
                tokenizer_name = "tokenizer"
                verticeIdtokenizer = vertice["id"] 
                numOfTokenizer = int(vertice["parallelism"])
            elif "name" in vertice and "counter" in vertice["name"]:
                counter_name = "counter"
                verticeIdcounter = vertice["id"]
                numOfCounter = int(vertice["parallelism"])
    dictTokenizer = getOperatorMetrics(numOfTokenizer,cluster,job_id,verticeIdtokenizer,tokenizer_name)

    dictCounter = getOperatorMetrics(numOfCounter,cluster,job_id,verticeIdcounter,counter_name)

    job_dict = {"job_name": jobName}

    dictCombo = job_dict.copy()
    
    dictCombo.update(dictTokenizer)
    dictCombo.update(dictCounter)

    return dictCombo

class GetJobMetrics(View):

    @staticmethod
    def get(request, **kwargs):
        response_status = 200
        cluster_id = kwargs["cluster_id"]
        job_id = kwargs["job_id"]
        print("Job id is " + job_id)
        print("Cluster id is"+ cluster_id)
        try:
            cluster_obj = Cluster.objects.get(id=cluster_id)
        except Exception as e: 
            print(e)
            return JsonResponse(e, status=response_status, safe=False)
        print("Job id is " + job_id)
        print("Cluster id is"+ cluster_id)
        #if wordcount
        
        cluster = cluster_obj.main_node_ip
        verticeResponse = requests.get("http://"+ cluster + ":8086/v1/jobs/"+job_id)
        jsonVertice = verticeResponse.json()

        if jsonVertice["name"] == 'Google Cloud Monitoring':
            processedMetrics = getGoogleCloudmonitoringMetrics(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == 'Ads Analytics':
            processedMetrics = getAdanalytics(jsonVertice, cluster, job_id)    
        elif jsonVertice["name"] == 'Flink smart grid job':
            processedMetrics = getSmartGrid(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == 'Flink word count job':
            processedMetrics = getWordCount(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Sentiment Analysis":
            processedMetrics = getSentimentAnalysis(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Spike Detection":
            processedMetrics = getSpikeDetection(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Trending Topics":
            processedMetrics = getTrendingTopics(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Logs Processing":
            processedMetrics = getLogsProcessing(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Bargain Index":
            processedMetrics = getBargainIndex(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Click Analytics":
            processedMetrics = getClickAnalytics(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Linear Road":
            processedMetrics = getLinearRoad(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Machine Outlier":
            processedMetrics = getMachineOutlier(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Traffic Monitoring":
            processedMetrics = getTrafficMonitoring(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "TPCH":
            processedMetrics = getTpch(jsonVertice, cluster, job_id)
        
        if "vertices" in jsonVertice:
            for vertice in jsonVertice["vertices"]:
                if "name" in vertice and "kafka-sink: Writer" in vertice["name"]:
                    verticeIdSink = vertice["id"]
                if "name" in vertice and "Source: kafka-source" in vertice["name"]:
                    verticeIdSource = vertice["id"]
                    

        #framing endpoint addresses for Source 
        
        numRecordsOutSource = cluster + ":8086/v1/jobs/"+job_id + "/vertices/" + verticeIdSource + "/metrics?get=0.numRecordsOut"
        recordsOutPerSecondSource = cluster + ":8086/v1/jobs/"+job_id + "/vertices/" + verticeIdSource + "/metrics?get=0.numRecordsOutPerSecond"
        
        #calling end point for Source metrics
        responserecordsOutPerSecondSource = requests.get("http://"+recordsOutPerSecondSource)
        jsonrecordsOutPerSecondSource = responserecordsOutPerSecondSource.json()
        
        #framing endpoint addresses for Sink
        numRecordsInSink = cluster + ":8086/v1/jobs/"+job_id + "/vertices/" + verticeIdSink + "/metrics?get=0.numRecordsIn"
        recordsPerSecondOutSink = cluster + ":8086/v1/jobs/"+job_id + "/vertices/" + verticeIdSink + "/metrics?get=0.numRecordsOutPerSecond"

        #calling end point for Sink metrics
        responseRecordsPerSecondOutSink = requests.get("http://"+recordsPerSecondOutSink)
        jsonRecordsPerSecondOutSink = responseRecordsPerSecondOutSink.json()
       
        #calculating end to end latency of any job
        while True:
            responseNumRecordsOutSource = requests.get("http://"+numRecordsOutSource)
            jsonNumRecordsOutSource = responseNumRecordsOutSource.json()
            print(jsonNumRecordsOutSource)
            if len(jsonNumRecordsOutSource) > 0 and "value" in jsonNumRecordsOutSource[0]:
                startDateTime = datetime.now()
                break
        
        while True:
            responseNumRecordsInSink = requests.get("http://"+numRecordsInSink)
            jsonNumRecordsInSink = responseNumRecordsInSink.json()
                
            if len(jsonNumRecordsInSink) > 0 and "value" in jsonNumRecordsInSink[0]:
                endDateTime = datetime.now()
                break

        latency = endDateTime - startDateTime
        jsonlatency = str(latency)
                
        combined_data = {'persecondoutsink':jsonRecordsPerSecondOutSink[0], 'persecondoutsource':jsonrecordsOutPerSecondSource[0], 'latency':jsonlatency}
        combined_data.update(processedMetrics)
        json_data = json.dumps(combined_data)
        print(f"json_data is {json_data}")

        return JsonResponse(json.dumps(json_data), status=response_status, safe=False) 
    
class GetHistoricalMetrics(View):

    @staticmethod
    def get(request, **kwargs):
        response_status = 200
        cluster_id = kwargs["cluster_id"]
        job_id = kwargs["job_id"]
        print("Job id is " + job_id)
        print("Cluster id is"+ cluster_id)
        try:
            cluster_obj = Cluster.objects.get(id=cluster_id)
        except Exception as e: 
            print(e)
            return JsonResponse(e, status=response_status, safe=False)
        print("Job id is " + job_id)
        print("Cluster id is"+ cluster_id)
        
        cluster = cluster_obj.main_node_ip
        verticeResponse = requests.get("http://"+ cluster + ":8086/v1/jobs/"+job_id)
        jsonVertice = verticeResponse.json()

        if jsonVertice["name"] == 'Google Cloud Monitoring':
            processedMetrics = getGoogleCloudmonitoringMetrics(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == 'Ads Analytics':
            processedMetrics = getAdanalytics(jsonVertice, cluster, job_id)    
        elif jsonVertice["name"] == 'Flink smart grid job':
            processedMetrics = getSmartGrid(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == 'Flink word count job':
            processedMetrics = getWordCount(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Sentiment Analysis":
            processedMetrics = getSentimentAnalysis(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Spike Detection":
            processedMetrics = getSpikeDetection(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Trending Topics":
            processedMetrics = getTrendingTopics(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Logs Processing":
            processedMetrics = getLogsProcessing(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Bargain Index":
            processedMetrics = getBargainIndex(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Click Analytics":
            processedMetrics = getClickAnalytics(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Linear Road":
            processedMetrics = getLinearRoad(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Machine Outlier":
            processedMetrics = getTrafficMonitoring(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "Traffic Monitoring":
            processedMetrics = getMachineOutlier(jsonVertice, cluster, job_id)
        elif jsonVertice["name"] == "TPCH":
            processedMetrics = getTpch(jsonVertice, cluster, job_id)

        if "vertices" in jsonVertice:
            for vertice in jsonVertice["vertices"]:
                if "name" in vertice and "kafka-sink: Writer" in vertice["name"]:
                    verticeIdSink = vertice["id"]
                if "name" in vertice and "Source: kafka-source" in vertice["name"]:
                    verticeIdSource = vertice["id"]
                    

        #framing endpoint addresses for Source 
        
        numRecordsOutSource = cluster + ":8086/v1/jobs/"+job_id + "/vertices/" + verticeIdSource + "/metrics?get=0.numRecordsOut"
        recordsOutPerSecondSource = cluster + ":8086/v1/jobs/"+job_id + "/vertices/" + verticeIdSource + "/metrics?get=0.numRecordsOutPerSecond"
        
        #calling end point for Source metrics
        responserecordsOutPerSecondSource = requests.get("http://"+recordsOutPerSecondSource)
        jsonrecordsOutPerSecondSource = responserecordsOutPerSecondSource.json()
        
        #framing endpoint addresses for Sink
        numRecordsInSink = cluster + ":8086/v1/jobs/"+job_id + "/vertices/" + verticeIdSink + "/metrics?get=0.numRecordsIn"
        recordsPerSecondOutSink = cluster + ":8086/v1/jobs/"+job_id + "/vertices/" + verticeIdSink + "/metrics?get=0.numRecordsOutPerSecond"
        
        #calling end point for Sink metrics
        responseRecordsPerSecondOutSink = requests.get("http://"+recordsPerSecondOutSink)
        jsonRecordsPerSecondOutSink = responseRecordsPerSecondOutSink.json()
       
        #calculating end to end latency of any job
        while True:
            responseNumRecordsOutSource = requests.get("http://"+numRecordsOutSource)
            jsonNumRecordsOutSource = responseNumRecordsOutSource.json()
            print(jsonNumRecordsOutSource)
            if len(jsonNumRecordsOutSource) > 0 and "value" in jsonNumRecordsOutSource[0]:
                startDateTime = datetime.now()
                break
        
        while True:
            responseNumRecordsInSink = requests.get("http://"+numRecordsInSink)
            jsonNumRecordsInSink = responseNumRecordsInSink.json()
                
            if len(jsonNumRecordsInSink) > 0 and "value" in jsonNumRecordsInSink[0]:
                endDateTime = datetime.now()
                break

        latency = endDateTime - startDateTime
        jsonlatency = str(latency)
        
        combined_data = {'persecondoutsink':jsonRecordsPerSecondOutSink[0], 'persecondoutsource':jsonrecordsOutPerSecondSource[0], 'latency':jsonlatency}
        combined_data.update(processedMetrics)
        json_data = json.dumps(combined_data)
        print(f"json_data is {json_data}")

        return JsonResponse(json.dumps(json_data), status=response_status, safe=False) 

class GetIndividualGraphData(View):
    @staticmethod
    def post(request):
        response_status = 200
        selections = json.loads(request.body)
        #print(selections)
        main_node = selections['cluster_main_node_ip']
        jobId = selections['selected_jobId']
        analysisOf = selections['selected_analysis_type']
        print(main_node)
        print(jobId)
        print(analysisOf)
        requested_cluster_jobs = requests.get("http://"+main_node+":8086/v1/jobs/"+jobId)
        cluster_jobs_json = requested_cluster_jobs.json()
        fullJobName = cluster_jobs_json["name"]
        cutjobId = jobId[0:4]
        cutJobName = fullJobName[0:3]
        givenName = cutJobName + '-' + cutjobId
        timestamp_prom = (cluster_jobs_json["start-time"]) // 1000
        timestamp_prom = timestamp_prom + 500
        timestamp_prom = str(timestamp_prom)
        
        print(timestamp_prom)
        
        hwtype_filepath = os.path.abspath(os.path.join(settings.BASE_DIR, '../dsp_be/hwtype.txt'))
        with open(hwtype_filepath, 'r') as file:
            content = file.read()

        if '=' in content:
            key, hwvalue = content.split('=')
            key = key.strip()
            hwvalue = hwvalue.strip()
            print(f"The value of '{key}' is '{hwvalue}'")
        else:
            print("Invalid format in the file.")

        if analysisOf == 'Entire Query':
            queryMetr = selections['selected_query_metrics']
            print(queryMetr)
            if queryMetr == 'Throughput':
    
                print('inside throughput')
                prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=flink_taskmanager_job_task_operator_numRecordsInPerSecond{job_id=\"" + jobId + "\" ,operator_name='kafka_sink:_Writer'}[5m] @ " +timestamp_prom
                print(prom_endpoint)
                throughput_response = requests.get(prom_endpoint)
                data =throughput_response.json()
                return JsonResponse(json.dumps(data),status=response_status, safe=False)
            elif queryMetr == 'CPU Utilization':
                prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=flink_taskmanager_System_CPU_Load15min[5m] @ " +timestamp_prom
                print(prom_endpoint)
                cpu_response = requests.get(prom_endpoint)
                data = cpu_response.json()
                print(data)
                return JsonResponse(json.dumps(data),status=response_status, safe=False)
            elif queryMetr == 'N/W Utilization':
                if hwvalue == 'd710' or hwvalue == 'm510':
                    prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=flink_taskmanager_System_Network_eno1_SendRate[5m] @ " +timestamp_prom
                if hwvalue == 'xl170':
                    prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=flink_taskmanager_System_Network_eno49np0_SendRate[5m] @ " +timestamp_prom
                if hwvalue == 'c6525-25g' or hwvalue == 'c6525-100g':
                    prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=flink_taskmanager_System_Network_eno33np0_SendRate[5m] @ " +timestamp_prom
                
                print(prom_endpoint)
                nw_response = requests.get(prom_endpoint)
                data = nw_response.json()
                print(data)
                return JsonResponse(json.dumps(data),status=response_status, safe=False)
            elif queryMetr == 'Memory Utilization':
                prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=flink_taskmanager_Status_JVM_Memory_Heap_Used[5m] @ " +timestamp_prom
                print(prom_endpoint)
                mem_response = requests.get(prom_endpoint)
                data = mem_response.json()
                print(data)
                return JsonResponse(json.dumps(data),status=response_status, safe=False)
            elif queryMetr == 'Latency':
                prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=sum(avg_over_time(flink_taskmanager_job_latency_source_id_operator_id_operator_subtask_index_latency{job_id=\"" + jobId + "\",operator_subtask_index='0',quantile='0.98'}[5m] @ " +timestamp_prom+"))"
                print(prom_endpoint)
                latency_response = requests.get(prom_endpoint)
                print(latency_response)
                datas = latency_response.json()
                print(datas)
                return JsonResponse(data=datas,status=response_status, safe=False)
        elif analysisOf == 'Operator':

            operator_id = selections['selected_operator']
            operatorMetr = selections['selected_operator_metrics']
            print(operator_id)
            print(operatorMetr)
            if operatorMetr == 'Selectivity':
                prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=avg_over_time(flink_taskmanager_job_task_operator_numRecordsOutPerSecond{job_id=\"" + jobId + "\",operator_id=\""+operator_id+"\"}[5m] @ " +timestamp_prom+")%20%2F%20avg_over_time(flink_taskmanager_job_task_operator_numRecordsInPerSecond{job_id=\"" + jobId + "\",operator_id=\""+operator_id+"\"}[5m] @ " +timestamp_prom+")"
                print(prom_endpoint)
                selectivity_response = requests.get(prom_endpoint)
                data2 = selectivity_response.json()
                pd = len(data2["data"]["result"])
                operatorName = ''
                for result in data2["data"]["result"]:
                    operatorName = result["metric"]["operator_name"]
                print("printing selectivityx+++++++++++++++++++++++++++++++++++")
                prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=sum(avg_over_time(flink_taskmanager_job_task_operator_numRecordsOutPerSecond{job_id=\"" + jobId + "\",operator_id=\""+operator_id+"\"}[5m] @ " +timestamp_prom+"))%20%2F%20sum(avg_over_time(flink_taskmanager_job_task_operator_numRecordsInPerSecond{job_id=\"" + jobId + "\",operator_id=\""+operator_id+"\"}[5m] @ " +timestamp_prom+"))"
                print(prom_endpoint)
                selectivity_response = requests.get(prom_endpoint)
                data1 = selectivity_response.json()
                selectivity_avg = data1["data"]["result"][0]["value"][1]

                response_data = { givenName +"-"+operatorName+ "-p-"+str(pd) : selectivity_avg }
                print(response_data)
                return JsonResponse(data=response_data,status=response_status, safe=False)
            elif operatorMetr == 'Processing Latency 98th percentile':
                prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=avg_over_time(flink_taskmanager_job_latency_source_id_operator_id_operator_subtask_index_latency{job_id=\"" + jobId + "\", operator_id=\""+operator_id+"\",quantile='0.98'}[5m] @ " +timestamp_prom+")"
                print(prom_endpoint)
                latency_response = requests.get(prom_endpoint)
                data = latency_response.json()
                print(data)
                
                sum = 0
                avg = 0
                for each_data in data["data"]["result"]:
                    print(each_data)
                    sum += float(each_data["value"][1])
                avg = sum/len(data)
                print(avg)
                    

                return JsonResponse(data=avg,status=response_status, safe=False)
            elif operatorMetr == 'Processing Latency 95th percentile':
                prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=avg_over_time(flink_taskmanager_job_latency_source_id_operator_id_operator_subtask_index_latency{job_id=\"" + jobId + "\", operator_id=\""+operator_id+"\",quantile='0.95'}[5m] @ " +timestamp_prom+")"
                print(prom_endpoint)
                latency_response = requests.get(prom_endpoint)
                data = latency_response.json()
                print(data)
                
                sum = 0
                avg = 0
                for each_data in data["data"]["result"]:
                    print(each_data)
                    sum += float(each_data["value"][1])
                avg = sum/len(data)
                print(avg)
                    

                return JsonResponse(data=avg,status=response_status, safe=False)
            
            elif operatorMetr == "Processing Latency median":
                prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=avg_over_time(flink_taskmanager_job_latency_source_id_operator_id_operator_subtask_index_latency{job_id=\"" + jobId + "\", operator_id=\""+operator_id+"\",quantile='0.5'}[5m] @ " +timestamp_prom+")"
                print(prom_endpoint)
                latency_response = requests.get(prom_endpoint)
                data = latency_response.json()
                print(data)
                
                sum = 0
                avg = 0
                for each_data in data["data"]["result"]:
                    print(each_data)
                    sum += float(each_data["value"][1])
                avg = sum/len(data)
                print(avg)
                    

                return JsonResponse(data=avg,status=response_status, safe=False)

class GetCompareGraphData(View):
    @staticmethod
    def post(request):
        comparisonFormElements = json.loads(request.body)
        #print(comparisonFormElements)
        print("comparison form elements is ")
        print(comparisonFormElements)
        returnData = []
        county = 1
        for comparisonFormElement in comparisonFormElements:
            print('calling prometheus for', county )
            data = getPrometheusData(comparisonFormElement)
            print("the ${county} data is ${data}")
            returnData.append(data)
            county += 1
        print("Return data is ")
        print(returnData)
        return JsonResponse(data=returnData,status=200, safe=False)

def getPrometheusData(selections):
    hwtype_filepath = os.path.abspath(os.path.join(settings.BASE_DIR, '../dsp_be/hwtype.txt'))
    print(hwtype_filepath)
    with open(hwtype_filepath, 'r') as file:
        content = file.read()
    # Extracting the value after '='
    if '=' in content:
        key, hwvalue = content.split('=')
        key = key.strip()
        hwvalue = hwvalue.strip()
        print(f"The value of '{key}' is '{hwvalue}'")
    else:
        print("Invalid format in the file.")
    print('######################################################')

    main_node = selections['cluster_main_node_ip']
    jobId = selections['selected_jobId']
    analysisOf = selections['selected_analysis_type']
    returnData = {}
    print("http://"+main_node+":8086/v1/jobs/"+jobId)
    requested_cluster_jobs = requests.get("http://"+main_node+":8086/v1/jobs/"+jobId)
    cluster_jobs_json = requested_cluster_jobs.json()
    verticescount = len(cluster_jobs_json['vertices'])
    parallelism_list = []
    for i in range(verticescount):
        if i == 0 or i == 1 or i == (verticescount) or i == (verticescount-1) or i == (verticescount-2):
            continue
        parallelism_list.append(cluster_jobs_json['vertices'][i]['parallelism'])

    print(parallelism_list)
    para_string = str(int(''.join(map(str, parallelism_list))))
    print(para_string)
    print("vertices count", verticescount)

    fullJobName = cluster_jobs_json["name"]
    cutjobId = jobId[0:4]
    cutJobName = fullJobName[0:3]
    givenName = cutJobName + '-' + cutjobId
    givenNameQuery = givenName + "-" + para_string
    timestamp_prom = (cluster_jobs_json["start-time"]) // 1000
    timestamp_prom = timestamp_prom + 300
    timestamp_prom = str(timestamp_prom)

    if analysisOf == 'Entire Query':
        queryMetr = selections['selected_query_metrics']
        if queryMetr == 'Throughput':

            prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=quantile_over_time(0.95, (flink_taskmanager_job_task_operator_numRecordsInPerSecond{job_id=\"" + jobId + "\" ,operator_name='kafka_sink:_Writer'}[5m] @ " +timestamp_prom+"))"
            throughput_response = requests.get(prom_endpoint)
            resp = throughput_response.json()
            print("resp data is")
            returnData = {givenNameQuery : resp['data']['result'][0]['value'][1]}
            print("return data")
            print(returnData)
        elif queryMetr == 'CPU Utilization':
            prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=quantile(0.50, quantile_over_time(0.95,%20(flink_taskmanager_System_CPU_Load15min[5m] @ " +timestamp_prom+")))"
            cpu_response = requests.get(prom_endpoint)
            resp = cpu_response.json()
            print("resp data is")
            returnData = {givenNameQuery : resp['data']['result'][0]['value'][1]}
            print("return data")
            print(returnData)
       
        elif queryMetr == 'N/W Utilization':
            if hwvalue == 'd710' or hwvalue == 'm510':
                prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=quantile(0.50, quantile_over_time(0.95,%20(flink_taskmanager_System_Network_eno1_SendRate[5m] @ " +timestamp_prom+")))"
                
            if hwvalue == 'xl170':
                prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=quantile(0.50, quantile_over_time(0.95,%20(flink_taskmanager_System_Network_eno49np0_SendRate[5m] @ " +timestamp_prom+")))"
                
            if hwvalue == 'c6525-25g' or hwvalue == 'c6525-100g':
                prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=quantile(0.50, quantile_over_time(0.95,%20(flink_taskmanager_System_Network_eno33np0_SendRate[5m] @ " +timestamp_prom+")))"
                
            nw_response = requests.get(prom_endpoint)
            resp = nw_response.json()
            print("resp data is")
            returnData = {givenNameQuery : resp['data']['result'][0]['value'][1]}
            print("return data")
            print(returnData)
        elif queryMetr == 'Memory Utilization':
            prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=log10(quantile(0.50, (quantile_over_time(0.95,%20(flink_taskmanager_Status_JVM_Memory_Heap_Used[5m] @ " +timestamp_prom+")))))"
            mem_response = requests.get(prom_endpoint)
            resp = mem_response.json()
            print("resp data is")
            returnData = {givenNameQuery : resp['data']['result'][0]['value'][1]}
            print("return data")
            print(returnData)
        elif queryMetr == 'Latency':
            prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=sum(avg_over_time(flink_taskmanager_job_latency_source_id_operator_id_operator_subtask_index_latency{job_id=\"" + jobId + "\",quantile='0.98'}[5m] @ " +timestamp_prom+"))"
            print(prom_endpoint)
            lat_response = requests.get(prom_endpoint)
            data = lat_response.json()
            print(data)
            extracted_data = data["data"]["result"][0]["value"][1]
            response_data = { givenNameQuery : extracted_data }
            print(response_data)
            returnData = response_data

            
    elif analysisOf == 'Operator':
        operator_id = selections['selected_operator']
        operatorMetr = selections['selected_operator_metrics']

        verticeResponse = requests.get("http://"+ main_node + ":8086/v1/jobs/"+jobId)
        jsonVertice = verticeResponse.json()

        for result in jsonVertice["vertices"]:
                 if result["id"] == operator_id:
                     operName = result["name"]
                
        
        if operatorMetr == 'Selectivity':

            prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=avg_over_time(flink_taskmanager_job_task_operator_numRecordsOutPerSecond{job_id=\"" + jobId + "\",operator_id=\""+operator_id+"\"}[5m] @ " +timestamp_prom+")%20%2F%20avg_over_time(flink_taskmanager_job_task_operator_numRecordsInPerSecond{job_id=\"" + jobId + "\",operator_id=\""+operator_id+"\"}[5m] @ " +timestamp_prom+")"
            print(prom_endpoint)
            selectivity_response = requests.get(prom_endpoint)
            data2 = selectivity_response.json()
            pd = len(data2["data"]["result"])
            operatorName = ''
            for result in data2["data"]["result"]:
                operatorName = result["metric"]["operator_name"]
            prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=sum(avg_over_time(flink_taskmanager_job_task_operator_numRecordsOutPerSecond{job_id=\"" + jobId + "\",operator_id=\""+operator_id+"\"}[5m] @ " +timestamp_prom+"))%20%2F%20sum(avg_over_time(flink_taskmanager_job_task_operator_numRecordsInPerSecond{job_id=\"" + jobId + "\",operator_id=\""+operator_id+"\"}[5m] @ " +timestamp_prom+"))"
            print(prom_endpoint)
            selectivity_response = requests.get(prom_endpoint)
            data1 = selectivity_response.json()
            selectivity_avg = data1["data"]["result"][0]["value"][1]
            response_data = { givenName +"-"+operatorName+ "-p-"+str(pd) : selectivity_avg }
            print(response_data)

            returnData = response_data
        elif operatorMetr == 'Processing Latency 98th percentile':
            prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=avg_over_time(flink_taskmanager_job_latency_source_id_operator_id_operator_subtask_index_latency{job_id=\"" + jobId + "\", operator_id=\""+operator_id+"\",quantile='0.98'}[5m] @ " +timestamp_prom+")"
            print(prom_endpoint)
            latency_response = requests.get(prom_endpoint)
            data = latency_response.json()
            pd = len(data["data"]["result"])
            
            print(data)
            sum = 0
            avg = 0
            for each_data in data["data"]["result"]:
                sum += float(each_data["value"][1])
            avg = sum/pd
            response_data = { givenName +"-"+operName+ "-p-"+str(pd)  : avg }
            print(avg)
            returnData = response_data


        elif operatorMetr == 'Processing Latency 95th percentile':
            prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=avg_over_time(flink_taskmanager_job_latency_source_id_operator_id_operator_subtask_index_latency{job_id=\"" + jobId + "\", operator_id=\""+operator_id+"\",quantile='0.95'}[5m] @ " +timestamp_prom+")"
            latency_response = requests.get(prom_endpoint)
            data = latency_response.json() 
            pd = len(data["data"]["result"])  
            print(data)            
            sum = 0
            avg = 0
            for each_data in data["data"]["result"]:
                sum += float(each_data["value"][1])
            avg = sum/pd
            response_data = { givenName +"-"+operName+ "-p-"+str(pd) : avg }
            returnData = response_data

        elif operatorMetr == 'Processing Latency median':
            prom_endpoint = "http://" + main_node + ":9090/api/v1/query?query=avg_over_time(flink_taskmanager_job_latency_source_id_operator_id_operator_subtask_index_latency{job_id=\"" + jobId + "\", operator_id=\""+operator_id+"\",quantile='0.50'}[5m] @ " +timestamp_prom+")"
            latency_response = requests.get(prom_endpoint)
            data = latency_response.json() 
            pd = len(data["data"]["result"])  
            print(data)            
            sum = 0
            avg = 0
            for each_data in data["data"]["result"]:
                sum += float(each_data["value"][1])
            avg = sum/pd
            response_data = { givenName +"-"+operName+ "-p-"+str(pd) : avg }
            returnData = response_data
    return returnData