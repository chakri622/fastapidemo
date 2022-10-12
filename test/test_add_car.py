from fastapi.testclient import TestClient
from unittest.mock import Mock

from main import app
from routers.cars import add_car
from schemas import CarInput, User, Car

client = TestClient(app)


def test_add_car_with_mock_session():
    mock_session = Mock()
    input = CarInput(doors=2, size="xl")
    user = User(username="chakri")
    result =  add_car(car_input=input, session=mock_session, user=user)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

    assert isinstance(result, Car)
    assert result.doors == 2
    assert  result.size == "xl"




