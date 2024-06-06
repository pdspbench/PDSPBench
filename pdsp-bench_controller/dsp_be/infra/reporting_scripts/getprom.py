import json
import os
import logging
import socket
import sys
import time
import pandas as pd
import click
import json
from datetime import datetime

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

# 'job_run_time': 6000, 
# 'job_program': 'Ads Analytics', 
# 'job_parallelization': '2,2,2,2,2', 
# 'job_query_number': 1, 
# 'job_window_size': 100, 
# 'job_window_slide_size': 10, 
# 'producer_event_per_second': '100', 
# 'node0.sat.maki-test.emulab.net',

def getOperatorMetrics(parallelization,main_node_ip,job_id,operatorId, operatorName,timestamp_prom):
#'Selectivity'
    dict_response = {}
    prom_endpoint_Selectivity = "http://" + main_node_ip + ":9090/api/v1/query?query=avg_over_time(flink_taskmanager_job_task_operator_numRecordsOutPerSecond{job_id=\"" + job_id + "\",operator_id=\""+operatorId+"\"}[5m] @ " +timestamp_prom+")%20%2F%20avg_over_time(flink_taskmanager_job_task_operator_numRecordsInPerSecond{job_id=\"" + job_id + "\",operator_id=\""+operatorId+"\"}[5m] @ " +timestamp_prom+")"
    
    print("Selectivity:pd")
    print(prom_endpoint_Selectivity)
    response = requests.get(prom_endpoint_Selectivity)
    data = response.json()
    pd = len(data["data"]["result"])
    #print("pd: ",pd)
    #print("parallelization passed: ",parallelization)
    #selectivity_sum = 0
    #operatorName_found = ''
    #for result in data["data"]["result"]:
    #    selectivity_sum =+ float(result["value"][1])
    #    operatorName_found = result["metric"]["operator_name"]
    #selectivity_avg = selectivity_sum/pd
    #print('operatorName_passed: ',operatorName)
    #print('operatorName_found: ',operatorName_found)
    prom_endpoint_Selectivity = "http://" + main_node_ip + ":9090/api/v1/query?query=max(avg_over_time(flink_taskmanager_job_task_operator_numRecordsOutPerSecond{job_id=\"" + job_id + "\",operator_id=\""+operatorId+"\"}[5m] @ " +timestamp_prom+"))%20%2F%20max(avg_over_time(flink_taskmanager_job_task_operator_numRecordsInPerSecond{job_id=\"" + job_id + "\",operator_id=\""+operatorId+"\"}[5m] @ " +timestamp_prom+"))"
    print("Selectivity")
    print(prom_endpoint_Selectivity)
    response = requests.get(prom_endpoint_Selectivity)
    data = response.json()
    print(data)
    
    
    selectivity_avg = data["data"]["result"][0]["value"][1]


    response_data = { "job_id:"+str(job_id)+"--OperatorName:"+operatorName+"--OperatorId:"+str(operatorId)+"--parallelization : "+str(pd)+"metric : Selectivity" : selectivity_avg }
    #print(response_data)
    dict_response["selectivity"]=response_data
    #dict_response.update(response_data)
#'Processing Latency 98th percentile'
    prom_endpoint_Latency_98th = "http://" + main_node_ip + ":9090/api/v1/query?query=avg(avg_over_time(flink_taskmanager_job_latency_source_id_operator_id_operator_subtask_index_latency{job_id=\"" + job_id + "\", operator_id=\""+operatorId+"\",quantile='0.98'}[5m] @ " +timestamp_prom+"))"
    #print(prom_endpoint_Latency_98th)
    response = requests.get(prom_endpoint_Latency_98th)
    data = response.json()
    data = data['data']['result'][0]['value'][1]
    #print(data)
    
    response_data = { "job_id:"+str(job_id)+"--OperatorName:"+operatorName+"--OperatorId:"+str(operatorId)+"--parallelization:"+str(parallelization)+"metric : Latency_98th" : data }
    #print(response_data)
    dict_response["processing_latency_98th"]=response_data
    #dict_response.update(response_data)                

    
#'Processing Latency 95th percentile'
    prom_endpoint_Latency_95th = "http://" + main_node_ip + ":9090/api/v1/query?query=avg(avg_over_time(flink_taskmanager_job_latency_source_id_operator_id_operator_subtask_index_latency{job_id=\"" + job_id + "\", operator_id=\""+operatorId+"\",quantile='0.95'}[5m] @ " +timestamp_prom+"))"
    response = requests.get(prom_endpoint_Latency_95th)
    data = response.json()
    data = data['data']['result'][0]['value'][1]
    #print(data)
    
    response_data = { "job_id:"+str(job_id)+"--OperatorName:"+operatorName+"--OperatorId:"+str(operatorId)+"--parallelization:"+str(parallelization)+"metric : Latency_95th" : data }
    #print(response_data)
    dict_response["processing_latency_95th"]=response_data
    
    prom_endpoint_Latency_50th = "http://" + main_node_ip + ":9090/api/v1/query?query=avg(avg_over_time(flink_taskmanager_job_latency_source_id_operator_id_operator_subtask_index_latency{job_id=\"" + job_id + "\", operator_id=\""+operatorId+"\",quantile='0.5'}[5m] @ " +timestamp_prom+"))"
    response = requests.get(prom_endpoint_Latency_50th)
    data = response.json()
    data = data['data']['result'][0]['value'][1]
    #print(data)
    
    response_data = { "job_id:"+str(job_id)+"--OperatorName:"+operatorName+"--OperatorId:"+str(operatorId)+"--parallelization:"+str(parallelization)+"metric : Latency_50th" : data }
    #print(response_data)
    dict_response["processing_latency_50th"]=response_data
    #dict_response.update(response_data)  

    return dict_response

