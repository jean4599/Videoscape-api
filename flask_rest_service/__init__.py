from flask import Flask
from flask_cors import CORS
from stage1 import get_cluster
from stage2 import get_links
from firebase import firebase

app = Flask(__name__)
cors = CORS(app, resources={r"/videoscape/api/*": {"origins": "*"}})
firebase = firebase.FirebaseApplication('https://videoscape-b857c.firebaseio.com', None)

@app.route('/videoscape/api/<string:course>/process/stage2', methods=['GET'])
def stage2(course):
	stage1_nodes = firebase.get('/_courses/'+course+'/STAGE1/_user_saved_concepts', None)
	data = firebase.get('/_courses/'+course+'/STAGE2/_user_saved_graphs', None)
	result = get_links(stage1_nodes, data)
	firebase.put('/_courses/'+course+'/STAGE2/', '_server_result', result)
	return 'Stage2 process finished!\n'
	

@app.route('/videoscape/api/<string:course>/process/stage1', methods=['GET'])
def stage1(course):
	print('Stage1 process start...')
	data = firebase.get('/_courses/'+course+'/STAGE1/_user_saved_concepts', None)
	if data==None:
		print('No data in firebase. Stage 1 end.')
		return 'No data in firebase. Stage 1 end.'
	elif(len(data.keys())<5):
		print('Data not sufficient. Stage 1 end')
		return 'Data not sufficient. Stage 1 end';

	result = get_cluster(data)
	aggregate_result = result[0]
	stage_finished = result[1]
	print(aggregate_result)
	firebase.put('/_courses/'+course+'/STAGE1/', '_server_result', aggregate_result)
	if stage_finished:
		firebase.put('/_courses/'+course,'/stage', 2)
	
	print('Stage1 process end!')
	return 'Stage1 process finished!\n'

@app.route('/')
def hello_world():
    return 'Hello World!'
