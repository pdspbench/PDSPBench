import json
import os
import logging
import socket
import sys
import time
import pandas as pd
import click
from confluent_kafka import Producer
#/home/legion/Desktop/park2/dsp_jobs/Data/sentimentAnalysis_tweetstream.jsonl

#List of app_types that can be passed from CLI
WORD_COUNT = "Word_Count"
SMART_GRID = "Smart_Grid"
AD_ANALYTICS = "Ad_Analytics"
GOOGLE = "Google_Cloud_Monitoring"
SENTIMENT = "Sentiment_Analysis"
SPIKE = "Spike_detection"
LOG = "Log_Processing"
TRENDING = "Trending_Topic"
OUTLIER = "Machine_Outlier"
CLICKANALYTICS = "Click_Analytics"
BARGAIN = "Bargain_Index"
TRAFFIC = "Traffic_Monitoring"
TPC = "Tpch"
TPCX = "Tpcx"
LRB ="LRB"
# Definig the path of the directory where data files are stored
BASE_DIR = "/home/legion/Desktop/dsp_cloudlab_profile/"
# List of available data set file names stored in BASE_DIR
FILE_NAME_WC = "word-count.txt"
FILE_NAME_SG = "smart-grid.csv"
FILE_NAME_AA = "adAnalytics.dat"
FILE_NAME_GCM = "googleCloudMonitoring.csv"
FILE_NAME_SA = "sentimentAnalysis_tweetstream.json"
FILE_NAME_SD = "spikeDetection_sensors.dat"
FILE_NAME_LP = "http.log"
FILE_NAME_TT = "ttopic.csv"
FILE_NAME_MO = "outlier.csv"
FILE_NAME_CA = "click-stream.json"
FILE_NAME_BI = "stocks.csv"
FILE_NAME_TM = "taxi-traces.csv"
FILE_NAME_TP = "tpc_h.csv"
FILE_NAME_TPCX = "tpc_x.csv"
FILE_NAME_LRB = "lrb.csv"


def wordcount(event_per_second, kafka_bootstrap_server, kafka_input_topic):
    """
        Generates event. An event consists of 5 words
    """

    

    logging.info("\n\t\t\tKafka publishing on topic " + kafka_input_topic + "\n")
    producer_conf = {
        'bootstrap.servers': kafka_bootstrap_server,#'localhost:9092',
        'client.id': socket.gethostname(),
        'message.max.bytes': 1000000000,
        'queue.buffering.max.messages': 1000000000,
        'compression.type': 'gzip'
    }
    producer = Producer(producer_conf)
    

    # Open the file in read mode
    with open(BASE_DIR+FILE_NAME_WC, 'r') as file:
        # Read the content of the file into a string variable
        wc_example = file.read()

    wc_example_list = wc_example.split()
    event_list = list()
    event = ""
    count_words = 0
    count_of_events = 0
    for word in wc_example_list:

        if count_words < 5:
            event = event + " " + word
            count_words = count_words + 1
        else:
            
            producer.produce(
                topic=kafka_input_topic,
                value=json.dumps(event)
            )
            
            event = ""
            count_words = 0
            count_of_events+=1

        if count_of_events == event_per_second:
            count_of_events=0
            producer.flush()
            time.sleep(1)
            
    
