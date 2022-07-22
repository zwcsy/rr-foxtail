from urllib.request import urlopen
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from flask import Flask
import json
import tqdm

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'use_ssl': False}])

def add():
	url = 'http://localhost:5001/get_alerts'
	response = urlopen(url)
	string = response.read().decode('utf-8')
	json_obj = json.loads(string)
	print("Retrieve success, total of " + str(len(json_obj['results'])) + " alerts")
	for i in json_obj['results']:
		obj = {
			"created_at": i["created_at"],
			"updated_at": i["updated_at"],
			"state": i["state"],
			"cnchost": i["alert_type_details"]["detail"]["cnchost"],
			"devicename": i["alert_type_details"]["detail"]["devicename"],
			"dstcountry": i["alert_type_details"]["detail"]["dstcountry"],
			"dstipv4": i["alert_type_details"]["detail"]["dstipv4"],
			"dstisp": i["alert_type_details"]["detail"]["dstisp"],
			"dstport": i["alert_type_details"]["detail"]["dstport"],
			"srcipv4": i["alert_type_details"]["detail"]["srcipv4"],
			"srcport": i["alert_type_details"]["detail"]["srcport"],
			"virus": i["alert_type_details"]["detail"]["virus"],
			"action": i["alert_type_details"]["summary"]["action"],
			"created_by": i["created_by"]["username"],
			"updated_by": i["updated_by"]["username"],
		}
	yield obj

@app.route('/')
def main():
	es.indices.create(
		index = "imported-alerts",
		body = {
		  "mappings": {
		    "properties": {
		      "created_at": {"type": "date"},
		      "updated_at": {"type": "date"},
		      "state": {"type": "keyword"},
		      "cnchost": {"type": "text"},
		      "devicename": {"type": "text"},
		      "dstcountry": {"type": "keyword"},
		      "dstipv4": {"type": "ip"},
		      "dstisp": {"type": "text"},
		      "dstport": {"type": "integer"},
		      "srcipv4": {"type": "ip"},
		      "srcport": {"type": "integer"},
		      "virus": {"type": "keyword"},
		      "action": {"type": "keyword"},
		      "created_by": {"type": "keyword"},
		      "updated_by": {"type": "keyword"},
		    },
		  },
		},
	)
	print("Attempting to index externally retrieved alerts, kindly wait")
	log = tqdm.tqdm(unit="alerts", total=len(json_obj['results']))
	good = 0
	for ok, action in streaming_bulk(
		client=es, index="imported-alerts", actions=add(),
	):
		log.update(1)
		good = good + ok
	print("Successfully indexed %d/%d alerts" % (good, len(json_obj['results'])))
	return str(good)