def getQueryMetrics(main_node_ip, job_id, timestamp_prom):
    dictReturn = {}
    prom_endpoint_recPerSecOutSource = "http://" + main_node_ip + ":9090/api/v1/query?query=sum(max_over_time(flink_taskmanager_job_task_operator_numRecordsOutPerSecond{job_id=\"" + job_id + "\" ,operator_name='Source:_kafka_source'}[5m] @ " +timestamp_prom+"))"
    #print(prom_endpoint_Throughput)
    recPerSecOutSource_resp = requests.get(prom_endpoint_recPerSecOutSource)
    data =recPerSecOutSource_resp.json()
    data = data['data']['result'][0]['value'][1]
    dictReturn["recPerSecOutSource_max"]= data

    prom_endpoint_recPerSecOutSource_50 = "http://" + main_node_ip + ":9090/api/v1/query?query=sum(quantile_over_time(0.5, flink_taskmanager_job_task_operator_numRecordsOutPerSecond{job_id=\"" + job_id + "\" ,operator_name='Source:_kafka_source'}[5m] @ " +timestamp_prom+"))"
    #print(prom_endpoint_Throughput)
    recPerSecOutSource_resp = requests.get(prom_endpoint_recPerSecOutSource_50)
    data =recPerSecOutSource_resp.json()
    data = data['data']['result'][0]['value'][1]
    dictReturn["recPerSecOutSource_50"]= data

    prom_endpoint_recPerSecOutSource_98 = "http://" + main_node_ip + ":9090/api/v1/query?query=sum(quantile_over_time(0.98, flink_taskmanager_job_task_operator_numRecordsOutPerSecond{job_id=\"" + job_id + "\" ,operator_name='Source:_kafka_source'}[5m] @ " +timestamp_prom+"))"
    print(prom_endpoint_recPerSecOutSource_98)
    recPerSecOutSource_resp = requests.get(prom_endpoint_recPerSecOutSource_98)
    data =recPerSecOutSource_resp.json()
    data = data['data']['result'][0]['value'][1]
    dictReturn["recPerSecOutSource_98"]= data

    prom_endpoint_recPerSecOutSource_95 = "http://" + main_node_ip + ":9090/api/v1/query?query=sum(quantile_over_time(0.95, flink_taskmanager_job_task_operator_numRecordsOutPerSecond{job_id=\"" + job_id + "\" ,operator_name='Source:_kafka_source'}[5m] @ " +timestamp_prom+"))"
    #print(prom_endpoint_Throughput)
    recPerSecOutSource_resp = requests.get(prom_endpoint_recPerSecOutSource_95)
    data =recPerSecOutSource_resp.json()
    data = data['data']['result'][0]['value'][1]
    print(data)
    dictReturn["recPerSecOutSource_95"]= data

    prom_endpoint_Throughput = "http://" + main_node_ip + ":9090/api/v1/query?query=flink_taskmanager_job_task_operator_numRecordsInPerSecond{job_id=\"" + job_id + "\" ,operator_name='kafka_sink:_Writer'}[5m] @ " +timestamp_prom
    #print(prom_endpoint_Throughput)
    throughput_response = requests.get(prom_endpoint_Throughput)
    data =throughput_response.json()
    data = data['data']['result']
    dictReturn["throughput"]= data
    #print('throughput done')house-event-parser
    
    prom_endpoint_Throughput = "http://" + main_node_ip + ":9090/api/v1/query?query=quantile_over_time(0.50, (flink_taskmanager_job_task_operator_numRecordsInPerSecond{job_id=\"" + job_id + "\" ,operator_name='kafka_sink:_Writer'}[5m] @ " +timestamp_prom+"))"
    print(prom_endpoint_Throughput)
    throughput_response = requests.get(prom_endpoint_Throughput)
    data =throughput_response.json()
    data = data['data']['result'][0]['value'][1]
    dictReturn["throughput_50"]= data
    #print('throughput 50 done')

    prom_endpoint_Throughput = "http://" + main_node_ip + ":9090/api/v1/query?query=quantile_over_time(0.95, (flink_taskmanager_job_task_operator_numRecordsInPerSecond{job_id=\"" + job_id + "\" ,operator_name='kafka_sink:_Writer'}[5m] @ " +timestamp_prom+"))"
    #print(prom_endpoint_Throughput)
    throughput_response = requests.get(prom_endpoint_Throughput)
    data =throughput_response.json()
    data = data['data']['result'][0]['value'][1]
    dictReturn["throughput_95"]= data
    #print('throughput 95 done')

    prom_endpoint_Throughput = "http://" + main_node_ip + ":9090/api/v1/query?query=quantile_over_time(0.98, (flink_taskmanager_job_task_operator_numRecordsInPerSecond{job_id=\"" + job_id + "\" ,operator_name='kafka_sink:_Writer'}[5m] @ " +timestamp_prom+"))"
    #print(prom_endpoint_Throughput)
    throughput_response = requests.get(prom_endpoint_Throughput)
    data =throughput_response.json()
    data = data['data']['result'][0]['value'][1]
    dictReturn["throughput_98"]= data
    #print('throughput 98 done')
    

    prom_endpoint_cpu = "http://" + main_node_ip + ":9090/api/v1/query?query=flink_taskmanager_System_CPU_Load15min[5m] @ " +timestamp_prom
    #print(prom_endpoint_cpu)
    cpu_response = requests.get(prom_endpoint_cpu)
    data = cpu_response.json()
    data = data['data']['result']
    dictReturn["cpu"]= data
    #print('cpu done')
    
    prom_endpoint_cpu = "http://" + main_node_ip + ":9090/api/v1/query?query=quantile(0.50, quantile_over_time(0.50,%20(flink_taskmanager_System_CPU_Load15min[5m] @ " +timestamp_prom+")))"
    #print(prom_endpoint_cpu)
    cpu_response = requests.get(prom_endpoint_cpu)
    data = cpu_response.json()
    data = data['data']['result'][0]['value'][1]
    dictReturn["cpu_50"]= data
    #print('cpu 50 done')

    prom_endpoint_cpu = "http://" + main_node_ip + ":9090/api/v1/query?query=quantile(0.50, quantile_over_time(0.95,%20(flink_taskmanager_System_CPU_Load15min[5m] @ " +timestamp_prom+")))"
    #print(prom_endpoint_cpu)
    cpu_response = requests.get(prom_endpoint_cpu)
    data = cpu_response.json()
    data = data['data']['result'][0]['value'][1]
    dictReturn["cpu_95"]= data
    #print('cpu 95 done')

    prom_endpoint_cpu = "http://" + main_node_ip + ":9090/api/v1/query?query=quantile(0.50, quantile_over_time(0.98,%20(flink_taskmanager_System_CPU_Load15min[5m] @ " +timestamp_prom+")))"
    #print(prom_endpoint_cpu)
    cpu_response = requests.get(prom_endpoint_cpu)
    data = cpu_response.json()
    data = data['data']['result'][0]['value'][1]
    dictReturn["cpu_98"]= data
    #print('cpu 98 done')
    
    #prom_endpoint_NW = "http://" + main_node_ip + ":9090/api/v1/query?query=flink_taskmanager_System_Network_eno33np0_SendRate[5m] @ " +timestamp_prom
    prom_endpoint_NW = "http://" + main_node_ip + ":9090/api/v1/query?query=flink_taskmanager_System_Network_eno33np0_SendRate[5m] @ " +timestamp_prom
    #print(prom_endpoint_NW)
    nw_response = requests.get(prom_endpoint_NW)
    data = nw_response.json()
    data = data['data']['result']
    dictReturn["NW"]= data
    #print('NW done')

    prom_endpoint_NW = "http://" + main_node_ip + ":9090/api/v1/query?query=quantile(0.95, quantile_over_time(0.50, (flink_taskmanager_System_Network_eno33np0_SendRate[5m] @ " +timestamp_prom+")))"
    #print(prom_endpoint_NW)
    nw_response = requests.get(prom_endpoint_NW)
    data = nw_response.json()
    #print(data)
    data = data['data']['result'][0]['value'][1]
    dictReturn["NW_50"]= data
    #print('NW 50 done')

    prom_endpoint_NW = "http://" + main_node_ip + ":9090/api/v1/query?query=quantile(0.95, quantile_over_time(0.95, (flink_taskmanager_System_Network_eno33np0_SendRate[5m] @ " +timestamp_prom+")))"
    #print(prom_endpoint_NW)
    nw_response = requests.get(prom_endpoint_NW)
    data = nw_response.json()
    #print(data)
    data = data['data']['result'][0]['value'][1]
    dictReturn["NW_95"]= data
    #print('NW 95 done')

    prom_endpoint_NW = "http://" + main_node_ip + ":9090/api/v1/query?query=quantile(0.95, quantile_over_time(0.98, (flink_taskmanager_System_Network_eno33np0_SendRate[5m] @ " +timestamp_prom+")))"
    #print(prom_endpoint_NW)
    nw_response = requests.get(prom_endpoint_NW)
    data = nw_response.json()
    #print(data)
    data = data['data']['result'][0]['value'][1]
    dictReturn["NW_98"]= data
    #print('NW 98 done')
      
    prom_endpoint_Memory = "http://" + main_node_ip + ":9090/api/v1/query?query=flink_taskmanager_Status_JVM_Memory_Heap_Used[5m] @ " +timestamp_prom
    mem_response = requests.get(prom_endpoint_Memory)
    data = mem_response.json()
    data = data['data']['result']
    dictReturn["Memory"]= data

    prom_endpoint_Memory = "http://" + main_node_ip + ":9090/api/v1/query?query=log10(quantile(0.50, (quantile_over_time(0.50,%20(flink_taskmanager_Status_JVM_Memory_Heap_Used[5m] @ " +timestamp_prom+")))))"
    mem_response = requests.get(prom_endpoint_Memory)
    data = mem_response.json()
    data = data['data']['result'][0]['value'][1]
    dictReturn["Memory_50"]= data

    prom_endpoint_Memory = "http://" + main_node_ip + ":9090/api/v1/query?query=log10(quantile(0.50, (quantile_over_time(0.95,%20(flink_taskmanager_Status_JVM_Memory_Heap_Used[5m] @ " +timestamp_prom+")))))"
    mem_response = requests.get(prom_endpoint_Memory)
    data = mem_response.json()
    data = data['data']['result'][0]['value'][1]
    dictReturn["Memory_95"]= data

    prom_endpoint_Memory = "http://" + main_node_ip + ":9090/api/v1/query?query=log10(quantile(0.50, (quantile_over_time(0.98,%20(flink_taskmanager_Status_JVM_Memory_Heap_Used[5m] @ " +timestamp_prom+")))))"
    mem_response = requests.get(prom_endpoint_Memory)
    data = mem_response.json()
    data = data['data']['result'][0]['value'][1]
    dictReturn["Memory_98"]= data

    
    prom_endpoint_Latency = "http://" + main_node_ip + ":9090/api/v1/query?query=sum(avg_over_time(flink_taskmanager_job_latency_source_id_operator_id_operator_subtask_index_latency{job_id=\"" + job_id + "\",operator_subtask_index='0',quantile='0.98'}[5m] @ " +timestamp_prom+"))"
    #print('prom_endpoint_Latency_98')
    #print(prom_endpoint_Latency)
    latency_response = requests.get(prom_endpoint_Latency)
    data = latency_response.json()
    data = data['data']['result'][0]['value'][1]
    dictReturn["endtoend_latency_98"]= data

    prom_endpoint_Latency = "http://" + main_node_ip + ":9090/api/v1/query?query=sum(avg_over_time(flink_taskmanager_job_latency_source_id_operator_id_operator_subtask_index_latency{job_id=\"" + job_id + "\",operator_subtask_index='0',quantile='0.95'}[5m] @ " +timestamp_prom+"))"
    latency_response = requests.get(prom_endpoint_Latency)
    data = latency_response.json()
    data = data['data']['result'][0]['value'][1]
    dictReturn["endtoend_latency_95"]= data
    
    prom_endpoint_Latency = "http://" + main_node_ip + ":9090/api/v1/query?query=sum(avg_over_time(flink_taskmanager_job_latency_source_id_operator_id_operator_subtask_index_latency{job_id=\"" + job_id + "\",operator_subtask_index='0',quantile='0.5'}[5m] @ " +timestamp_prom+"))"
    latency_response = requests.get(prom_endpoint_Latency)
    data = latency_response.json()
    data = data['data']['result'][0]['value'][1]
    dictReturn["endtoend_latency_50"]= data
    
    return dictReturn

