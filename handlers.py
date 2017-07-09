
class ResponseHandler(object):
	"""Formats api responses using standard format.

    Attributes:
        n/a
    """

	def __init__(self):
		pass	
	
	def not_found(self,message=None,request_url=None):
		""" A resource or page not found response

		Args:
			message: a string describing the details of the error
			request_url: a string containing the url of the original request

		Returns:
			A dict in a the standard success or error format.
			Contains the error message and includes the status code for convenience
		"""
		status_code = 404
		if not request_url:
			request_url = ''
		if not message:
			message = 'Sorry this route %s does not exist. Check for spelling errors' % request_url
		
		return self.error(message,status_code)

	def bad_request(self,message=None):
		""" A client bad request response

		Args:
			message: a string message describing the details of the error

		Returns:
			A dict in a the standard success or error format.
			Contains the error message and includes the status code for convenience
		"""
		status_code = 400
		if not message:
			message = 'Client made an invalid request'

		return self.error(message,status_code)

	def method_not_allowed(self,message=None):
		""" A http method that is not allowed was in request

		Args:
			message: a string message describing the details of the error

		Returns:
			A dict in a the standard success or error format.
			Contains the error message and includes the status code for convenience
		"""
		status_code = 405
		if not message:
			message = 'Client made a request with an HTTP method that is not supported at this endpoint'

		return self.error(message,status_code)

	def server_error(self,message=None):
		""" An internal server error occurred

		Args:
			message: a string message describing the details of the error

		Returns:
			A dict in a the standard success or error format.
			Contains the error message and includes the status code for convenience
		"""
		status_code = 500
		if not message:
			message = 'Internal server error'

		return self.error(message,status_code)

	def success(self,result):
		""" A success response

		Attributes:
			message: a string message describing the details of the error
			request_url: a string containing the url of the original request

		Returns:
			A dict in a the standard success format.
			Contains the result data in 'success'
		"""
		return {'success': result,
				'error': {}
				}

	def error(self,message,status_code):
		""" An error response

		Attributes:
			message: a string message describing the details of the error
			status_code: a standard http status code

		Returns:
			A dict in a the standard error format.
			Contains the error message and includes the status code for convenience
		"""
		return {'success': None,
				'error': {'message':message,'code':status_code} 
				}

    