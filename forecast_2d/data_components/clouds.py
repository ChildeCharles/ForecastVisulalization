from numpy import nan


def get_y_values(forecast):
    return [
        forecast_item.get('clouds').get('all')
        if forecast_item.get('clouds') is not None and forecast_item.get('clouds').get('all') is not None
        else nan
        for forecast_item in forecast
    ]