def getLinearRoad(job_id, main_node_ip, timestamp_prom):
    #"Vehicle-event-parser", "toll-notification", "formatter-toll-notification", "accident-notification", "formatter-accident-notification" ,"daily-expenditure", "vehicle-report-mapper"
    #"VehicleEventParser", "TollNotification", "FormatterTollNotification", "AccidentNotification", "FormatterAccidentNotification", ,"DailyExpenditure", "VehicleReportMapper"
    verticeResponse = requests.get("http://"+ main_node_ip + ":8086/v1/jobs/"+job_id)
    jsonVertice = verticeResponse.json()
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
    #dict_metrtics['tokenizer'] = []
    #dict_metrtics['counter'] = []
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "Vehicle-event-parser" in vertice["name"]:
                #print(vertice)
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
    dictCombo["operatorMetrics"] = {}

    dictVehicleEventParser = getOperatorMetrics(numOfVehicleEventParser, main_node_ip, job_id, verticeIdVehicleEventParser, VehicleEventParser_name,timestamp_prom)
    dictCombo["operatorMetrics"]["VehicleEventParser"] = dictVehicleEventParser
    if verticeIdTollNotification is not None:
        dictTollNotification = getOperatorMetrics(numOfTollNotification, main_node_ip, job_id, verticeIdTollNotification, TollNotification_name,timestamp_prom)
        dictCombo["operatorMetrics"]["TollNotification"] = dictTollNotification

    if verticeIdFormatterTollNotification is not None:
        dictFormatterTollNotification = getOperatorMetrics(numOfFormatterTollNotification, main_node_ip, job_id, verticeIdFormatterTollNotification, FormatterTollNotification_name,timestamp_prom)
        dictCombo["operatorMetrics"]["FormatterTollNotification"] = dictFormatterTollNotification

    if verticeIdAccidentNotification is not None:
        dictAccidentNotification = getOperatorMetrics(numOfAccidentNotification, main_node_ip, job_id, verticeIdAccidentNotification, AccidentNotification_name,timestamp_prom)
        dictCombo["operatorMetrics"]["AccidentNotification"] = dictAccidentNotification

    if verticeIdFormatterAccidentNotification is not None:
        dictFormatterAccidentNotification = getOperatorMetrics(numOfFormatterAccidentNotification, main_node_ip, job_id, verticeIdFormatterAccidentNotification, FormatterAccidentNotification_name,timestamp_prom)
        dictCombo["operatorMetrics"]["FormatterAccidentNotification"] = dictFormatterAccidentNotification
    if verticeIdDailyExpenditure is not None:
        dictDailyExpenditure = getOperatorMetrics(numOfDailyExpenditure, main_node_ip, job_id, verticeIdDailyExpenditure, DailyExpenditure_name,timestamp_prom)
        dictCombo["operatorMetrics"]["DailyExpenditure"] = dictDailyExpenditure
    if verticeIdVehicleReportMapper is not None:
        dictVehicleReportMapper = getOperatorMetrics(numOfVehicleReportMapper, main_node_ip, job_id, verticeIdVehicleReportMapper, VehicleReportMapper_name,timestamp_prom)
        dictCombo["operatorMetrics"]["VehicleReportMapper"] = dictVehicleReportMapper

    querymetric = getQueryMetrics(main_node_ip, job_id, timestamp_prom)
    dictCombo["queryMetrics"] = querymetric      
    
    return dictCombo

