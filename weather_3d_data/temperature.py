import vtk
from constants import temperature_thresholds, temperature_colors, temperature_labels


def create_actors(x, y, temperature, is_visible):
    if temperature is None:
        return None, None

    cube_source = vtk.vtkCubeSource()
    cube_source.SetXLength(30)
    cube_source.SetYLength(30)
    cube_source.SetZLength(1)
    cube_source.SetCenter(x, y - 19, 0)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(cube_source.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    temperature_label = temperature_labels[get_temperature_label_index(temperature)]
    actor.GetProperty().SetColor(temperature_colors.GetColor3d(temperature_label))
    actor.SetVisibility(is_visible)

    atext = vtk.vtkVectorText()
    atext.SetText("{:.1f}".format(temperature).center(5))
    textMapper = vtk.vtkPolyDataMapper()
    textMapper.SetInputConnection(atext.GetOutputPort())
    textActor = vtk.vtkFollower()
    textActor.SetMapper(textMapper)
    textActor.SetScale(8, 8, 8)
    textActor.AddPosition(x - 16, y - 23, 1)
    textActor.GetProperty().SetColor(0, 0, 0)

    return actor, textActor


def get_temperature_label_index(temperature):
    for index, threshold in enumerate(temperature_thresholds):
        if temperature <= threshold:
            return index
    return len(temperature_thresholds)
