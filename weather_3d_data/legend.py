import vtk
from constants import temperature_labels, temperature_colors, pressure_labels, pressure_colors


def create_temperature_actors(widget_width, widget_height):
    legend_actors = []

    temperature_item_height = widget_height / (len(temperature_labels) + 1)
    temperature_item_width = 60

    for index, temperature in enumerate(temperature_labels):
        cube_source = vtk.vtkCubeSource()
        cube_source.SetXLength(temperature_item_width)
        cube_source.SetYLength(temperature_item_height)
        cube_source.SetCenter(widget_width - (temperature_item_width / 2),
                              temperature_item_height / 2 + index * temperature_item_height,
                              0)

        mapper = vtk.vtkPolyDataMapper2D()
        mapper.SetInputConnection(cube_source.GetOutputPort())

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(temperature_colors.GetColor3d(temperature))

        legend_actors.append(actor)

        txt = vtk.vtkTextActor()
        txt.SetInput(temperature)
        txt.GetTextProperty().SetFontFamilyToTimes()
        txt.GetTextProperty().SetFontSize(18)
        txt.GetTextProperty().SetColor(0, 0, 0)
        txt.SetDisplayPosition(int(widget_width - (temperature_item_width / 2) - 20),
                               int((temperature_item_height / 2) + (index * temperature_item_height) - 12))

        legend_actors.append(txt)

    cube_source = vtk.vtkCubeSource()
    cube_source.SetXLength(temperature_item_width)
    cube_source.SetYLength(temperature_item_height)
    cube_source.SetCenter(widget_width - (temperature_item_width / 2),
                          temperature_item_height / 2 + len(temperature_labels) * temperature_item_height,
                          0)

    mapper = vtk.vtkPolyDataMapper2D()
    mapper.SetInputConnection(cube_source.GetOutputPort())

    actor = vtk.vtkActor2D()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1, 1, 1)

    legend_actors.append(actor)

    txt = vtk.vtkTextActor()
    txt.SetInput("T [ºC]")
    txt.GetTextProperty().SetFontFamilyToTimes()
    txt.GetTextProperty().SetFontSize(18)
    txt.GetTextProperty().SetColor(0, 0, 0)
    txt.SetDisplayPosition(int(widget_width - (temperature_item_width / 2) - 25),
                           int(temperature_item_height / 2 + len(temperature_labels) * temperature_item_height - 12))

    legend_actors.append(txt)

    return legend_actors


def create_pressure_actors(widget_width, widget_height):
    legend_actors = []

    pressure_item_height = widget_height / (len(pressure_labels) + 1)
    pressure_item_width = 60

    for index, pressure in enumerate(pressure_labels):
        cube_source = vtk.vtkCubeSource()
        cube_source.SetXLength(pressure_item_width)
        cube_source.SetYLength(pressure_item_height)
        cube_source.SetCenter(pressure_item_width / 2,
                              pressure_item_height / 2 + index * pressure_item_height,
                              0)

        mapper = vtk.vtkPolyDataMapper2D()
        mapper.SetInputConnection(cube_source.GetOutputPort())

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(pressure_colors.GetColor3d(pressure))

        legend_actors.append(actor)

        txt = vtk.vtkTextActor()
        txt.SetInput(pressure)
        txt.GetTextProperty().SetFontFamilyToTimes()
        txt.GetTextProperty().SetFontSize(18)
        txt.GetTextProperty().SetColor(1, 1, 1)
        txt.SetDisplayPosition(int(pressure_item_width / 2 - 27),
                               int((pressure_item_height / 2) + (index * pressure_item_height) - 12))

        legend_actors.append(txt)

    cube_source = vtk.vtkCubeSource()
    cube_source.SetXLength(pressure_item_width)
    cube_source.SetYLength(pressure_item_height)
    cube_source.SetCenter(pressure_item_width / 2,
                          pressure_item_height / 2 + len(pressure_labels) * pressure_item_height,
                          0)

    mapper = vtk.vtkPolyDataMapper2D()
    mapper.SetInputConnection(cube_source.GetOutputPort())

    actor = vtk.vtkActor2D()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1, 1, 1)

    legend_actors.append(actor)

    txt = vtk.vtkTextActor()
    txt.SetInput("p [hPa]")
    txt.GetTextProperty().SetFontFamilyToTimes()
    txt.GetTextProperty().SetFontSize(18)
    txt.GetTextProperty().SetColor(0, 0, 0)
    txt.SetDisplayPosition(int(pressure_item_width / 2 - 29),
                           int(pressure_item_height / 2 + len(pressure_labels) * pressure_item_height - 12))

    legend_actors.append(txt)

    return legend_actors