def getTrafficMonitoring(job_id, main_node_ip, timestamp_prom):
    #"traffic-event-parser", "road-matcher", "avg-speed","formatter"
    ##"TrafficEventParser", "RoadMatcher", "AvgSpeed","Formatter"
    verticeResponse = requests.get("http://"+ main_node_ip + ":8086/v1/jobs/"+job_id)
    jsonVertice = verticeResponse.json()
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
    #dict_metrtics['tokenizer'] = []
    #dict_metrtics['counter'] = []
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "traffic-event-parser" in vertice["name"]:
                    #print(vertice)
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

    dictTrafficEventParser = getOperatorMetrics(numOfTrafficEventParser,main_node_ip,job_id,verticeIdTrafficEventParser,TrafficEventParser_name,timestamp_prom)
    

    dictRoadMatcher = getOperatorMetrics(numOfRoadMatcher,main_node_ip,job_id,verticeIdRoadMatcher,RoadMatcher_name,timestamp_prom)
    

    dictAvgSpeed = getOperatorMetrics(numOfAvgSpeed,main_node_ip,job_id,verticeIdAvgSpeed,AvgSpeed_name,timestamp_prom)
    

    dictFormatter = getOperatorMetrics(numOfFormatter,main_node_ip,job_id,verticeIdFormatter,Formatter_name,timestamp_prom)
    

    dictCombo["operatorMetrics"] = {}
    dictCombo["operatorMetrics"]["TrafficEventParser"] = dictTrafficEventParser
    dictCombo["operatorMetrics"]["RoadMatcher"] = dictRoadMatcher
    dictCombo["operatorMetrics"]["AvgSpeed"] = dictAvgSpeed
    dictCombo["operatorMetrics"]["Formatter"] = dictFormatter
    
    

    querymetric = getQueryMetrics(main_node_ip, job_id, timestamp_prom)
    dictCombo["queryMetrics"] = querymetric    
    
    return dictCombo

def getTpch(job_id, main_node_ip, timestamp_prom):
   
    #"tpch-event-parser", "tpch-data-filter", "tpch-flat-mapper", "priority-counter", "formatter"
     #"TpchEventParser", "TpchDataFilter", "TpchFlatMapper", "PriorityCounter", "Formatter"
    verticeResponse = requests.get("http://"+ main_node_ip + ":8086/v1/jobs/"+job_id)
    jsonVertice = verticeResponse.json()
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
    #dict_metrtics['tokenizer'] = []
    #dict_metrtics['counter'] = []
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "tpch-event-parser" in vertice["name"]:
                    #print(vertice)
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

    dictTpchEventParser = getOperatorMetrics(numOfTpchEventParser,main_node_ip,job_id,verticeIdTpchEventParser,TpchEventParser_name,timestamp_prom)
    

    dictTpchDataFilter = getOperatorMetrics(numOfTpchDataFilter,main_node_ip,job_id,verticeIdTpchDataFilter,TpchDataFilter_name,timestamp_prom)
    

    dictTpchFlatMapper = getOperatorMetrics(numOfTpchFlatMapper,main_node_ip,job_id,verticeIdTpchFlatMapper,TpchFlatMapper_name,timestamp_prom)
    

    dictPriorityCounter = getOperatorMetrics(numOfPriorityCounter,main_node_ip,job_id,verticeIdPriorityCounter,PriorityCounter_name,timestamp_prom)
    

    dictFormatter = getOperatorMetrics(numOfFormatter,main_node_ip,job_id,verticeIdFormatter,Formatter_name,timestamp_prom)
    

    dictCombo["operatorMetrics"] = {}
    dictCombo["operatorMetrics"]["TpchEventParser"] = dictTpchEventParser
    dictCombo["operatorMetrics"]["TpchDataFilter"] = dictTpchDataFilter
    dictCombo["operatorMetrics"]["TpchFlatMapper"] = dictTpchFlatMapper
    dictCombo["operatorMetrics"]["PriorityCounter"] = dictPriorityCounter
    dictCombo["operatorMetrics"]["Formatter"] = dictFormatter
    

    querymetric = getQueryMetrics(main_node_ip, job_id, timestamp_prom)
    dictCombo["queryMetrics"] = querymetric
        
    return dictCombo

def getTrendingTopics(job_id, main_node_ip, timestamp_prom):
    #"parser", "average-calculator", "spike-detector"
    verticeResponse = requests.get("http://"+ main_node_ip + ":8086/v1/jobs/"+job_id)
    jsonVertice = verticeResponse.json()
    verticeIdTrendingTopicsParser = None
    verticeIdTrendingTopicsExtractor = None
    verticeIdTrendingTopicsPopularityDetector = None
    
    dictTrendingTopicsParser = {}
    dictTrendingTopicsExtractor = {}
    dictTrendingTopicsPopularityDetector = {}
    
    dictCombo = {}
    jobName = jsonVertice["name"]
    #dict_metrtics['tokenizer'] = []
    #dict_metrtics['counter'] = []
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "twitter-parser" in vertice["name"]:
                    #print(vertice)
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

    dictTrendingTopicsParser = getOperatorMetrics(numOfTrendingTopicsParser,main_node_ip,job_id,verticeIdTrendingTopicsParser,TrendingTopicsParser_name,timestamp_prom)
    

    dictTrendingTopicsExtractor = getOperatorMetrics(numOfTrendingTopicsExtractor,main_node_ip,job_id,verticeIdTrendingTopicsExtractor,TrendingTopicsExtractor_name,timestamp_prom)
    

    dictTrendingTopicsPopularityDetector = getOperatorMetrics(numOfTrendingTopicsPopularityDetector,main_node_ip,job_id,verticeIdTrendingTopicsPopularityDetector,TrendingTopicsPopularityDetector_name,timestamp_prom)
    

    dictCombo["operatorMetrics"] = {}
    dictCombo["operatorMetrics"]["twitter-parser"] = dictTrendingTopicsParser
    dictCombo["operatorMetrics"]["topic-extractor"] = dictTrendingTopicsExtractor
    dictCombo["operatorMetrics"]["popularity-detector"] = dictTrendingTopicsPopularityDetector
    

    querymetric = getQueryMetrics(main_node_ip, job_id, timestamp_prom)
    dictCombo["queryMetrics"] = querymetric         
    
    return dictCombo

