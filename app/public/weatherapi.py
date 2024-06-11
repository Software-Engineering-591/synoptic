from datetime import datetime
from time import time
from functools import lru_cache
from typing import Optional
from pydantic.dataclasses import dataclass
from pydantic import BaseModel, Field


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
    wind: WindData
    # visibility: int
    pop: float
    sys: G
    dt_txt: datetime
    cloud: Optional[float] = Field(None, alias='clouds.all')
    rain: Optional[float] = Field(None, alias='rain.3h')


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


@lru_cache()
def _get_weather_data(ttl=None, **params) -> WeatherResponse:
    del ttl  # unused
    """
    Get weather data from openweathermap.org
    This function is cached for 20 seconds.
    """
    import requests

    print('getting weather data')
    response = requests.get(
        'https://api.openweathermap.org/data/2.5/forecast',
        params=params,
    )
    return WeatherResponse.model_validate_json(response.content)


def get_ttl(seconds: int = 20) -> int:
    return time() // seconds  # type: ignore // does floor division stupid!


def get_weather_data(**params) -> WeatherResponse:
    """
    Get weather data from openweathermap.org

    Returns a WeatherResponse object,
    you need to check if the response.cod is 200 or not.

    :param params: params to pass to openweathermap.org
    """
    return _get_weather_data(get_ttl(), **params)


@dataclass
class DailyWeather:
    date: datetime
    max_temp: float
    min_temp: float
    average_temp: float
    total_rain: float


def get_weekly_weather(**params) -> Optional[list[DailyWeather]]:
    """
    Get daily weather data from openweathermap.org

    Returns a list of DailyWeather objects,
    Returns None if the response.cod is not 200.

    :param params: params to pass to openweathermap.org
    """
    data = get_weather_data(**params)
    if not data.is_ok():
        return None

    sentinal = data.list[0].dt_txt
    current_weather = []
    daily_weather = []
    for weather in data.list:
        if weather.dt_txt.date() != sentinal.date():
            daily_weather.append(
                DailyWeather(
                    date=sentinal,  # ignore time
                    max_temp=max(current_weather, key=lambda x: x.main.temp).main.temp,
                    min_temp=min(current_weather, key=lambda x: x.main.temp).main.temp,
                    average_temp=sum(weather.main.temp for weather in current_weather)
                    / len(current_weather),
                    total_rain=sum(
                        weather.rain
                        for weather in current_weather
                        if weather.rain is not None
                    ),
                )
            )
            sentinal = weather.dt_txt
            current_weather = []
        current_weather.append(weather)

    # The above code is something I just spewed out of my head.
    # but it works.

    return daily_weather
