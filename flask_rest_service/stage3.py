import requests
import json
import operator
import urllib
import numpy as np
import math

def getLabel(list, id):
   for obj in list:
      if obj['id']==id:
         return obj['label']
      
def findObjectFromList(list, attr, value):
   for obj in list:
      if obj[attr]==value:
         return obj

def aggregate_label(labels):
  if(type(labels)!=list):
    return []
  dic={}
  for label in labels:
    if(label in dic):
      dic[label]+=1
    else:
      dic[label]=1
  s = sorted(dic.items(), key = operator.itemgetter(1), reverse = True)
  return s

def get_links(stage1_nodes, data, put_label):
  print('Stage3 start processing...')

  nodes = stage1_nodes
  edges = []
  link_list = []
  link_aggr={}

  for user in data:
    if 'nodes' in data[user] and 'edges' in data[user]:
      for edge in data[user]['edges']:
        start = getLabel(data[user]['nodes'], edge['from'])
        end = getLabel(data[user]['nodes'], edge['to'])
        if(start==None or end==None):
           continue
        elif(start in link_aggr):
           if(end in link_aggr[start]):
              link_aggr[start][end]['num'] += 1
              link_aggr[start][end]['label'].append(edge['label'])
           else:
              link_aggr[start][end] = {'num':1, 'label':[edge['label']]}
        else:
          link_aggr[start]={end: {'num':1, 'label':[edge['label']]} }

  flag={}
  for start in link_aggr:
    if(findObjectFromList(nodes, 'label', start)==None):
         nodes.append({'id': len(nodes), 'label': start})
    for end in link_aggr[start]:
      if(findObjectFromList(nodes, 'label', end)==None):
         nodes.append({'id': len(nodes), 'label': end})
      if(link_aggr[start][end]['num']>1):
        nfrom=findObjectFromList(nodes, 'label', start)['id']
        nto=findObjectFromList(nodes, 'label', end)['id']
        flag[nfrom]=1
        flag[nto]=1

        link_aggr[start][end]['label'] = aggregate_label(link_aggr[start][end]['label'])
        if(put_label):
          link_list.append({
            'from':nfrom,
            'to':nto,
            'width':link_aggr[start][end]['num']-2,
            'labels':link_aggr[start][end]['label'],
            'label':link_aggr[start][end]['label'][0][0]
          })
        else:
          link_list.append({
            'from':nfrom,
            'to':nto,
            'width':link_aggr[start][end]['num']-2,
            'labels':link_aggr[start][end]['label']
          })
  
  filtered_nodes=[]
  for n in nodes:
    if(n['id'] in flag):
      filtered_nodes.append(n)
  result = {}
  result['nodes'] = filtered_nodes
  result['edges'] = link_list
  print('Stage3 end processing')
  return result