def getLogsProcessing(job_id, main_node_ip, timestamp_prom):
    #"parser", "average-calculator", "spike-detector"
    verticeResponse = requests.get("http://"+ main_node_ip + ":8086/v1/jobs/"+job_id)
    jsonVertice = verticeResponse.json()
    verticeIdLogProcessorParser = None
    verticeIdLogProcessorVolumeCounter = None
    verticeIdLogProcessorStatusCounter = None
    
    dictLogProcessorParser = {}
    dictLogProcessorVolumeCounter = {}
    dictLogProcessorStatusCounter = {}
    
    dictCombo = {}
    jobName = jsonVertice["name"]
    #dict_metrtics['tokenizer'] = []
    #dict_metrtics['counter'] = []
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "Log-parser" in vertice["name"]:
                #print(vertice)
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
    dictCombo["operatorMetrics"] = {}

    dictLogProcessorParser = getOperatorMetrics(numOfLogProcessorParser, main_node_ip, job_id, verticeIdLogProcessorParser, LogProcessorParser_name,timestamp_prom)
    dictCombo["operatorMetrics"]["LogProcessorParser"] = dictLogProcessorParser
    if verticeIdLogProcessorVolumeCounter is not None:
        dictLogProcessorVolumeCounter = getOperatorMetrics(numOfLogProcessorVolumeCounter, main_node_ip, job_id, verticeIdLogProcessorVolumeCounter, LogProcessorVolumeCounter_name,timestamp_prom)
        dictCombo["operatorMetrics"]["LogProcessorVolumeCounter"] = dictLogProcessorVolumeCounter

    if verticeIdLogProcessorStatusCounter is not None:
        dictLogProcessorStatusCounter = getOperatorMetrics(numOfLogProcessorStatusCounter, main_node_ip, job_id, verticeIdLogProcessorStatusCounter, LogProcessorStatusCounter_name,timestamp_prom)
        dictCombo["operatorMetrics"]["LogProcessorStatusCounter"] = dictLogProcessorStatusCounter
    

    querymetric = getQueryMetrics(main_node_ip, job_id, timestamp_prom)
    dictCombo["queryMetrics"] = querymetric     
    
    return dictCombo

def getBargainIndex(job_id, main_node_ip, timestamp_prom):
    #"parser", "average-calculator", "spike-detector"
    verticeResponse = requests.get("http://"+ main_node_ip + ":8086/v1/jobs/"+job_id)
    jsonVertice = verticeResponse.json()
    verticeIdBargainIndexParser = None
    verticeIdBargainIndexVWAP = None
    verticeIdBargainIndexCalc = None
    
    dictBargainIndexParser = {}
    dictBargainIndexVWAP = {}
    dictBargainIndexCalc = {}
    
    dictCombo = {}
    jobName = jsonVertice["name"]
    #dict_metrtics['tokenizer'] = []
    #dict_metrtics['counter'] = []
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "quote-parser" in vertice["name"]:
                    #print(vertice)
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

    dictBargainIndexParser = getOperatorMetrics(numOfBargainIndexParser,main_node_ip,job_id,verticeIdBargainIndexParser,BargainIndexParser_name,timestamp_prom)
    

    dictBargainIndexVWAP = getOperatorMetrics(numOfBargainIndexVWAP,main_node_ip,job_id,verticeIdBargainIndexVWAP,BargainIndexVWAP_name,timestamp_prom)
    

    dictBargainIndexCalc = getOperatorMetrics(numOfBargainIndexCalc,main_node_ip,job_id,verticeIdBargainIndexCalc,BargainIndexCalc_name,timestamp_prom)
    

    dictCombo["operatorMetrics"] = {}
    dictCombo["operatorMetrics"]["BargainIndexParser"] = dictBargainIndexParser
    dictCombo["operatorMetrics"]["BargainIndexVWAP"] = dictBargainIndexVWAP
    dictCombo["operatorMetrics"]["BargainIndexCalc"] = dictBargainIndexCalc
    

    querymetric = getQueryMetrics(main_node_ip, job_id, timestamp_prom)
    dictCombo["queryMetrics"] = querymetric   
    
    return dictCombo

def getClickAnalytics(job_id, main_node_ip, timestamp_prom):
    #"parser", "average-calculator", "spike-detector"
    verticeResponse = requests.get("http://"+ main_node_ip + ":8086/v1/jobs/"+job_id)
    jsonVertice = verticeResponse.json()
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
    #dict_metrtics['tokenizer'] = []
    #dict_metrtics['counter'] = []
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "click-log-parser" in vertice["name"]:
                    #print(vertice)
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
    dictCombo["operatorMetrics"] = {}

    if verticeIdClickAnalyticsParser is not None:
        dictClickAnalyticsParser = getOperatorMetrics(numOfClickAnalyticsParser,main_node_ip,job_id,verticeIdClickAnalyticsParser,ClickAnalyticsParser_name,timestamp_prom)
        dictCombo["operatorMetrics"]["ClickAnalyticsParser"] = dictClickAnalyticsParser

    if verticeIdClickAnalyticsRepeat is not None:
        dictClickAnalyticsRepeat = getOperatorMetrics(numOfClickAnalyticsRepeat,main_node_ip,job_id,verticeIdClickAnalyticsRepeat,ClickAnalyticsRepeat_name,timestamp_prom)
        dictCombo["operatorMetrics"]["ClickAnalyticsRepeat"] = dictClickAnalyticsRepeat

    if verticeIdClickAnalyticsReduce is not None:
        dictClickAnalyticsReduce = getOperatorMetrics(numOfClickAnalyticsReduce,main_node_ip,job_id,verticeIdClickAnalyticsReduce,ClickAnalyticsReduce_name,timestamp_prom)
        dictCombo["operatorMetrics"]["ClickAnalyticsReduce"] = dictClickAnalyticsReduce

    if verticeIdClickAnalyticsGeo is not None:
        dictClickAnalyticsGeo = getOperatorMetrics(numOfClickAnalyticsGeo,main_node_ip,job_id,verticeIdClickAnalyticsGeo,ClickAnalyticsGeo_name,timestamp_prom)
        dictCombo["operatorMetrics"]["ClickAnalyticsGeo"] = dictClickAnalyticsGeo

    
    
    
    
    
    

    querymetric = getQueryMetrics(main_node_ip, job_id, timestamp_prom)
    dictCombo["queryMetrics"] = querymetric
        
    
    return dictCombo

