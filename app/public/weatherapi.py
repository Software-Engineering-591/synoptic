from datetime import datetime
from pydantic.dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class WeatherReport:
    id: int
    main: str  # What is the current weather
    description: str  # in depth of main
    icon: str  # what is 04n??


@dataclass
class WeatherStats:
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    sea_level: int
    grnd_level: int
    humidity: int
    temp_kf: float


@dataclass
class CloudData:
    all: int


@dataclass
class WindData:
    speed: float
    deg: int
    gust: float


@dataclass
class G:
    pod: str


@dataclass
class WeatherData:
    dt: int
    main: WeatherStats
    weather: list[WeatherReport]
    clouds: CloudData
    wind: WindData
    # visibility: int
    pop: float
    sys: G
    dt_txt: datetime


@dataclass
class GeoLocation:
    lat: float
    lon: float


@dataclass
class CityInfo:
    id: int
    name: str
    coord: GeoLocation
    country: str
    population: int
    timezone: int
    sunrise: int
    sunset: int


class WeatherResponse(BaseModel):
    cod: int
    message: int
    cnt: int
    list: list[WeatherData]
    city: CityInfo

    def is_ok(self):
        return self.cod == 200


def get_weather_data(**params) -> WeatherResponse:
    """
    Get weather data from openweathermap.org

    Returns a WeatherResponse object,
    you need to check if the response.cod is 200 or not.

    :param params: params to pass to openweathermap.org
    """
    import requests

    response = requests.get(
        'https://api.openweathermap.org/data/2.5/forecast',
        params=params,
    )
    return WeatherResponse.model_validate_json(response.content)
