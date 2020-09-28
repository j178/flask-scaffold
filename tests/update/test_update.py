
from flask.testing import FlaskClient
def test_get_update(client):
    args = {
        'app_name': '',
        'lang': 'zh-CN'
    }
    resp = client.get("/update/", args=args)

    assert resp.status_code == 200