def getMachineOutlier(job_id, main_node_ip, timestamp_prom):
    #"machine-usage-parser", "machine-usage-grouper", "outlier-detector"
    #"MachineUsageParser", "MachineUsageGrouper", "OutlierDetector"
    verticeResponse = requests.get("http://"+ main_node_ip + ":8086/v1/jobs/"+job_id)
    jsonVertice = verticeResponse.json()
    verticeIdMachineUsageParser = None
    verticeIdMachineUsageGrouper = None
    verticeIdOutlierDetector = None
    
    dictMachineUsageParser = {}
    dictMachineUsageGrouper = {}
    dictOutlierDetector = {}
    
    dictCombo = {}
    jobName = jsonVertice["name"]
    #dict_metrtics['tokenizer'] = []
    #dict_metrtics['counter'] = []
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

    dictMachineUsageParser = getOperatorMetrics(numOfMachineUsageParser,main_node_ip,job_id,verticeIdMachineUsageParser,MachineUsageParser_name,timestamp_prom)
    

    #dictMachineUsageGrouper = getOperatorMetrics(numOfMachineUsageGrouper,main_node_ip,job_id,verticeIdMachineUsageGrouper,MachineUsageGrouper_name,timestamp_prom)
    

    dictOutlierDetector = getOperatorMetrics(numOfOutlierDetector,main_node_ip,job_id,verticeIdOutlierDetector,OutlierDetector_name,timestamp_prom)
    

    dictCombo["operatorMetrics"] = {}
    dictCombo["operatorMetrics"]["MachineUsageParser"] = dictMachineUsageParser
    #dictCombo["operatorMetrics"]["MachineUsageGrouper"] = dictMachineUsageGrouper
    dictCombo["operatorMetrics"]["OutlierDetector"] = dictOutlierDetector
    

    querymetric = getQueryMetrics(main_node_ip, job_id, timestamp_prom)
    dictCombo["queryMetrics"] = querymetric
        
    
    return dictCombo

def getSpikeDetection(job_id, main_node_ip, timestamp_prom):
    #"parser", "average-calculator", "spike-detector"
    verticeResponse = requests.get("http://"+ main_node_ip + ":8086/v1/jobs/"+job_id)
    jsonVertice = verticeResponse.json()
    verticeIdSpikeParser = None
    verticeIdAvgCal = None
    verticeIdSpikeDetector = None
    
    dictSpikeParser = {}
    dictAvgCal = {}
    dictSpikeDetector = {}
    
    dictCombo = {}
    jobName = jsonVertice["name"]
    #dict_metrtics['tokenizer'] = []
    #dict_metrtics['counter'] = []
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "parser" in vertice["name"]:
                    #print(vertice)
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

    dictSpikeParser = getOperatorMetrics(numOfSpikeParser,main_node_ip,job_id,verticeIdSpikeParser,SpikeParser_name,timestamp_prom)
    

    dictAvgCal = getOperatorMetrics(numOfAvgCal,main_node_ip,job_id,verticeIdAvgCal,AvgCal_name,timestamp_prom)
    

    dictSpikeDetector = getOperatorMetrics(numOfSpikeDetector,main_node_ip,job_id,verticeIdSpikeDetector,SpikeDetector_name,timestamp_prom)
    

    dictCombo["operatorMetrics"] = {}
    dictCombo["operatorMetrics"]["SpikeParser"] = dictSpikeParser
    dictCombo["operatorMetrics"]["AvgCal"] = dictAvgCal
    dictCombo["operatorMetrics"]["SpikeDetector"] = dictSpikeDetector
    

    querymetric = getQueryMetrics(main_node_ip, job_id, timestamp_prom)
    dictCombo["queryMetrics"] = querymetric
        
    
    return dictCombo

def getSentimentAnalysis(job_id, main_node_ip, timestamp_prom):
    verticeResponse = requests.get("http://"+ main_node_ip + ":8086/v1/jobs/"+job_id)
    jsonVertice = verticeResponse.json()
    #"twitter-parser" and "twitter-analyser"
    verticeIdTwitterParser = None
    verticeIdTwitterAnalyser = None
    
    dictTwitterParser = {}
    dictTwitterAnalyser = {}
    
    dictCombo = {}
    jobName = jsonVertice["name"]
    #dict_metrtics['tokenizer'] = []
    #dict_metrtics['counter'] = []
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "twitter-parser" in vertice["name"]:
                    #print(vertice)
                TwitterParser_name = "twitter-parser"
                verticeIdTwitterParser = vertice["id"] 
                numOfTwitterParser = int(vertice["parallelism"])
            elif "name" in vertice and "twitter-analyser" in vertice["name"]:
                TwitterAnalyser_name = "twitter-analyser"
                verticeIdTwitterAnalyser = vertice["id"]
                numOfTwitterAnalyser = int(vertice["parallelism"])
            
    job_dict = {"job_name": jobName}
    dictCombo = job_dict.copy()

    dictTwitterParser = getOperatorMetrics(numOfTwitterParser,main_node_ip,job_id,verticeIdTwitterParser,TwitterParser_name,timestamp_prom)
    

    dictTwitterAnalyser = getOperatorMetrics(numOfTwitterAnalyser,main_node_ip,job_id,verticeIdTwitterAnalyser,TwitterAnalyser_name,timestamp_prom)
    

    dictCombo["operatorMetrics"] = {}
    dictCombo["operatorMetrics"]["TwitterParser"] = dictTwitterParser
    dictCombo["operatorMetrics"]["TwitterAnalyzer"] = dictTwitterAnalyser
    

    querymetric = getQueryMetrics(main_node_ip, job_id, timestamp_prom)
    dictCombo["queryMetrics"] = querymetric   
    
    return dictCombo

