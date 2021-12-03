# How to run it
You need pipenv installed and then you do

	pipenv install
	pipenv shell
	flask run

You must have the `.env` file configured

# .env

	FLASK_APP=main
	FLASK_ENV=development

	DB_USER=<user>
	DB_PWD=<password>
	DB_HOST=<mongo server URL>
	DB_NAME=<database name>

# Create an Inquiry

	POST http://127.0.0.1:5000/api/inquiries
	{
	    "name": "John Smith",
	    "email": "example@google.com",
	    "phone_number": "1309513058",
	    "company_name": "Skan AI",
	    "job_title": "Dev",
	    "location": "India"
	}

	RESPONSE
	{
	  "_cls": "Inquiry",
	  "_id": {
	    "$oid": "61aa31b6487f58c452302f81"
	  },
	  "company_name": "Skan AI",
	  "email": "example@google.com",
	  "job_title": "Dev",
	  "location": "India",
	  "name": "John Smith",
	  "phone_number": "1309513058"
	}

# Retrieve Inquiries

	GET http://127.0.0.1:5000/api/inquiries

	RESPONSE
	[
	  {
	    "_cls": "Inquiry",
	    "_id": {
	      "$oid": "61aa3127487f58c452302f80"
	    },
	    "company_name": "Skan AI",
	    "email": "example@google.com",
	    "job_title": "Dev",
	    "location": "India",
	    "name": "John Smith",
	    "phone_number": "1309513058"
	  },
	  {
	    "_cls": "Inquiry",
	    "_id": {
	      "$oid": "61aa31b6487f58c452302f81"
	    },
	    "company_name": "Skan AI",
	    "email": "example@google.com",
	    "job_title": "Dev",
	    "location": "India",
	    "name": "John Smith",
	    "phone_number": "1309513058"
	  }
	]	
