from flask import Flask
from flask_cors import CORS
from stage1 import get_cluster
from stage2_1 import get_links as stage2_1_getlinks
from stage2_2 import get_links as stage2_2_getlinks
from stage3 import get_links as stage3_1_getlinks
from firebase import firebase

app = Flask(__name__)
cors = CORS(app, resources={r"/videoscape/api/*": {"origins": "*"}})
firebase = firebase.FirebaseApplication('https://beta-videoscape.firebaseio.com/', None)

@app.route('/videoscape/api/<string:course>/process/stage3/3_1', methods=['GET'])
def stage3_1(course):
	stage1_nodes = firebase.get('/_courses/'+course+'/STAGE1_3'+'/_server_result', None)
	data = firebase.get('/_courses/'+course+'/STAGE3_1'+'/_user_saved_graphs', None)
	if len(data.keys())<1:
		print('stage3_1 not enough data')

	else:
		result = stage3_1_getlinks(stage1_nodes, data)
		firebase.put('/_courses/'+course+'/STAGE3_1', '_server_result', result)
		firebase.put('/_courses/'+course,'/stage', '3_2')
	return 'Stage3_1 process finished!\n'

@app.route('/videoscape/api/<string:course>/process/stage2/2_3', methods=['GET'])
def stage2_3(course):
	stage1_nodes = firebase.get('/_courses/'+course+'/STAGE1_3'+'/_server_result', None)
	data1 = firebase.get('/_courses/'+course+'/STAGE2_2'+'/_user_saved_graphs', None)
	data2 = firebase.get('/_courses/'+course+'/STAGE2_3'+'/_user_saved_graphs', None)
	if len(data2.keys())<5:
		print('stage2_3 not enough data')

	else:
		result = stage2_2_getlinks(stage1_nodes, data1, data2, 3)
		firebase.put('/_courses/'+course+'/STAGE2_3', '_server_result', result)
		firebase.put('/_courses/'+course,'/stage', '3_1')
	return 'Stage2_3 process finished!\n'

@app.route('/videoscape/api/<string:course>/process/stage2/2_2', methods=['GET'])
def stage2_2(course):
	stage1_nodes = firebase.get('/_courses/'+course+'/STAGE1_3'+'/_server_result', None)
	data1 = firebase.get('/_courses/'+course+'/STAGE2_1'+'/_user_saved_graphs', None)
	data2 = firebase.get('/_courses/'+course+'/STAGE2_2'+'/_user_saved_graphs', None)
	if len(data2.keys())<5:
		print('stage2_2 not enough data')

	else:
		result = stage2_2_getlinks(stage1_nodes, data1, data2, 2)
		firebase.put('/_courses/'+course+'/STAGE2_2', '_server_result', result)
		firebase.put('/_courses/'+course,'/stage', '2_3')
	return 'Stage2_2 process finished!\n'

@app.route('/videoscape/api/<string:course>/process/stage2/2_1', methods=['GET'])
def stage2_1(course):
	stage1_nodes = firebase.get('/_courses/'+course+'/STAGE1_3'+'/_server_result', None)
	data = firebase.get('/_courses/'+course+'/STAGE2_1'+'/_user_saved_graphs', None)
	
	if len(data.keys())<10:
		print('stage2_1 not enough data')
	else:
		result = stage2_1_getlinks(stage1_nodes, data)
		firebase.put('/_courses/'+course+'/STAGE2_1', '_server_result', result)
		firebase.put('/_courses/'+course,'/stage', '2_2')
	return 'Stage2_1 process finished!\n'
	

@app.route('/videoscape/api/<string:course>/process/stage1/1_1', methods=['GET'])
def stage1_1(course):
	print('Stage1_1 process start...')
	data = firebase.get('/_courses/'+course+'/STAGE1_1'+'/_user_saved_concepts', None)
	if data==None:
		print('No data in firebase. Stage 1 end.')
		return 'No data in firebase. Stage 1 end.'
	elif(len(data.keys())<9):
		print('Data not sufficient. Stage 1 end')
		return 'Data not sufficient. Stage 1 end';

	result = get_cluster(data, 2)
	aggregate_result = result
	print(aggregate_result)
	firebase.put('/_courses/'+course+'/STAGE1_1', '_server_result', aggregate_result)
	if len(data.keys())>9:
		firebase.put('/_courses/'+course,'/stage', '1_2')
	
	print('Stage1_1 process end!')
	return 'Stage1_1 process finished!\n'

@app.route('/videoscape/api/<string:course>/process/stage1/1_2', methods=['GET'])
def stage1_2(course):
	print('Stage1_2 process start...')
	data = firebase.get('/_courses/'+course+'/STAGE1_2'+'/_user_saved_concepts', None)
	if data==None:
		print('No data in firebase. Stage 1 end.')
		return 'No data in firebase. Stage 1 end.'

	result = get_cluster(data, 2)
	aggregate_result = result
	print(aggregate_result)
	firebase.put('/_courses/'+course+'/STAGE1_2', '_server_result', aggregate_result)
	if len(data.keys())>5:
		firebase.put('/_courses/'+course,'/stage', '1_3')
	
	print('Stage1_2 process end!')
	return 'Stage1_2 process finished!\n'

@app.route('/videoscape/api/<string:course>/process/stage1/1_3', methods=['GET'])
def stage1_3(course):
	print('Stage1_2 process start...')
	data = firebase.get('/_courses/'+course+'/STAGE1_3'+'/_user_saved_concepts', None)
	if data==None:
		print('No data in firebase. Stage 1 end.')
		return 'No data in firebase. Stage 1 end.'

	result = get_cluster(data, 1)
	aggregate_result = result
	print(aggregate_result)
	firebase.put('/_courses/'+course+'/STAGE1_3', '_server_result', aggregate_result)
	if len(data.keys())>5:
		firebase.put('/_courses/'+course,'/stage', '2_1')
	
	print('Stage1_3 process end!')
	return 'Stage1_3 process finished!\n'

@app.route('/')
def hello_world():
    return 'Hello World!'
