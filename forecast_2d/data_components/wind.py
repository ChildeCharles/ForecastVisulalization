from numpy import nan


def get_y_values(forecast):
    # convert m/s to km/h
    return [
        forecast_item.get('wind').get('speed') * 3.6
        if forecast_item.get('wind') is not None and forecast_item.get('wind').get('speed') is not None
        else nan
        for forecast_item in forecast
    ]
