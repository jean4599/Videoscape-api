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
	data = firebase.get('/'+course+'/STAGE2/_user_saved_graphs', None)
	result = get_links(data)
	firebase.put('/'+course+'/STAGE2/', '_server_result', result)
	return 'Stage2 process finished!\n'
	

@app.route('/videoscape/api/<string:course>/process/stage1', methods=['GET'])
def stage1(course):
	data = firebase.get('/'+course+'/STAGE1/_user_saved_concepts', None)
	result = get_cluster(data)
	firebase.put('/'+course+'/STAGE1/', '_server_result', result)
	return 'Stage1 process finished!\n'

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()