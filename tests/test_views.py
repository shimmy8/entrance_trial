from fastapi.testclient import TestClient

from src.run import app
from src.service import CalculationsService


client = TestClient(app)


class ServiceMock:
    def read_one(self, *args, **kwargs):
        return {
            "id": 2,
            "status": "complete",
            "calc_start": "2022-11-28T12:14:19.892858",
            "calc_fin": "2022-11-28T12:14:29.906295",
            "calc_time": 10,
            "date_start": "2022-11-27",
            "date_fin": "2022-11-28",
            "lag": 1,
            "results": [
                {"date": "2022-11-27", "liquid": 17.030682, "oil": 16.085, "water": 0.94568133, "wct": 0.0555281},
                {"date": "2022-11-28", "liquid": 14.983521, "oil": 3.7244835, "water": 11.259038, "wct": 0.751428},
            ],
        }

    def read_many(self, *args, **kwargs):
        return [
            {"id": 2, "status": "complete", "calc_start": "2022-11-28T12:00:11.424926"},
            {"id": 1, "status": "queued", "calc_start": "2022-11-28T11:59:08.490282"},
        ]


app.dependency_overrides[CalculationsService] = ServiceMock


def test_calculations_list():
    response = client.get("/calculations")
    assert response.json() == {"detail": "Invalid X-Token header"}
