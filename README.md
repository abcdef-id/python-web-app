# GGCode Python Web App Project Template


## Installation

Pre requisite:
- Python 3.7
- Python Virtual Environment (we usually use this https://pypi.org/project/virtualenv/)
- MariaDB database
- MongoDB
- Redis

Install Command:
- Create MariaDB database, clone & follow the instruction from https://github.com/abcdef-id/python-mysql-migration.git
- Activate your Python Virtual Environment, if using virtualenv: 
```
<virtualenv_directory>/bin/activate
```
- Install Libraries:
```
pip install -r requirement.txt
```
- create folder logs, run this command from project root:
```
mkdir -p app/resources/logs
```

Uninstall Command:
- Remove libraries: 
```
pip uninstall -r requirement.txt
```

## Run

- change project mysql connection in config.cfg
- python run.py

### Try It
- url: http://127.0.0.1:8899/
- username: admin, password: 123456

## Directory Structure

- app/controllers/ : code location for web controller
- app/libraries/ : code location for global function
- app/models/ : code location for data model
- app/static/ : location for static file
- app/tempates/ : location for html jinja2 file

## Template Files
- app/__init__.py : code to initiate app configuration 
- app/config.py : code to read config.cfg files
- app/routes.py : code to load api controller files & routes
- app/variable_constant.py : code for global constant & variable
- app/models/base_model.py : code for model superclass, contains default models function


## How to write


This project template use [Flask Framework](https://flask.palletsprojects.com) and [Jinja Template](https://palletsprojects.com/p/jinja/)

### Create your Model

#### Create file model in [**app/models/**](https://github.com/abcdef-id/python-web-app/tree/master/app/models) directory. See the model example in [**app/models/user.py**](https://github.com/abcdef-id/python-web-app/blob/master/app/models/user.py)

```
from app.models.base_model import CrudBase

class <model_class_name>(CrudBase):

    __table__ = '<table_name>' # What is the table for this Model
    
    __primary_key__ = 'id' # What is the primary key for this table

    # Define which columns can be added.
    __add_new_fillable__ = [
        '<field_name_1>',
        '<field_name_2>',
        '<field_name_3>',
        'status',
        'created_by'
    ]

    #Define which columns can be updated.
    __update_fillable__ = [
	'<field_name_1>',
        '<field_name_2>',
        '<field_name_3>',
        'status',
	'updated_by'
    ]

    # Define form input validation, Use this in api validation.
    addNewValidation = {
	'<field_name_1>': {'type': 'string', 'required': True, 'empty': False},
	'<field_name_2>': {'type': 'string', 'required': True, 'empty': False},
	'<field_name_3>': {'type': 'string', 'required': True, 'empty': False},
    }

    updateValidation = {
	'<field_name_1>': {'type': 'string', 'required': True, 'empty': False},
	'<field_name_2>': {'type': 'string', 'required': True, 'empty': False},
	'<field_name_3>': {'type': 'string', 'required': True, 'empty': False},
    }
```

We provide **CrudBase** Class for **MySQL** and **CrudBaseMongoDB** Class for MongoDB if it is standard List and CRUD. 

CrudBase Contain methods:

**# getList**, with parameters:
- **args** with value below:
```
{ 
	"rp":<RecordPerPage>, 
	"p":<Page>, 
	"f":{"<query_field_name>":"<field_value"},
	"o":{"<order_field_name>":"<asc_desc>"}
}
```
- **qraw** (optional) if you want to use raw query value, example: ' id=1 and status=1 '

usage in controller:
```
    args = { 
	"rp":25, 
	"p":1, 
	"f":{
	    "field_1":"a",
	    "field_2":"b"
	},
	"o":{
	    "field_1":"asc",
	    "field_2":"desc"
	}
    }
    # Without raw query
    data_list = YourModel.getList(args)
    
    # With raw query
    qraw = ' field_3 like '%abcd% ' 
    data_list = YourModel.getList(args,qraw)
    
```
**# getById**, with parameter:
- **id** <primary_key_value>

usage in controller:
```
    id = 1
    single_data = YourModel.getById(id)
```
**# addNew**
- **args** dictionary data
	
usage in controller:
```
    args = {
        'field_1':'a',
        'field_2':'b',
        'field_3':'c'
    }
    YourModel.addNew(args)
```

**# doUpdate**
- **id** <primary_key_value>
- **args** dictionary data
usage in controller:
```
    id = 1
    args = {
        'field_1':'a',
        'field_2':'b',
        'field_3':'c'
    }
    YourModel.doUpdate(id, args)
```

**# doDelete**
- **id** <primary_key_value>

usage in controller:
```
    id = 1
    YourModel.doDelete(id)
```
**# getAll**
usage in controller:
```
    data_list = YourModel.getAll()
```
**Make your own method**
in your model class:
```
    from app import db
     
    @classmethod
    def <your_method_name>(self, <your_argument>):
        result = db.<your_query_builder>
        # Your Logic
        return result
```
usage in controller:
```
    result = YourModel.<your_method_name>(<your_argument>)
```

Learn orator-orm query builder [here](https://orator-orm.com/docs/0.9/query_builder.html#introduction)

### Create your Controller

#### 1. Create file controller in [**app/controllers/**](https://github.com/abcdef-id/python-web-app/tree/master/app/controllers) directory. See the controller example in [**app/controllers/user.py**](https://github.com/abcdef-id/python-web-app/blob/master/app/controllers/user.py)

```
from app import app
from flask import render_template, request, redirect, url_for, session, flash, json
from app.libraries.util import Util as util, web_permission_checker
from app.models.user import User as UserModel
from app.libraries.validator import MyValidator

class <your_controller_class_name>():
    def __init__(self):

        @app.route('/<your_url_path>', methods=['GET','POST'])
        def <your_controller_method>():
        Your Logic
        return redirect(util.my_url_for(url_for('<your_redirect_controller_method>')))
        or
        return render_template('<your_ui_path>')

```

#### 2. Create ui in [**app/templates/**](https://github.com/abcdef-id/python-web-app/tree/master/app/templates) directory. See the ui example in [**app/templates/user/**](https://github.com/abcdef-id/python-web-app/blob/master/app/templates/user/)

#### 3. Add your controller in [**app/routes.py**](https://github.com/abcdef-id/python-web-app/blob/master/app/routes.py)
```
    from app.controllers.<your_controller_class_file_name> import <your_controller_class_name>
    <your_controller_class_name>()
```
