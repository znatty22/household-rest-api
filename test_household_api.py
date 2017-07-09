from pprint import pprint
import pytest, json

import household_api

""" The unit tests for household rest api
"""

@pytest.fixture
def client():
    client = household_api.app.test_client()

    yield client

def test_page_not_found(client):
	response = client.get('/')
	status_code = response.status_code
	assert status_code == 404

def test_resource_not_found(client):
	uri = '/id/h1'
	response = client.get(uri)
	status_code = response.status_code
	message = json.loads(response.data)['error']['message']
	expected_message = household_api.response_handler.not_found(request_url=uri)['error']['message']

	assert b'does not exist' in expected_message
	assert status_code == 404

def test_post_missing_inputs(client):
	# Missing both required inputs
	household = {}
	response = client.post('/households',data=json.dumps(household),content_type='application/json')
	status_code = response.status_code
	message = json.loads(response.data)['error']['message']

	assert status_code == 400
	assert b'income' in message
	assert b'members' in message

	# Missing 1 required input
	household = {'income': 100000,
				'members':[]}
	response = client.post('/households',data=json.dumps(household),content_type='application/json')
	status_code = response.status_code
	message = json.loads(response.data)['error']['message']

	assert status_code == 400
	assert b'income' not in message
	assert b'members' in message

def test_post_invalid_inputs(client):
	# Negative income
	household = {'income': -100000,
				'members':[{'age':45,'gender':'female'}]}
	response = client.post('/households',data=json.dumps(household),content_type='application/json')
	status_code = response.status_code
	message = json.loads(response.data)['error']['message']

	assert status_code == 400
	assert b'income' in message
	assert b'greater than or equal to zero' in message

	# Invalid Age
	household = {'income': 100000,
				'members':[{'age':'forty','gender':'female'}]}
	response = client.post('/households',data=json.dumps(household),content_type='application/json')
	status_code = response.status_code
	message = json.loads(response.data)['error']['message']

	assert status_code == 400
	assert b'age' in message
	assert b'not int' in message

def test_post_bad_format(client):
	# Invalid json format
	household = {'income': 100000,
				'members':[{'age':45,'gender':'female'}]}
	json_string = json.dumps(household)	+ '}'		
	response = client.post('/households',data=json_string,content_type='application/json')
	status_code = response.status_code
	message = json.loads(response.data)['error']['message']

	assert status_code == 400
	
def test_post_valid_inputs(client):
	# Valid input
	household = {'income': 100000,
				'members':[{'age':45,'gender':'female'}]}
	response = client.post('/households',data=json.dumps(household),content_type='application/json')
	status_code = response.status_code
	result = json.loads(response.data)['success']

	assert status_code == 200
	assert 1 == len(result)
	assert b'id' in result[0]

def test_get_one(client):
	# Valid input
	household = {'income': 900000,
				'members':[{'age':45,'gender':'female'}]}
	response = client.post('/households',data=json.dumps(household),content_type='application/json')
	result = json.loads(response.data)
	id = result['success'][0]['id']

	uri = '/households/' + id
	response = client.get(uri)
	status_code = response.status_code
	result = json.loads(response.data)['success']

	assert status_code == 200
	assert 1 == len(result)
	assert result[0]['id'] == id

def test_get_fpl(client):
	# Valid input
	household = {'income': 900000,
				'members':[{'age':45,'gender':'female'}]}
	response = client.post('/households',data=json.dumps(household),content_type='application/json')
	result = json.loads(response.data)
	id = result['success'][0]['id']

	uri = '/households/' + id + '/fpl-percentage'
	response = client.get(uri)
	status_code = response.status_code
	result = json.loads(response.data)['success']

	assert status_code == 200
	assert 'fpl_percentage' in result[0]

def test_get_all(client):
	# Valid input
	response = client.get('/households')
	status_code = response.status_code
	result = json.loads(response.data)

	assert status_code == 200
	assert len(result['success']) > 0
