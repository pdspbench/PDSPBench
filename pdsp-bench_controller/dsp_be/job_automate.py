import requests
import time
job_query_mapping = {
    "Word Count": [1],
    #"Bargain Index": [1],
    #"Google cloud Monitoring":[1,2],
    #"Click Analytics": [1,2],
    #"Log Processing":[1,2],
    #"Linear Road": [1,2,3,4],
    #"Smart Grid": [1,2],
    #"Ad Analytics": [1],
    #"Sentiment Analysis": [1],
    #"Trending Topics": [1],
    #
    #"Machine Outlier": [1],
    #"Traffic Monitoring": [1],
    #"Spike Detection": [1],
    #"TPCH": [1],
    
}
count = 0
parallelism_degrees = ['2'] # Have to change this , '32', '8','2'
event_rates = [50000]#,50000, 20000, 10000, 5000, 1000]# Have to change this , 20000, 10000, 5000, 1000
cluster_id = '89aae67ed1044d91927765650d331da4' # Have to change this

count=0

for job_name in job_query_mapping:
    queries = job_query_mapping[job_name]

    for query in queries:

        for parallelism_degree in parallelism_degrees:

            for event_rate in event_rates:
            
                data_sent = {
                    'job_class': job_name, 
                    'job_class_input_type': 'Kafka', 
                    'job_class_input': event_rate, 
                    'job_query_name': query, 
                    'job_pds': [parallelism_degree, parallelism_degree, parallelism_degree, parallelism_degree, parallelism_degree, parallelism_degree, parallelism_degree], 
                    'job_window_size': '10', 
                    'job_window_slide_size': '1', 
                    'job_run_time': 2, 
                    'job_google_lateness': 0, 
                    'job_threshold': 5, 
                    'num_of_times_job_run': 1
                }
                print('##################################################################\n\n\n\n')
                print("Data sending...\n")
                print(data_sent)
                requests.post("http://localhost:8000/infra/jobcreate/"+cluster_id, json=data_sent)
                #count+=1
                #print((count*4)/60)
                
                
                print('DONE')
                print('##################################################################\n\n\n\n')
    time.sleep(60)