def getGoogleCloudmonitoringMetrics(job_id, main_node_ip, timestamp_prom):
    #"parser". "average-cpu-per-category" or "average-cpu-per-job"
    verticeResponse = requests.get("http://"+ main_node_ip + ":8086/v1/jobs/"+job_id)
    jsonVertice = verticeResponse.json()
    verticeIdParser = None
    verticeIdAvgCpuPerCat = None
    verticeIdAvgCpuPerJob = None
    dictParser = {}
    dictAvgCpuPerCat = {}
    dictAvgCpuPerJob = {}
    dictCombo = {}
    jobName = jsonVertice["name"]
    #dict_metrtics['tokenizer'] = []
    #dict_metrtics['counter'] = []
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "parser" in vertice["name"]:
                    #print(vertice)
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
    dictCombo["operatorMetrics"] = {}
    dictParser = getOperatorMetrics(numOfParser,main_node_ip,job_id,verticeIdParser,Parser_name,timestamp_prom)
    dictCombo["operatorMetrics"]["Parser"] = dictParser

    if verticeIdAvgCpuPerCat is not None:
        dictAvgCpuPerCat = getOperatorMetrics(numOfAvgCpuPerCat,main_node_ip,job_id,verticeIdAvgCpuPerCat,AvgCpuPerCat_name,timestamp_prom)
        dictCombo["operatorMetrics"]["AvgCpuPerCat"] = dictAvgCpuPerCat
        
    if verticeIdAvgCpuPerJob is not None:
        dictAvgCpuPerJob = getOperatorMetrics(numOfAvgCpuPerJob,main_node_ip,job_id,verticeIdAvgCpuPerJob,AvgCpuPerJob_name,timestamp_prom)
        dictCombo["operatorMetrics"]["AvgCpuPerJob"] = dictAvgCpuPerJob

     
    
    
    
    
    

    querymetric = getQueryMetrics(main_node_ip, job_id, timestamp_prom)
    dictCombo["queryMetrics"] = querymetric
    
    return dictCombo

def getAdanalytics(job_id, main_node_ip, timestamp_prom):
    #click-parser,impression-parser, clicks-counter, impressions-counter, rollingCTR
    #"Ads Analytics"
    
    verticeResponse = requests.get("http://"+ main_node_ip + ":8086/v1/jobs/"+job_id)
    jsonVertice = verticeResponse.json()

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
    #dict_metrtics['tokenizer'] = []
    #dict_metrtics['counter'] = []
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
    #if verticeIdClickParser is not None:
    dictClickParser = getOperatorMetrics(numOfClickParser,main_node_ip,job_id,verticeIdClickParser,ClickParser_name,timestamp_prom)
    dictImpressionParser = getOperatorMetrics(numOfImpressionParser,main_node_ip,job_id,verticeIdImpressionParser,ImpressionParser_name,timestamp_prom)
    dictClicksCounter = getOperatorMetrics(numOfClicksCounter,main_node_ip,job_id,verticeIdClicksCounter,ClicksCounter_name,timestamp_prom)
    dictImpressionsCounter = getOperatorMetrics(numOfImpressionsCounter,main_node_ip,job_id,verticeIdImpressionsCounter,ImpressionsCounter_name,timestamp_prom)
    dictRollingCTR = getOperatorMetrics(numOfRollingCTR,main_node_ip,job_id,verticeIdRollingCTR,RollingCTR_name,timestamp_prom)
    dictCombo["operatorMetrics"] = {}
    dictCombo["operatorMetrics"]["ClickParser"] = dictClickParser
    dictCombo["operatorMetrics"]["ImpressionParser"] = dictImpressionParser
    dictCombo["operatorMetrics"]["ClicksCounter"] = dictClicksCounter
    dictCombo["operatorMetrics"]["ImpressionsCounter"] = dictImpressionsCounter
    dictCombo["operatorMetrics"]["RollingCTR"] = dictRollingCTR
    

    querymetric = getQueryMetrics(main_node_ip, job_id, timestamp_prom)
    dictCombo["queryMetrics"] = querymetric
    #dictCombo.update(querymetric)
   
    return dictCombo
    
def getSmartGrid(job_id, main_node_ip, timestamp_prom):
    verticeResponse = requests.get("http://"+ main_node_ip + ":8086/v1/jobs/"+job_id)
    jsonVertice = verticeResponse.json()
    verticeIdglobalavgload = None
    verticeIdlocalavgload = None
    dictGlobalload = {}
    dictLocalload = {}
    dictCombo = {}
    jobName = jsonVertice["name"]
    #dict_metrtics['tokenizer'] = []
    #dict_metrtics['counter'] = []
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "global average load" in vertice["name"]:
                    #print(vertice)
                globalAvgLoad_name = "global average load"
                verticeIdglobalavgload = vertice["id"] 
                numOfGlobalAvgLoad = int(vertice["parallelism"])
            elif "name" in vertice and "local average load" in vertice["name"]:
                localAvgLoad_name = "local average load"
                verticeIdlocalavgload = vertice["id"]
                #print(f"the counter id is {verticeIdcounter} \n\n\n\n")
                numOfLocalAvgLoad = int(vertice["parallelism"])
    job_dict = {"job_name": jobName}
    dictCombo = job_dict.copy()
    dictCombo["operatorMetrics"] = {}
    if verticeIdglobalavgload is not None:
        dictGlobalload = getOperatorMetrics(numOfGlobalAvgLoad,main_node_ip,job_id,verticeIdglobalavgload,globalAvgLoad_name,timestamp_prom)
        dictCombo["operatorMetrics"]["Globalload"] = dictGlobalload
        
    if verticeIdlocalavgload is not None:
        dictLocalload = getOperatorMetrics(numOfLocalAvgLoad,main_node_ip,job_id,verticeIdlocalavgload,localAvgLoad_name,timestamp_prom)
        dictCombo["operatorMetrics"]["Localload"] = dictLocalload


    querymetric = getQueryMetrics(main_node_ip, job_id, timestamp_prom)
    dictCombo["queryMetrics"] = querymetric
    
    return dictCombo

def getWordCount(job_id, main_node_ip, timestamp_prom):
    verticeResponse = requests.get("http://"+ main_node_ip + ":8086/v1/jobs/"+job_id)
    jsonVertice = verticeResponse.json()
    
    verticeIdtokenizer = None
    verticeIdcounter = None
    dictTokenizer = {}
    dictCounter = {}
    dictCombo = {}
    jobName = jsonVertice["name"]
    #dict_metrtics['tokenizer'] = []
    #dict_metrtics['counter'] = []
    if "vertices" in jsonVertice:

        for vertice in jsonVertice["vertices"]:
                
            if "name" in vertice and "tokenizer" in vertice["name"]:
                    #print(vertice)
                tokenizer_name = "tokenizer"
                verticeIdtokenizer = vertice["id"] 
                numOfTokenizer = int(vertice["parallelism"])
            elif "name" in vertice and "counter" in vertice["name"]:
                counter_name = "counter"
                verticeIdcounter = vertice["id"]
                #print(f"the counter id is {verticeIdcounter} \n\n\n\n")
                numOfCounter = int(vertice["parallelism"])
    #if verticeIdtokenizer is not None:
    dictTokenizer = getOperatorMetrics(numOfTokenizer,main_node_ip,job_id,verticeIdtokenizer,tokenizer_name,timestamp_prom)

        
    #if verticeIdcounter is not None:
    dictCounter = getOperatorMetrics(numOfCounter,main_node_ip,job_id,verticeIdcounter,counter_name,timestamp_prom)

    # Create a new dictionary with "job_name": job_name
    job_dict = {"job_name": jobName}

