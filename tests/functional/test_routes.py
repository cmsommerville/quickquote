from app import create_app
from config import CONFIG

config = CONFIG.get("TEST")
flask_app = create_app(config)


def test_home_page():
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b"Hello World!" in response.data


def test_create_tables():
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/admin/create-tables')
        assert response.status_code == 200


def test_group_save_to_db(new_group_data1):
    with flask_app.test_client() as test_client:
        # recreate tables
        test_client.get('/admin/create-tables')

        # create a group record
        post_group_response = test_client.post(
            '/workflow/group', json=new_group_data1)

        # get the group_id from the response
        group_id = post_group_response.get_json()['group_id']

        # GET request to get the all the group data for the group ID
        get_group_response = test_client.get(
            f'/workflow/group?group_id={group_id}')

        # extract group selections
        selections = get_group_response.get_json()['selections']
        assert selections['group_id'] == group_id
        assert selections['group_size'] == 2400
        assert get_group_response.status_code == 200


def test_plan_save_to_db(new_plan_data1, new_group_data1):
    with flask_app.test_client() as test_client:
        # recreate tables
        test_client.get('/admin/create-tables')

        # generate group record
        post_group_response = test_client.post(
            '/workflow/group', json=new_group_data1)
        # get group id
        group_id = post_group_response.get_json()['group_id']

        # generate plan record
        post_plan_response = test_client.post(
            '/workflow/plan', json={**new_plan_data1, "group_id": group_id})

        # get plan id
        plan_id = post_plan_response.get_json()['plan_id']

        # GET request to get plan data from database
        get_plan_response = test_client.get(
            f'/workflow/plan?plan_id={plan_id}')

        # extract the plan selections
        selections = get_plan_response.get_json()['selections']
        assert selections['plan_id'] == plan_id
        assert selections['product_name'] == 'Accident'
        assert get_plan_response.status_code == 200
        assert post_plan_response.status_code == 201
