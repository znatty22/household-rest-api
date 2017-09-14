# About
This repository was created just for fun to experiment with flask, redis, and docker. It contains a rest api for household resources. You can get a listing of household, a particular household by id and the federal poverty level percentage for a household.

# Household Resource REST API Documentation
This api doc provides documentation on how to create and retrieve household resources via the company household rest api. The api currently does not support all CRUD (create, read, update, delete) operations. Only create and read have been implemented thus far.

## For All Endpoints
All resource URIs will be relative to the base URL:

```
http://<ip address>:<port>/
```
### Requests
All `POST` requests must have `content-type` set to `application/json`

### Responses
All responses with a body will have a json payload with `content-type` set to `application/json`

### Errors
* 500 internal server error
* 405 method not allowed

## Create a household 
This endpoint is used to create a single household resource.

### Example Request
```
http://<ip address>:<port>/household/787bcb8d-75df-4b06-a8ff-2b227e30e13c
```
`Content-Type`: `application/json`
```
{
    "income":100000,
    "members":[
        {"age": 36, "gender":"male"},
        {"age": 30, "gender":"male"}
    ]
}
```

### Example Success Response
```
{
    "error": {},
    "success": [
        {
            "id": "787bcb8d-75df-4b06-a8ff-2b227e30e13c"
        }
    ]
}
```
### Example Error Response
```
{
    "error": {
        "code": 400,
        "message": "{'income': ConversionError([ErrorMessage(u'This field is required.', None)])}"
    },
    "success": null
}
```
### Endpoint URL
`<base URL>/households`

### Method
`POST`

### Required
Household
* `income` - a float greater than or equal to zero
* `members` - a list with at least 1 element

Element of `members` must have:
* `age` - a positive integer
* `gender` - a string with value either `female` or `male`

### Errors
* 404 route not found
* 400 bad client request

## Get One household 
This endpoint is used to retrieve a single household resource given the household id.

### Example Request
```
http://<ip address>:<port>/household/787bcb8d-75df-4b06-a8ff-2b227e30e13c
```

### Example Success Response
```
{
    "error": {},
    "success": [
        {
            "id": "b1620fab-a9aa-41b3-af02-82d793188db7",
            "income": 10000,
            "members": [
                {
                    "age": 36,
                    "gender": "male"
                },
                {
                    "age": 30,
                    "gender": "male"
                }
            ]
        }
    ]
}
```
### Example Error Response
```
{
    "error": {
        "code": 404,
        "message": "Household with id b1620fab-a9aa-41b3-af02-82d793188db was not found"
    },
    "success": null
}
```
### Endpoint URL
`<base URL>/households/<household id>`

### Method
`GET`

### Required
* `household_id` - a standard uuid or alphanumeric string

### Errors
* 404 resource not found
* 404 route not found
* 400 bad client request


## Get All households
This endpoint is used to retrieve all household resources.

### Example Request
```
http://<ip address>:<port>/households
```

### Example Success Response
```
{
    "error": {},
    "success": [
        {
            "id": "b1620fab-a9aa-41b3-af02-82d793188db7",
            "income": 10000,
            "members": [
                {
                    "age": 36,
                    "gender": "male"
                },
                {
                    "age": 30,
                    "gender": "male"
                }
            ]
        },
        {
            "id": "787bcb8d-75df-4b06-a8ff-2b227e30e13c",
            "income": 100000,
            "members": [
                {
                    "age": 36,
                    "gender": "male"
                },
                {
                    "age": 30,
                    "gender": "male"
                }
            ]
        }
    ]
}
```
### Example Error Response
```
{
    "error": {
        "code": 404,
        "message": "Sorry this route http://localhost:5000/householdsm does not exist. Check for spelling errors"
    },
    "success": null
}
```
### Endpoint URL
`<base URL>/households`

### Method
`GET`

### Required
* N/A

### Errors
* 404 route not found


## Get Household Federal Poverty Level Percentage  
This endpoint is used to retrieve the federal poverty level percentage for a household given the household id.

### Example Request
```
http://<ip address>:<port>/household/787bcb8d-75df-4b06-a8ff-2b227e30e13c/fpl-percentage
```

### Example Success Response
```
{
    "error": {},
    "success": [
        {
            "fpl_percentage": 6.157635467980295,
            "household_size": 2,
            "income": 100000,
            "year": 2017
        }
    ]
}
```
### Example Error Response
```
{
    "error": {
        "code": 404,
        "message": "Household with id b1620fab-a9aa-41b3-af02-82d793188db was not found"
    },
    "success": null
}
```
### Endpoint URL
`<base URL>/households/<household id>/fpl-percentage`

### Method
`GET`

### Required
* `household_id` - a standard uuid or alphanumeric string

### Errors
* 404 resource not found
* 404 route not found
* 400 bad client request

