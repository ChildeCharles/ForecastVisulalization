def get_y_values(forecast):
    return [forecast_item['main']['pressure'] for forecast_item in forecast]