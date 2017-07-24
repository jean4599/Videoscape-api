import requests
import json
import operator
import numpy as np
import math

class DBSCAN:
	UNCLASSIFIED = False
	NOISE = None

	def _dist(self, p,q):
		return math.sqrt(np.power(p-q,2).sum())

	def _eps_neighborhood(self, p,q,eps):
		return self._dist(p,q) < eps

	def _region_query(self, m, point_id, eps):
	    n_points = m.shape[0]
	    seeds = []
	    for i in range(0, n_points):
	        if self._eps_neighborhood(m[point_id], m[i], eps):
	            seeds.append(i)
	    return seeds

	def _expand_cluster(self, m, classifications, point_id, cluster_id, eps, min_points):
	    seeds = self._region_query(m, point_id, eps)
	    if len(seeds) < min_points:
	        classifications[point_id] = self.NOISE
	        return False
	    else:
	        classifications[point_id] = cluster_id
	        for seed_id in seeds:
	            classifications[seed_id] = cluster_id
	            
	        while len(seeds) > 0:
	            current_point = seeds[0]
	            results = self._region_query(m, current_point, eps)
	            if len(results) >= min_points:
	                for i in range(0, len(results)):
	                    result_point = results[i]
	                    if classifications[result_point] == self.UNCLASSIFIED or \
	                       classifications[result_point] == self.NOISE:
	                        if classifications[result_point] == self.UNCLASSIFIED:
	                            seeds.append(result_point)
	                        classifications[result_point] = cluster_id
	            seeds = seeds[1:]
	        return True
	        
	def dbscan(self, m, eps, min_points):
		"""Implementation of Density Based Spatial Clustering of Applications with Noise
		See https://en.wikipedia.org/wiki/DBSCAN

		scikit-learn probably has a better implementation

		Uses Euclidean Distance as the measure

		Inputs:
		m - A matrix whose columns are feature vectors
		eps - Maximum distance two points can be to be regionally related
		min_points - The minimum number of points to make a cluster

		Outputs:
		An array with either a cluster id number or dbscan.NOISE (None) for each
		column vector in m.
		"""
		self.UNCLASSIFIED = False
		self.NOISE = None
		cluster_id = 1
		n_points = m.shape[0]
		classifications = [self.UNCLASSIFIED] * n_points
		for point_id in range(0, n_points):
			point = m[point_id]
			if classifications[point_id] == self.UNCLASSIFIED:
				if self._expand_cluster(m, classifications, point_id, cluster_id, eps, min_points):
					cluster_id = cluster_id + 1
		return {'classlist':classifications,'totalCluster':cluster_id-1}

def find_majority(k):
    myMap = {}
    maximum = ( '', 0 ) # (occurring element, occurrences)
    for n in k:
        if n in myMap: myMap[n] += 1
        else: myMap[n] = 1

        # Keep track of maximum on the go
        if myMap[n] > maximum[1] and n!=None: maximum = (n,myMap[n])

    return maximum
def get_time_period(time_list):
	
    nparray = np.array(time_list)
    result = DBSCAN().dbscan(nparray, 10, 2)
    
    classlist = result['classlist']
    total_cluster = result['totalCluster']

    m = find_majority(classlist)
    x = 1
    begin = '?'
    end = '?'
    for index, ele in enumerate(classlist):
        if ele == m[0] and m[0]!='':
            if x == 1:
                begin = time_list[index]
            elif x == m[1]:
                end = time_list[index]
                break
            x = x+1
    period = (begin, end)
    return period

def get_cluster(data):
	
	label_time_list = []
	cluster_request = ''
	for user in data:
		for concept in data[user]:
			if(concept['word']):
				x = {
					'label':concept['word'],
					'time':concept['time']
				}
				label_time_list.append(x)
				cluster_request += (concept['word'] + '\n')
	
	print('Send request to meaningcloud')

	url = "http://api.meaningcloud.com/clustering-1.1"
	payload = "key=7669c401635f55cdeb14a325326ac695&lang=en&mode=dg&txt="+cluster_request
	headers = {'content-type': 'application/x-www-form-urlencoded'}

	response = requests.request("POST", url, data=payload, headers=headers)

	result = json.loads(response.text)
	clusters = result['cluster_list']
	print(clusters)

	dic = {}
	for item in clusters:
		if (int(item['size']) > 2 and item['title']!='Other Topics'):
			cluster = {}
			time = []
			for index in item['document_list']:
				label = item['document_list'][index]
				if(label in cluster):
					cluster[label] = cluster[label]+1
				else:
					cluster[label] = {}
					cluster[label] = 0
				time.append(label_time_list[int(index)-1]['time'])

			s = sorted(cluster.items(), key = operator.itemgetter(1), reverse = True)
			# print(s)
			cluster = {
				'label':s[0][0],
				'timestamp':time
			}
			if cluster['label'] in dic:
				dic[cluster['label']['timestamp']+cluster['timestamp']]
			else: 
				dic[cluster['label']] = cluster
	
	for topic in dic:
		timestamp = dic[topic]['timestamp']
		timestamp = sorted(timestamp)
		# print('timestamp')
		# print(timestamp)
		t = get_time_period(timestamp)
		dic[topic]['time'] = t[0]
		dic[topic]['end'] = t[1]

	print(dic)
	
	return dic
