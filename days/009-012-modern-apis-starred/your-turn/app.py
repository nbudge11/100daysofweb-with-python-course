import json
from typing import List

from apistar import App, Route, types, validators
from apistar.http import JSONResponse


def _load_application_data():
    with open('MOCK_DATA.json') as f:
        applications = json.loads(f.read())
        return {application["id"]: application for application in applications}


applications = _load_application_data()

VALID_COMPANIES = set([application["company_name"] for application in applications.values()])
APP_NOT_FOUND = 'Application not found'


class Application(types.Type):
    id = validators.Integer(allow_null=True)  # assign in POST
    app_name = validators.String(max_length=100)
    app_version = validators.String(max_length=100)
    logo = validators.String(max_length=100)
    company_name = validators.String(enum=list(VALID_COMPANIES))


def list_applications() -> List[Application]:
    return [Application(application[1]) for application in sorted(applications.items())]


def create_application(application: Application) -> JSONResponse:
    application_id = len(applications) + 1
    application.id = application_id
    applications[application_id] = application
    return JSONResponse(Application(application), status_code=201)


def get_application(application_id: int) -> JSONResponse:
    application = applications.get(application_id)

    if not application:
        error = {'error': APP_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    return JSONResponse(Application(application), status_code=200)


def update_application(application_id: int, application: Application) -> JSONResponse:
    if not applications.get(application_id):
        error = {'error': APP_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    application.id = application_id
    applications[application_id] = application
    return JSONResponse(Application(application), status_code=200)


def delete_application(application_id: int) -> JSONResponse:
    if not applications.get(application_id):
        error = {'error': APP_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    del applications[application_id]
    return JSONResponse({}, status_code=204)


routes = [
    Route('/', method='GET', handler=list_applications),
    Route('/', method='POST', handler=create_application),
    Route('/{application_id}/', method='GET', handler=get_application),
    Route('/{application_id}/', method='PUT', handler=update_application),
    Route('/{application_id}/', method='DELETE', handler=delete_application),
]

app = App(routes=routes)

if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)