def event_producer(event_per_second, kafka_bootstrap_server, kafka_input_topic, app_type):
    #print('here')
    if app_type == SMART_GRID:
        all_events = read_data_file(BASE_DIR+FILE_NAME_SG, event_per_second, app_type)

    elif app_type == AD_ANALYTICS:
        all_events = read_data_file(BASE_DIR+FILE_NAME_AA, event_per_second, app_type)
        
    elif app_type == GOOGLE:
        all_events = read_data_file(BASE_DIR+FILE_NAME_GCM, event_per_second, app_type)
        
    elif app_type == SENTIMENT:
        all_events = read_data_file(BASE_DIR+FILE_NAME_SA, event_per_second, app_type)

    elif app_type == SPIKE:
        all_events = read_data_file(BASE_DIR+FILE_NAME_SD, event_per_second, app_type)

    elif app_type == LOG:

        all_events = read_data_file(BASE_DIR+FILE_NAME_LP, event_per_second, app_type)



    elif app_type == TRENDING:

        all_events = read_data_file(BASE_DIR+FILE_NAME_TT, event_per_second, app_type)



    elif app_type == OUTLIER:

        all_events = read_data_file(BASE_DIR+FILE_NAME_MO, event_per_second, app_type)



    elif app_type == CLICKANALYTICS:

        all_events = read_data_file(BASE_DIR+FILE_NAME_CA, event_per_second, app_type)



    elif app_type == BARGAIN:

        all_events = read_data_file(BASE_DIR+FILE_NAME_BI, event_per_second, app_type)



    elif app_type == TRAFFIC:

        all_events = read_data_file(BASE_DIR+FILE_NAME_TM, event_per_second, app_type)



    elif app_type == TPC:

        all_events = read_data_file(BASE_DIR+FILE_NAME_TP, event_per_second, app_type)


    
    elif app_type == TPCX:

        all_events = read_data_file(BASE_DIR+FILE_NAME_TPCX, event_per_second, app_type)


    elif app_type == LRB:

        all_events = read_data_file(BASE_DIR+FILE_NAME_LRB, event_per_second, app_type)

    
    producer_conf = {
        'bootstrap.servers': kafka_bootstrap_server,#'localhost:9092',
        'client.id': socket.gethostname(),
        'message.max.bytes': 1000000000,
        'queue.buffering.max.messages': 1000000000,
    }
    

    logging.info("\t\t\tProducer config :")
    for key, value in producer_conf.items():
        logging.info("\t\t\t\t" + str(key) + " : " + str(value))

    kafka_topic = kafka_input_topic

    logging.info("\n\t\t\tKafka publishing on topic " + kafka_topic + "\n")

    producer = Producer(producer_conf)

    batch_count = 1
    for batch_data in all_events:

        start = time.time()

        for event_in_batch in batch_data:
            
            if app_type == SMART_GRID or app_type == SENTIMENT or app_type == CLICKANALYTICS:
                producer.produce(
            
                    topic=kafka_topic,
                
                    value=json.dumps(event_in_batch)
                )
            else:
                producer.produce(
                    
            
                    topic=kafka_topic,
                
                    value=event_in_batch
                )

        time.sleep(1)
        producer.flush()
        end = time.time()
        time_consumed = end - start
        logging.info(
            "\t\t\tTime consumed for publishing batch number " + str(batch_count) + ":: " + str(time_consumed) + "\n")
        batch_count += 1
    

