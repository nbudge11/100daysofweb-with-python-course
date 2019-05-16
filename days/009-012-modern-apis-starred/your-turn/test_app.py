from apistar import test

from app import app, applications, APP_NOT_FOUND

client = test.TestClient(app)


def test_list_applications():
    response = client.get('/')
    assert response.status_code == 200

    json_resp = response.json()
    assert len(json_resp) == 1000

    expected = {
        "id": 1,
        "app_name": "Fintone",
        "app_version": "8.4",
        "logo": "nisl.jpeg",
        "company_name": "Littel-Collier"
    }
    assert json_resp[0] == expected


def test_create_application():
    data = {
        "app_name": "Wootwa",
        "app_version": "1.0.1",
        "logo": "noce.png",
        "company_name": "Littel-Collier"
    }

    response = client.post('/', data=data)
    assert response.status_code == 201
    assert len(applications) == 1001

    response = client.get('/1001/')
    expected = {
        "id": 1001,
        "app_name": "Wootwa",
        "app_version": "1.0.1",
        "logo": "noce.png",
        "company_name": "Littel-Collier"
    }
    assert response.json() == expected


def test_create_application_missing_fields():
    data = {"key":1}
    response = client.post('/', data=data)
    assert response.status_code == 400

    errors = response.json()
    assert errors['app_name'] == 'The "app_name" field is required.'
    assert errors['app_version'] == 'The "app_version" field is required.'
    assert errors['logo'] == 'The "logo" field is required.'
    assert errors['company_name'] == 'The "company_name" field is required.'


def test_create_car_field_validation():
    data = {
        "app_name": "Wootwa",
        "app_version": "1.0.1",
        "logo": "noce.png",
        "company_name": "Google"
    }
    response = client.post('/', data=data)
    assert response.status_code == 400

    errors = response.json()
    assert "Must be one of" in errors['company_name']


def test_get_application():
    response = client.get('/777/')
    assert response.status_code == 200

    expected = {
        "id": 777,
        "app_name": "It",
        "app_version": "0.9.7",
        "logo": "dictumst.gif",
        "company_name": "Donnelly, Hintz and Kuhn"
    }
    assert response.json() == expected


def test_get_application_not_found():
    response = client.get('/1111111/')
    assert response.status_code == 404
    assert response.json() == {'error': APP_NOT_FOUND}


def test_update_application():
    data = {
        "app_name": "Wootwa",
        "app_version": "1.0.1",
        "logo": "noce.png",
        "company_name": "Littel-Collier"
    }
    response = client.put('/777/', data=data)
    assert response.status_code == 200

    expected = {
        "id": 777,
        "app_name": "Wootwa",
        "app_version": "1.0.1",
        "logo": "noce.png",
        "company_name": "Littel-Collier"
    }
    assert response.json() == expected

    response = client.get('/777/')
    assert response.json() == expected


def test_update_application_not_found():
    data = {
        "app_name": "Wootwa",
        "app_version": "1.0.1",
        "logo": "noce.png",
        "company_name": "Littel-Collier"
    }
    response = client.put('/1111111/', data=data)

    assert response.status_code == 404
    assert response.json() == {'error': APP_NOT_FOUND}


def test_update_application_validation():
    data = {
        "app_name": "Wootwa",
        "app_version": "1.0.1",
        "logo": "noce.png",
        "company_name": "Google"
    }
    response = client.put('/777/', data=data)
    assert response.status_code == 400

    errors = response.json()
    assert "Must be one of" in errors['company_name']


def test_delete_application():
    application_count = len(applications)

    for i in (11, 22, 33):
        response = client.delete(f'/{i}/')
        assert response.status_code == 204

        response = client.get(f'/{i}/')
        assert response.status_code == 404

    assert len(applications) == application_count - 3

