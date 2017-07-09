import datetime
from redis_crud import *
from fpl import *

MAIN_COLLECTION = 'Household'

class HouseholdCrudApi(RedisCrudApi):
	"""A CRUD API for household objects in the redis data store.
	Currently provides methods to create, find one, and find all
	household objects in the data store.

    Attributes:
        n/a
    """
	def __init__(self,models=[MAIN_COLLECTION]):
		""" Constructor

		Args:
			models: a list of strings containing names of collections 
			in the data store. The default is a single redis hash with 
			a key that matches the name of the Household model class.

		"""
		RedisCrudApi.__init__(self,models)

	def create(self,object_json):
		""" Creates a household resource in the household data store.

			Args:
				object_json: the json formatted payload describing
				the household object to be created

			Returns:
				A dict containing the result of the create operation
		"""
		return RedisCrudApi.create(self,MAIN_COLLECTION,object_json)

	def find_one(self,object_id):
		""" Finds a household resource in the household data store by object_id.

			Args:
				object_id: the unique id of the household object

			Returns:
				A dict containing the result of the find_one operation
		"""
		return RedisCrudApi.find_one(self,MAIN_COLLECTION,object_id)

	def find_all(self):
		""" Finds all household resources in the household data store 

			Args:
				id: the unique id of the household object

			Returns:
				A dict containing the result of the find_one operation
		"""
		return RedisCrudApi.find_all(self,MAIN_COLLECTION)
	
	def get_fpl_percentage(self,object_id):
		""" Get the federal percentage level of a household

			Args:
				object_id: the unique id of the household object

			Returns:
				A dict containing the result of the fpl_percentage operation
		"""

		# Get household object
		result = self.find_one(object_id)
		
		# Household found, get federal poverty level percentage
		if result['success']:
			household = result['success'][0]
			year = datetime.datetime.now().year
			income = household['income']
			household_size = len(household['members'])
			
			fpl_percentage = self._caluclate_fpl_percentage(income,household_size)

			result = self.response_handler.success([{'fpl_percentage': fpl_percentage,
												'income': income,
												'household_size': household_size,
												'year': year }])
			
		return result

	def _caluclate_fpl_percentage(self,income, household_size):
		""" Calculate the federal percentage level of a household
		
			FPL is based on household income, # of members in the household. 
			Currently returns FPL for year 2017. FPL is calculated by:

				household.income / FPL
				FPL = Lookup based on household size

			Args:
				income: the total annual income of the household
				household_size: the a count of all members in the household 

			Returns:
				A float representing the fpl percentage
		"""
		# Only supports year 2017
		year = 2017
		fpl_table = fpl_db[year]

		# Get the federal povery level
		if household_size <= 8:
			fpl = fpl_table[household_size]
		else:
			fpl = household_size * fpl_table[0]

		# Calculate the fpl percentage	
		fpl_percentage = income/fpl

		return fpl_percentage	