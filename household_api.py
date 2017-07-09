from flask import Flask, request, jsonify
from pprint import pprint
from household_crud import *
from handlers import *

""" The rest api for households
"""

app = Flask(__name__)
household_crud = HouseholdCrudApi()
response_handler = ResponseHandler()

@app.route('/households', methods=['POST'])
def post_household():
    """ Creates a new household 
    """

    # Check mime-type
    if not request.is_json:
        message = 'Mimetype must me %s not %s' % ('application/json',request.mimetype) 
        result  = response_handler.bad_request(message=message)
        return jsonify(result),400 

    result = household_crud.create(request.json)

    if result['success']:
        response = jsonify(result), 200
    else:
        response = jsonify(result), result['error']['code']

    return response

@app.route('/households/<string:household_id>', methods=['GET'])
def get_household(household_id):
    """ Retrieves a household by household id 
    """
    result = household_crud.find_one(household_id)

    if result['success']:
        response = jsonify(result), 200
    else:
        response = jsonify(result), result['error']['code']

    return response

@app.route('/households/', methods=['GET'])
@app.route('/households', methods=['GET'])
def get_households():
    """ Retrieves all households
    """
    result = household_crud.find_all()
    if not result['error']:
        response = jsonify(result), 200
    else:
        response = jsonify(result), result['error']['code']
        
    return response

@app.route('/households/<string:household_id>/fpl-percentage', methods=['GET'])
def get_fpl_percentage(household_id):
    """ Retrieves a household's federal poverty level percentage by household id 
    """
    result = household_crud.get_fpl_percentage(household_id)

    if result['success']:
        response = jsonify(result), 200
    else:
        response = jsonify(result), result['error']['code']

    return response

@app.errorhandler(405)
def method_not_allowed(e):
    """ Catch method not allowed requests
    """
    result  = response_handler.method_not_allowed(message=str(e))
    return jsonify(result),405

@app.errorhandler(500)
def server_error(e):
    """ Catch generic bad client requests 
    """
    result  = response_handler.server_error(message=str(e))
    return jsonify(result),500

@app.errorhandler(400)
def bad_request(e):
    """ Catch generic bad client requests 
    """
    result  = response_handler.bad_request(message=str(e))
    return jsonify(result),400

@app.errorhandler(404)
def page_not_found(e):
    """ Catch generic route not found errors
    """
    result  = response_handler.not_found(request_url=request.url)
    return jsonify(result),404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
