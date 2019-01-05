from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
from constants import IMAGES_PATH, MAP_FILENAME, GALE_SPEED
from math import sin, cos, radians

colors = vtk.vtkNamedColors()
colors.SetColor("precipitation", [0, 0, 255, 255])
colors.SetColor("clouds", [255, 255, 255, 255])
colors.SetColor("wind", [0, 0, 255, 255])
colors.SetColor("yellow", [255, 255, 0, 255])
colors.SetColor("greenish", [13, 241, 0, 255])


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def normalize(value, minimum, maximum):
    return (value - minimum) / (maximum - minimum)


class MapWidget:
    def __init__(self, parent: QWidget, geographic_bounds: dict, cities: list):
        self.geographic_bounds = geographic_bounds
        self.cities = cities
        self.vtk_widget = QVTKRenderWindowInteractor(parent)
        self.vtk_widget.resize(parent.size())
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        interactor_style = vtk.vtkInteractorStyleTrackballCamera()
        self.interactor.SetInteractorStyle(interactor_style)

        self.actors = {'precipitation': [], 'clouds': [], 'wind': [], 'temperature': [], 'pressure': []}
        self.map_actor = None

        self.init_map()
        self.interactor.Initialize()
        self.renderer.GetActiveCamera().Elevation(-45)
        self.renderer.ResetCamera()

    def init_map(self):
        reader = vtk.vtkPNGReader()
        reader.SetFileName(IMAGES_PATH + MAP_FILENAME)
        reader.Update()

        filter = vtk.vtkImageDataGeometryFilter()
        filter.SetInputConnection(reader.GetOutputPort())
        filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(filter.GetOutputPort())

        self.map_actor = vtk.vtkActor()
        self.map_actor.SetMapper(mapper)
        self.renderer.AddActor(self.map_actor)

    def render_data(self, weather_data, visibilities):
        self.clear_data()
        for city_id, city_data in weather_data.items():
            coord = self.get_city_coord(city_id)
            x, y = self.geographic_to_vtk_coordinates(coord)

            self.render_precipitation(x, y, city_data.get('rain'), city_data.get('snow'), visibilities.get('precipitation'))
            self.render_clouds(x, y, city_data.get('clouds'), visibilities.get('clouds'))
            self.render_wind(x, y, city_data.get('wind'), visibilities.get('wind'))

            self.vtk_widget.update()

    def clear_data(self):
        for key, values in self.actors.items():
            for actor in values:
                self.renderer.RemoveActor(actor)
            self.actors[key].clear()

    def render_precipitation(self, x, y, rain, snow, is_visible):
        precipitation = 0
        precipitation += rain.get('3h') if rain is not None and rain.get('3h') is not None else 0
        precipitation += snow.get('3h') if snow is not None and snow.get('3h') is not None else 0

        cube_source = vtk.vtkCubeSource()
        cube_source.SetXLength(7)
        cube_source.SetYLength(7)
        height = precipitation * 50
        cube_source.SetZLength(height)
        cube_source.SetCenter(x, y, height / 2)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(cube_source.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(colors.GetColor3d('precipitation'))
        actor.SetVisibility(is_visible)

        self.renderer.AddActor(actor)
        self.actors['precipitation'].append(actor)

    def render_clouds(self, x, y, clouds, is_visible):
        cloud_volume = 0
        cloud_volume += clouds.get('all') if clouds is not None and clouds.get('all') is not None else 0

        sphere_source = vtk.vtkSphereSource()
        radius = cloud_volume / 4
        sphere_source.SetRadius(radius)
        sphere_source.SetPhiResolution(50)
        sphere_source.SetThetaResolution(50)
        sphere_source.SetCenter(x - 25, y - 25, 35)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere_source.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(colors.GetColor3d('clouds'))
        actor.GetProperty().SetOpacity(cloud_volume / 100)
        actor.SetVisibility(is_visible)

        self.renderer.AddActor(actor)
        self.actors['clouds'].append(actor)

    def render_wind(self, x, y, wind, is_visible):
        wind_speed = wind.get('speed') if wind is not None and wind.get('speed') is not None else 0
        direction = wind.get('deg') if wind is not None and wind.get('deg') is not None else 0
        arrow_length = wind_speed * 10

        arrow_source = vtk.vtkArrowSource()
        arrow_source.SetShaftResolution(50)
        arrow_source.SetTipResolution(50)

        # Generate a random start and end point
        start_point = [x, y, 5]
        end_point = [x - arrow_length * sin(radians(direction)), y - arrow_length * cos(radians(direction)), 5]

        # Compute a basis
        normalized_x = [0 for i in range(3)]
        normalized_y = [0 for i in range(3)]
        normalized_z = [0 for i in range(3)]

        # The X axis is a vector from start to end
        math = vtk.vtkMath()
        math.Subtract(end_point, start_point, normalized_x)
        length = math.Norm(normalized_x)
        math.Normalize(normalized_x)

        # The Z axis is an arbitrary vector cross X
        arbitrary = [1 for i in range(3)]
        math.Cross(normalized_x, arbitrary, normalized_z)
        math.Normalize(normalized_z)

        # The Y axis is Z cross X
        math.Cross(normalized_z, normalized_x, normalized_y)
        matrix = vtk.vtkMatrix4x4()

        # Create the direction cosine matrix
        matrix.Identity()
        for i in range(3):
            matrix.SetElement(i, 0, normalized_x[i])
            matrix.SetElement(i, 1, normalized_y[i])
            matrix.SetElement(i, 2, normalized_z[i])

        # Apply the transforms
        transform = vtk.vtkTransform()
        transform.Translate(start_point)
        transform.Concatenate(matrix)
        transform.Scale(length, length, length)

        # Transform the polydata
        transform_filter = vtk.vtkTransformPolyDataFilter()
        transform_filter.SetTransform(transform)
        transform_filter.SetInputConnection(arrow_source.GetOutputPort())

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(transform_filter.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        # wind faster than gale speed - 30 m/s (108 km/h) - will be full red
        actor.GetProperty().SetColor(clamp(2 * wind_speed / GALE_SPEED, 0, 1),
                                     clamp(2 * (1 - (wind_speed / GALE_SPEED)), 0, 1),
                                     0)
        actor.SetVisibility(is_visible)

        self.renderer.AddActor(actor)
        self.actors['wind'].append(actor)

    def toggle_precipitation(self, checked):
        for actor in self.actors['precipitation']:
            actor.SetVisibility(bool(checked))
        self.vtk_widget.update()

    def toggle_clouds(self, checked):
        for actor in self.actors['clouds']:
            actor.SetVisibility(bool(checked))
        self.vtk_widget.update()

    def toggle_wind(self, checked):
        for actor in self.actors['wind']:
            actor.SetVisibility(bool(checked))
        self.vtk_widget.update()

    def toggle_pressure(self, checked):
        for actor in self.actors['pressure']:
            actor.SetVisibility(bool(checked))
        self.vtk_widget.update()

    def toggle_temperature(self, checked):
        for actor in self.actors['temperature']:
            actor.SetVisibility(bool(checked))
        self.vtk_widget.update()

    def geographic_to_vtk_coordinates(self, coordinates):
        vtk_width = self.map_actor.GetBounds()[1]
        vtk_height = self.map_actor.GetBounds()[3]

        vtk_x = normalize(coordinates['lon'], self.geographic_bounds['left'], self.geographic_bounds['right']) * vtk_width
        vtk_y = normalize(coordinates['lat'], self.geographic_bounds['lower'], self.geographic_bounds['upper']) * vtk_height

        return vtk_x, vtk_y

    def get_city_coord(self, city_id):
        for city in self.cities:
            if int(city['id']) == int(city_id):
                return city['coord']
