from numpy import nan
from numpy import isnan


def get_y_values(forecast):
    rain_values = []
    snow_values = []
    sum_values = []

    for forecast_item in forecast:
        rain = forecast_item.get('rain').get('3h') if forecast_item.get('rain') is not None and forecast_item.get('rain').get('3h') is not None else 0
        snow = forecast_item.get('snow').get('3h') if forecast_item.get('snow') is not None and forecast_item.get('snow').get('3h') is not None else 0
        rain_values.append(rain)
        snow_values.append(snow)
        sum_values.append(rain + snow)

    return rain_values, snow_values, sum_values
