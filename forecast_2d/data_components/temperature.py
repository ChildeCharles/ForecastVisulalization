from numpy import nan


def get_y_values(forecast):
    return [
        forecast_item.get('main').get('temp')
        if forecast_item.get('main') is not None and forecast_item.get('main').get('temp') is not None
        else nan
        for forecast_item in forecast
    ]
