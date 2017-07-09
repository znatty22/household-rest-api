
import os, json, redis
from pprint import pprint
from handlers import ResponseHandler


REDIS_HOST = os.environ.get('DB_PORT_6379_TCP_ADDR')

class RedisCrudApi(object):
	"""A CRUD API for objects in the redis data store.
	Currently provides methods to create, find one, and find all
	objects in a particular collection inside the data store.

	The datastore could store collections for multiple object
	types.

    Attributes:
        db: connection to redis database
        response_handler: helper for formatting results
        models: a list of object class names pertaining
        to object collections in redis data store
    """

	def __init__(self,models):
		""" Constructor

		Stores the connection to the redis data store
		Stores a reference to the response handler
		Dynamically imports the model classes for this data store.
		Each model class will have its own collection in the data store

		Args:
			models: a list of strings containing names of collections 
			in the data store. Each string must match the name of the 
			model class. 
		"""

		# Get connection to redis data store
		self.db = self.get_redis_connection()
		self.response_handler = ResponseHandler()
		# Dynamic import of model classes for this redis data store
		self.models = {}
		for model_name in models:
			module = __import__('models')
			model_class = getattr(module, model_name)
			self.models[model_name] = model_class

	def get_redis_connection(self):
		""" Create and return reference to redis data store """
		return redis.StrictRedis(host=REDIS_HOST)	

	def create(self,object_name,object_json):
		""" Creates a object in the object's collection within data store.

			Args:
				object_name: the name of the collection in the data store


			Returns:
				A dict containing the result of the create operation
		"""
		# Get class for <object_name>
		object_model_class = self.models[object_name]
		
		# Validate object json
		try:
			object_model = object_model_class(object_json)
			object_model.validate()
		
		# Validation failed, return the error message
		except Exception as e:
			return self.response_handler.bad_request(str(e.messages))
		
		# Convert json to string
		json_string = json.dumps(object_model.to_primitive())

		# Store in redis in a collection called <object_name>
		self.db.hset(object_name,object_model.id,json_string)
		
		return self.response_handler.success([{'id':object_model.id}])

	def find_one(self,object_name,id):
		""" Finds an object in the object's collection within data storeb by id.

			Args:
				object_name: the name of the collection in the data store
				id: a unique identifier of the object

			Returns:
				A dict containing the result of the find_one operation
		"""

		results_dict = {}
		# Get object string from redis data store
		json_string = self.db.hget(object_name, id)
	
		# Object exists
		if json_string:
			# Convert string to dict
			results_dict = json.loads(json_string)
			return self.response_handler.success([results_dict])
		# Object does not exist
		else:
			message = '%s with id %s was not found' % (object_name, id)
			return self.response_handler.not_found(message) 

	def find_all(self, object_name):
		""" Finds all object in the object's collection within data store.

			Args:
				object_name: the name of the collection in the data store

			Returns:
				A dict containing the result of the find_all operation
		"""

		# Get object from redis data store
		results_dict = self.db.hgetall(object_name)
		
		# Convert object json strings to dict
		results = []
		for id in results_dict:
			results.append(json.loads(results_dict[id]))

		return self.response_handler.success(results)

