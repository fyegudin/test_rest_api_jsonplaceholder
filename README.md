# Python Test the REST API: https://jsonplaceholder.typicode.com/

## Prerequisite

Other than the **Open Project** site, you should have the following installed:

* Python 3.10 and up
* Pipenv
* Pytest

Create venv and install all dependencies by use requirements.txt:

```
> python -m venv venv
> source venv/bin/activate # On Windows, use venv\Scripts\activate
> pip freeze > requirements.txt
> pip install -r requirements.txt
```


## Running the project

You can run the tests using your favourite IDE or from the command line. For example:

```
> pytest -s -v tests_api
```

## View the Allure Report

You can view the allure test report:

```
> allure serve .\Report\
```