# Merge the new dictionary with dictTokenizer and dictCounter using update()
    dictCombo = job_dict.copy()

    dictCombo["operatorMetrics"] = {}
    dictCombo["operatorMetrics"]["Tokenizer"] = dictTokenizer
    dictCombo["operatorMetrics"]["Counter"] = dictCounter
    
    

    querymetric = getQueryMetrics(main_node_ip, job_id, timestamp_prom)
    dictCombo["queryMetrics"] = querymetric
    
    #dictCombo.update(dictTokenizer)
    #dictCombo.update(dictCounter)

    return dictCombo

@click.command()
@click.option('--main_node_ip', type=str, help='node address where prometheus and flink resides')
@click.option('--job_id', type=str, help='node address where prometheus and flink resides')
@click.option('--job_run_time', type=str, help='node address where prometheus and flink resides')
@click.option('--job_parallelization', type=str, help='node address where prometheus and flink resides')
@click.option('--job_query_number', type=str, help='node address where prometheus and flink resides')
@click.option('--job_window_size', type=str, help='node address where prometheus and flink resides')
@click.option('--job_window_slide_size', type=str, help='node address where prometheus and flink resides')
@click.option('--producer_event_per_second', type=str, help='node address where prometheus and flink resides')

# 'job_run_time': 6000, 
# 'job_program': 'Ads Analytics', 
# 'job_parallelization': '2,2,2,2,2', 
# 'job_query_number': 1, 
# 'job_window_size': 100, 
# 'job_window_slide_size': 10, 
# 'producer_event_per_second': '100', 
# 'node0.sat.maki-test.emulab.net',

def main(main_node_ip, job_id, job_run_time, job_parallelization, job_query_number,job_window_size,job_window_slide_size, producer_event_per_second):
    #list_of_all_jobs = []
    #url = "http://"+main_node_ip+":8086/v1/jobs/overview", 
    #requested_main_node_ip_jobs = requests.get(url)
    #print(requested_main_node_ip_jobs)
    #main_node_ip_jobs_json = requested_main_node_ip_jobs.json()
    #print(main_node_ip_jobs_json)
    ###You have to see that everytime which job is being called.
    response = requests.get("http://"+ main_node_ip + ":8086/v1/jobs/"+job_id)
    response = response.json()
    #node0.sat.maki-test.emulab.net
    jobName = response["name"]
    startTime = response["start-time"]
    timestamp_prom = startTime // 1000
    timestamp_prom = timestamp_prom + 300
    timestamp_prom = str(timestamp_prom)
    #"start-time": 1695578058128
    #for job_in_main_node_ip in requested_main_node_ip_jobs.json()["jobs"]:
    #    state = job_in_main_node_ip['state']
    #    if state == 'RUNNING':
    #        timestamp_prom = (job_in_main_node_ip["start-time"]) // 1000
    #        timestamp_prom = timestamp_prom + 300
    #        timestamp_prom = str(timestamp_prom)
    #        #print(job_in_main_node_ip)
    #        job_id = job_in_main_node_ip['jid']
    #        jobName = job_in_main_node_ip['name']
    
    current_directory = os.getcwd()

    # Specify the folder name you want to create
    folder_name = jobName

    # Combine the current directory and folder name to create the full folder path
    full_folder_path = os.path.join(current_directory, folder_name)
    if not os.path.exists(full_folder_path):
        os.makedirs(full_folder_path)
        print(f"Folder '{folder_name}' created successfully at '{full_folder_path}'")
    else:
        print(f"Folder '{folder_name}' already exists at '{full_folder_path}'")
    
    

    if jobName == 'Google Cloud Monitoring':
        processedMetrics = getGoogleCloudmonitoringMetrics(job_id, main_node_ip, timestamp_prom)
    elif jobName == 'Ads Analytics':
        processedMetrics = getAdanalytics(job_id, main_node_ip, timestamp_prom) 

    elif jobName == 'Flink smart grid job':
        processedMetrics = getSmartGrid(job_id, main_node_ip, timestamp_prom)
    elif jobName == 'Flink word count job':
        processedMetrics = getWordCount(job_id, main_node_ip, timestamp_prom)
    elif jobName == "Sentiment Analysis":
        processedMetrics = getSentimentAnalysis(job_id, main_node_ip, timestamp_prom)
    elif jobName == "Spike Detection":
        processedMetrics = getSpikeDetection(job_id, main_node_ip, timestamp_prom)
    elif jobName == "Trending Topics":
        processedMetrics = getTrendingTopics(job_id, main_node_ip, timestamp_prom)
    elif jobName == "Logs Processing":
        processedMetrics = getLogsProcessing(job_id, main_node_ip, timestamp_prom)
    elif jobName == "Bargain Index":
        processedMetrics = getBargainIndex(job_id, main_node_ip, timestamp_prom)
    elif jobName == "Click Analytics":
        processedMetrics = getClickAnalytics(job_id, main_node_ip, timestamp_prom)
    elif jobName == "Linear Road":
        processedMetrics = getLinearRoad(job_id, main_node_ip, timestamp_prom)
    elif jobName == "Machine Outlier":
        processedMetrics = getMachineOutlier(job_id, main_node_ip, timestamp_prom)
    elif jobName == "Traffic Monitoring":
        processedMetrics = getTrafficMonitoring(job_id, main_node_ip, timestamp_prom)
    elif jobName == "TPCH":
        processedMetrics = getTpch(job_id, main_node_ip, timestamp_prom)
    print('printing processed metrics#####################################################################')
    #print(processedMetrics)
    metaInfo = {
        'job_run_time': job_run_time, 
        'job_parallelization': job_parallelization, 
        'job_query_number': job_query_number, 
        'job_window_size': job_window_size, 
        'job_window_slide_size': job_window_slide_size, 
        'producer_event_per_second': producer_event_per_second,
    }
    # Specify the file name
    meta_file_name = "metaInfo-"+job_id+".json"
    evaluation_file_name = "evaluationMetrics-"+job_id+".json"
    # Combine the current directory and file name to create the full file path
    metaFile = os.path.join(full_folder_path, meta_file_name)
    evaluationFile = os.path.join(full_folder_path, evaluation_file_name)

    try:
        # Write the dictionary to a JSON file
        with open(metaFile, 'w') as json_file:
            json.dump(metaInfo, json_file, indent=4)
        # Write the dictionary to a JSON file
        with open(evaluationFile, 'w') as json_file:
            json.dump(processedMetrics, json_file, indent=4)

    except Exception as e:
        print(f"An error occurred: {e}")
    #node0.sat.maki-test.emulab.net
    #d39de0661be1f95083f18f8060869378
            
if __name__ == "__main__":
    """ Main function
    """
    main()
