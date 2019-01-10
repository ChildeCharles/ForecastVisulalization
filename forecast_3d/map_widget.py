import vtk
from PyQt5.QtWidgets import *
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from constants import IMAGES_PATH, MAP_FILENAME
from forecast_3d import legend
from forecast_3d.data_components import clouds, precipitation, pressure, temperature, wind


def normalize(value, minimum, maximum):
    return (value - minimum) / (maximum - minimum)


class MapWidget:
    def __init__(self, parent: QWidget, geographic_bounds: dict, cities: list):
        self.parent = parent
        self.geographic_bounds = geographic_bounds
        self.cities = cities
        self.vtk_widget = QVTKRenderWindowInteractor(parent)
        self.vtk_widget.resize(parent.size())
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        self.actors = {'precipitation': [], 'clouds': [], 'wind': [], 'temperature': [], 'pressure': []}
        self.map_actor = None
        self.legend_actors = {'temperature': [], 'pressure': []}

        self.initialize_map()
        self.initialize_legend()
        self.interactor.Initialize()
        self.renderer.GetActiveCamera().Elevation(-15)
        self.renderer.ResetCamera()

    def update_size(self):
        self.vtk_widget.resize(self.parent.size())
        for actor in self.legend_actors['temperature'] + self.legend_actors['pressure']:
            self.renderer.RemoveActor(actor)
        self.initialize_legend()

    def initialize_map(self):
        reader = vtk.vtkJPEGReader()
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

    def initialize_legend(self):
        self.legend_actors['temperature'] = \
            legend.create_temperature_actors(self.vtk_widget.size().width(), self.vtk_widget.size().height())
        for actor in self.legend_actors['temperature']:
            self.renderer.AddActor(actor)
        self.legend_actors['pressure'] = \
            legend.create_pressure_actors(self.vtk_widget.size().width(), self.vtk_widget.size().height())
        for actor in self.legend_actors['pressure']:
            self.renderer.AddActor(actor)

    def render_data(self, weather_data, visibilities):
        self.clear_data()
        for city_id, city_data in weather_data.items():
            coord = self.get_city_coord(city_id)
            x, y = self.geographic_to_vtk_coordinates(coord)

            self.actors['precipitation'].append(
                precipitation.create_actor(x, y, city_data.get('rain'), city_data.get('snow'), visibilities.get('precipitation')))
            self.renderer.AddActor(self.actors['precipitation'][-1])

            self.actors['clouds'].append(clouds.create_actor(x, y, city_data.get('clouds'), visibilities.get('clouds')))
            self.renderer.AddActor(self.actors['clouds'][-1])

            self.actors['wind'].append(wind.create_actor(x, y, city_data.get('wind'), visibilities.get('wind')))
            self.renderer.AddActor(self.actors['wind'][-1])

            temperature_actor, temperature_text_actor = temperature.create_actors(
                x, y, city_data['main']['temp'], visibilities.get('temperature'))
            if temperature_actor is not None:
                self.actors['temperature'].append(temperature_actor)
                self.renderer.AddActor(temperature_actor)
                self.actors['temperature'].append(temperature_text_actor)
                self.renderer.AddActor(temperature_text_actor)

            pressure_actor, pressure_text_actor = pressure.create_actors(
                x, y, city_data['main']['pressure'], visibilities.get('pressure'))
            if pressure_actor is not None:
                self.actors['pressure'].append(pressure_actor)
                self.renderer.AddActor(pressure_actor)
                self.actors['pressure'].append(pressure_text_actor)
                self.renderer.AddActor(pressure_text_actor)

        self.vtk_widget.update()

    def clear_data(self):
        for key, values in self.actors.items():
            for actor in values:
                self.renderer.RemoveActor(actor)
            self.actors[key].clear()

    def toggle_data(self, checked, key):
        for actor in self.actors[key]:
            actor.SetVisibility(bool(checked))
        if key in self.legend_actors:
            for legend_actor in self.legend_actors[key]:
                legend_actor.SetVisibility(bool(checked))
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

    def reset_camera(self):
        camera = vtk.vtkCamera()
        self.renderer.SetActiveCamera(camera)
        self.renderer.ResetCamera()
        self.renderer.GetActiveCamera().Elevation(-15)
        self.vtk_widget.update()
