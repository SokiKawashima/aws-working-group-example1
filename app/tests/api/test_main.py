from unittest.mock import patch

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_check_health():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!!"}


def test_get_fibonacci():
    response = client.get("/fib?n=2")
    assert response.status_code == 200
    assert response.json() == {"result": 1}

    response = client.get("/fib?n=3")
    assert response.status_code == 200
    assert response.json() == {"result": 2}

    response = client.get("/fib?n=4.0")
    assert response.status_code == 200
    assert response.json() == {"result": 3}

    response = client.get("/fib?n=1000")
    assert response.status_code == 200
    assert response.json() == {
        "result": 43466557686937456435688527675040625802564660517371780402481729089536555417949051890403879840079255169295922593080322634775209689623239873322471161642996440906533187938298969649928516003704476137795166849228875
    }

    response = client.get("/fib?n=ひゃく")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["query", "n"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "ひゃく",
            }
        ]
    }

    response = client.get("/fib?n=-1")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than",
                "loc": ["query", "n"],
                "msg": "Input should be greater than 0",
                "input": "-1",
                "ctx": {"gt": 0},
            }
        ]
    }

    response = client.get("/fib?n=0")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than",
                "loc": ["query", "n"],
                "msg": "Input should be greater than 0",
                "input": "0",
                "ctx": {"gt": 0},
            }
        ]
    }

    response = client.get("/fib?n=30000001")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "less_than_equal",
                "loc": ["query", "n"],
                "msg": "Input should be less than or equal to 30000000",
                "input": "30000001",
                "ctx": {"le": 30000000},
            }
        ]
    }

    response = client.get("/fib")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["query", "n"],
                "msg": "Field required",
                "input": None,
            }
        ]
    }

    response = client.get("/fib?n=")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["query", "n"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "",
            }
        ]
    }

    response = client.get("/fib?n=1.1")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["query", "n"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "1.1",
            }
        ]
    }


def test_fibonacci_unexpected_error():
    with patch("app.main.fast_doubling_fibonacci") as mock_fib:
        mock_fib.side_effect = Exception("Unexpected error")
        response = client.get("/fib?n=10")
        assert response.status_code == 500
        assert response.json() == {"detail": "Internal Server Error"}
