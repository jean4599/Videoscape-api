import requests
import json
import operator
from stage1 import get_time_period

nodes = []
edges = []
concept_dic = {} #{conceptID: couster label}
dic = {} #{cluster label: }

def comp(x,y):
	return len(x[0])-len(y[0])

def node_aggregate(stage1_nodes,nodes):
	print('Process node...')

	cluster_request = ''
	for node in nodes:
		cluster_request += (node['label'] + '\n')

	print('Send request to meaningcloud')

	url = "http://api.meaningcloud.com/clustering-1.1"
	payload = "key=7669c401635f55cdeb14a325326ac695&lang=en&mode=dg&txt="+cluster_request
	headers = {'content-type': 'application/x-www-form-urlencoded'}

	response = requests.request("POST", url, data=payload, headers=headers)

	result = json.loads(response.text)
	clusters = result['cluster_list']
	print('Get meaningcloud result')
	
	for item in clusters:
		if (int(item['size']) > 2 and item['title']!='Other Topics'):
			cluster = {}
			time = []
			
			for index in item['document_list']:
				label = item['document_list'][index].lower()
				if(label in cluster):
					cluster[label] = cluster[label]+1
				else:
					cluster[label] = 0

				#For edge reference
				concept_dic[nodes[int(index)-1]['id']] = label 

				t=nodes[int(index)-1]['time']
				if(type(t) is float):
					time.append(nodes[int(index)-1]['time'])

			s = sorted(cluster.items(), cmp = comp)
			s = sorted(s, key = operator.itemgetter(1), reverse = True)
			cluster = {
				'id':s[0][0],
				'label':s[0][0],
				'timestamp':time
			}
			if cluster['label'] in dic:
				dic[cluster['label']]['timestamp'] += cluster['timestamp']
			else: 
				dic[cluster['label']] = cluster

	result = []
	for topic in dic:
		timestamp = dic[topic]['timestamp']
		timestamp = sorted(timestamp)
		t = get_time_period(timestamp)
		dic[topic]['time'] = t[0]
		dic[topic]['end'] = t[1]
		result.append(dic[topic])

	return result

def edge_aggregate(edges):
	print('process edges...')
	edge_dic = {}
	for edge in edges:
		fr=''
		to=''
		if(edge['from'] in concept_dic):
			fr = concept_dic[edge['from']]
		if(edge['to'] in concept_dic):
			to = concept_dic[edge['to']]
		if fr!='' and to!='':
			index = fr+'_'+to
			if index in edge_dic:
				edge_dic[index]['width'] += 1
			else:
				edge_dic[index]={
					'from': fr,
					'to': to,
					'width': 0
				}
	result = []
	for key in edge_dic:
		if(edge_dic[key]['width']>1):
			result.append(edge_dic[key])
	return result

def get_links(stage1_nodes, data):
	print('Stage2_1 start processing...')

	global nodes, edges, concept_dic, dic
	nodes = []
	edges = []
	concept_dic = {} #{conceptID: couster label}
	dic = {} #{cluster label: }
	
	for user in data:
		if 'nodes' in data[user] and 'edges' in data[user]:
			for concept in data[user]['nodes']:
				nodes.append(concept)
			for edge in data[user]['edges']:
				edges.append(edge)

	result_node = node_aggregate(stage1_nodes,nodes)
	result_edge = edge_aggregate(edges)

	result = {}
	result['nodes'] = result_node
	result['edges'] = result_edge
	print('Stage2 end processing')
	return result
