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

def get_links(stage1_nodes, data1, data2, param):
  print('Stage2_2 start processing...')

  nodes = stage1_nodes
  edges = []
  link_aggr = {}
  link_list = []

  for user in data1:
    if 'nodes' in data1[user] and 'edges' in data1[user]:
      for edge in data1[user]['edges']:
        start = getLabel(data1[user]['nodes'], edge['from'])
        end = getLabel(data1[user]['nodes'], edge['to'])
        if(start==None or end==None):
           continue
        elif(start in link_aggr):
           if(end in link_aggr[start]):
              link_aggr[start][end] = link_aggr[start][end]+1
           else:
              link_aggr[start][end] = 1
        else:
          link_aggr[start]={end: 1}

  for user in data2:
    if 'nodes' in data2[user] and 'edges' in data2[user]:
      for edge in data2[user]['edges']:
        start = getLabel(data2[user]['nodes'], edge['from'])
        end = getLabel(data2[user]['nodes'], edge['to'])
        if(start==None or end==None):
           continue
        elif(start in link_aggr):
           if(end in link_aggr[start]):
              link_aggr[start][end] = link_aggr[start][end]+1
           else:
              link_aggr[start][end] = 1
        else:
          link_aggr[start]={end: 1}

  flag={}
  for start in link_aggr:
    if(findObjectFromList(nodes, 'label', start)==None):
         nodes.append({'id': len(nodes), 'label': start})
    for end in link_aggr[start]:
      if(findObjectFromList(nodes, 'label', end)==None):
         nodes.append({'id': len(nodes), 'label': end})
      if(link_aggr[start][end]>param):
        nfrom=findObjectFromList(nodes, 'label', start)['id']
        nto=findObjectFromList(nodes, 'label', end)['id']
        flag[nfrom]=1
        flag[nto]=1
        link_list.append({
          'from':nfrom,
          'to':nto,
          'width':(link_aggr[start][end]-param)/5 + 1
        })
  
  filtered_nodes=[]
  for n in nodes:
    if(n['id'] in flag):
      filtered_nodes.append(n)
  result = {}
  result['nodes'] = filtered_nodes
  result['edges'] = link_list
  print('Stage2 end processing')
  return result