def read_data_file(file_path, batch_size, app_type):

    
    batched_event_list = []

    if app_type == SMART_GRID:

        try:
            data_frame = pd.read_csv(file_path, sep=',', header=None)
        except FileNotFoundError:
            logging.error("File  not found" + file_path)
            sys.exit(404)
           
    elif app_type == AD_ANALYTICS:

        try:
            data_frame = pd.read_csv(file_path, sep='\t', header=None)
            
        except FileNotFoundError:
            logging.error("File  not found" + file_path)
            sys.exit(404)

    elif app_type == GOOGLE:
        try:
            data_frame = pd.read_csv(file_path, sep=',', header=None)
        except FileNotFoundError:
            logging.error("File  not found" + file_path)
            sys.exit(404)

    elif app_type == SENTIMENT:

        try:
            start = time.time()
            data_frame = pd.read_json(file_path)
            end = time.time()
    
        except FileNotFoundError:
            logging.error("File  not found" + file_path)
            sys.exit(404)
    elif app_type == SPIKE:
        try:
            data_frame = pd.read_csv(file_path, sep=' ', header=None)
        except FileNotFoundError:
            logging.error("File  not found" + file_path)
            sys.exit(404)
    elif app_type == LOG:
        try:
            data_frame = pd.read_csv(file_path, delimiter=r'\s+', header=None)


        except FileNotFoundError:
            logging.error("File  not found" + file_path)
            sys.exit(404)
    elif app_type == TRENDING:
        try:
            start = time.time()
            data_frame = pd.read_csv(file_path, sep=',', header=None)
            end = time.time()


        except FileNotFoundError:
            logging.error("File  not found" + file_path)
            sys.exit(404)
    elif app_type == OUTLIER:
        try:
            data_frame = pd.read_csv(file_path, sep=',', header=None)



        except FileNotFoundError:
            logging.error("File  not found" + file_path)
            sys.exit(404)
    elif app_type == CLICKANALYTICS:
        try:
        
            data_frame = pd.read_json(file_path, lines=True)

    
        except FileNotFoundError:
            logging.error("File  not found" + file_path)
            sys.exit(404)
    elif app_type == BARGAIN:
        try:
            data_frame = pd.read_csv(file_path, sep=',', header=None)



        except FileNotFoundError:
            logging.error("File  not found" + file_path)
            sys.exit(404)
    elif app_type == TRAFFIC:
        try:
            data_frame = pd.read_csv(file_path, sep=',', header=None)



        except FileNotFoundError:
            logging.error("File  not found" + file_path)
            sys.exit(404)
    
    elif app_type == TPC:
        try:
            data_frame = pd.read_csv(file_path, sep=',', header=None)



        except FileNotFoundError:
            logging.error("TPCH File  not found" + file_path)
            sys.exit(404)

    elif app_type == TPCX:
        try:
            data_frame = pd.read_csv(file_path, sep=',', header=None)



        except FileNotFoundError:
            logging.error("TPCX File  not found" + file_path)
            sys.exit(404)

    elif app_type == LRB:
        try:
            data_frame = pd.read_csv(file_path, sep=',', header=None)



        except FileNotFoundError:
            logging.error("LRB File  not found" + file_path)
            sys.exit(404)


    number_of_events = len(data_frame.index)

    current_index = 0

    while current_index < number_of_events:

        df_batched = None
        if current_index + batch_size < number_of_events:
            df_batched = data_frame.iloc[current_index: current_index + batch_size]
            current_index = current_index + batch_size

        else:

            df_batched = data_frame.iloc[current_index: number_of_events]
            current_index = number_of_events
        
        
        if  app_type == SMART_GRID:
            batch_data = df_batched.to_csv(header=False, index=False, sep=',').strip()

            temp_list1 = batch_data.split('\n')
            batched_event_list.append(temp_list1)

            

        elif app_type == AD_ANALYTICS:
            
            batch_data = df_batched.to_csv(header=False, index=False, sep='\t').strip()

            temp_list = batch_data.split('\n')
            batched_event_list.append(temp_list)
            
        
        elif app_type == GOOGLE:
            batch_data = df_batched.to_csv(header=False, index=False, sep=',').strip()
            temp_list1 = batch_data.split('\n')
            batched_event_list.append(temp_list1)

        elif app_type == SENTIMENT:
            
            batch_data = df_batched.to_json(orient='records')
            batched_event_list.append(json.loads(batch_data))


        elif app_type == SPIKE:
            batch_data = df_batched.to_csv(header=False, index=False, sep=' ').strip()
            temp_list1 = batch_data.split('\n')
            batched_event_list.append(temp_list1)

        elif app_type == LOG:
            batch_data = df_batched.to_csv(header=False, index=False, sep=' ').strip()
            temp_list1 = batch_data.split('\n')
            batched_event_list.append(temp_list1)

        elif app_type == TRENDING:
            batch_data = df_batched.to_csv(header=False, index=False, sep=',').strip()
            temp_list1 = batch_data.split('\n')
            batched_event_list.append(temp_list1)

        elif app_type == OUTLIER:
            batch_data = df_batched.to_csv(header=False, index=False, sep=',').strip()
            temp_list1 = batch_data.split('\n')
            batched_event_list.append(temp_list1)

        elif app_type == CLICKANALYTICS:
            batch_data = df_batched.to_json(orient='records')
            batched_event_list.append(json.loads(batch_data))


        elif app_type == BARGAIN:
            batch_data = df_batched.to_csv(header=False, index=False, sep=',').strip()
            temp_list1 = batch_data.split('\n')
            batched_event_list.append(temp_list1)
        
        elif app_type == TRAFFIC:
            batch_data = df_batched.to_csv(header=False, index=False, sep=',').strip()
            temp_list1 = batch_data.split('\n')
            batched_event_list.append(temp_list1)
        
        elif app_type == TPC:
            batch_data = df_batched.to_csv(header=False, index=False, sep=',').strip()
            temp_list1 = batch_data.split('\n')
            batched_event_list.append(temp_list1)

        elif app_type == TPCX:
            batch_data = df_batched.to_csv(header=False, index=False, sep=',').strip()
            temp_list1 = batch_data.split('\n')
            batched_event_list.append(temp_list1)   
            
        elif app_type == LRB:
            batch_data = df_batched.to_csv(header=False, index=False, sep=',').strip()
            temp_list1 = batch_data.split('\n')
            batched_event_list.append(temp_list1)   
            
            

    return batched_event_list


@click.command()
@click.option('--event_per_second', type=int, help='Define the event per second for the application')
@click.option('--app_type', type=str, help='Type of application like "Word Count",etc')
@click.option('--kafka_bootstrap_server', type=str, help='Define where the kafka bootstrap server is present')
@click.option('--kafka_input_topic', type=str, help='Defines the topic producer sends events on.')


def main(event_per_second, app_type, kafka_bootstrap_server, kafka_input_topic):

    if app_type == WORD_COUNT:
        wordcount(event_per_second, kafka_bootstrap_server, kafka_input_topic)

    else:
        event_producer(event_per_second, kafka_bootstrap_server, kafka_input_topic, app_type)


if __name__ == "__main__":
    """ Main function
    """
    main()
