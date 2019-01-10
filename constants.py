import vtk

MAX_DAY_OFFSET = 4
IMAGES_PATH = "./images/"
MAP_FILENAME = "poland_map_small.jpg"
CLOUD_FILENAME = "cloud.stl"
GALE_SPEED = 30  # m/s

colors = vtk.vtkNamedColors()
colors.SetColor("precipitation", [0, 0, 255, 255])
colors.SetColor("clouds", [255, 255, 255, 255])
colors.SetColor("wind", [0, 0, 255, 255])
colors.SetColor("yellow", [255, 255, 0, 255])
colors.SetColor("greenish", [13, 241, 0, 255])


temperature_thresholds = [x * 10 for x in range(-2, 5 + 1)]
temperature_labels = ['> {}'.format(x) for x in temperature_thresholds]
temperature_labels.insert(0, '< {}'.format(temperature_thresholds[0]))

temperature_colors = vtk.vtkNamedColors()
temperature_colors.SetColor(temperature_labels[8], [255, 0, 0, 255])
temperature_colors.SetColor(temperature_labels[7], [255, 85, 0, 255])
temperature_colors.SetColor(temperature_labels[6], [255, 170, 0, 255])
temperature_colors.SetColor(temperature_labels[5], [255, 255, 0, 255])
temperature_colors.SetColor(temperature_labels[4], [128, 255, 0, 255])
temperature_colors.SetColor(temperature_labels[3], [0, 255, 255, 255])
temperature_colors.SetColor(temperature_labels[2], [0, 170, 255, 255])
temperature_colors.SetColor(temperature_labels[1], [0, 85, 255, 255])
temperature_colors.SetColor(temperature_labels[0], [0, 0, 255, 255])


pressure_thresholds = [x * 10 for x in range(97, 104 + 1)]
pressure_labels = ['>{}'.format(x) for x in pressure_thresholds]
pressure_labels.insert(0, '<{}'.format(pressure_thresholds[0]))

pressure_colors = vtk.vtkNamedColors()
pressure_colors.SetColor(pressure_labels[8], [230, 120, 255, 255])
pressure_colors.SetColor(pressure_labels[7], [220, 90, 215, 255])
pressure_colors.SetColor(pressure_labels[6], [210, 60, 195, 255])
pressure_colors.SetColor(pressure_labels[5], [200, 30, 175, 255])
pressure_colors.SetColor(pressure_labels[4], [200, 0, 155, 255])
pressure_colors.SetColor(pressure_labels[3], [160, 0, 135, 255])
pressure_colors.SetColor(pressure_labels[2], [120, 0, 115, 255])
pressure_colors.SetColor(pressure_labels[1], [80, 0, 95, 255])
pressure_colors.SetColor(pressure_labels[0], [40, 0, 75, 255])
