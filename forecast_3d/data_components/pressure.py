import vtk
from constants import pressure_thresholds, pressure_colors, pressure_labels


def create_actors(x, y, pressure, is_visible):
    if pressure is None:
        return None, None

    cube_source = vtk.vtkCubeSource()
    cube_source.SetXLength(30)
    cube_source.SetYLength(30)
    cube_source.SetZLength(1)
    cube_source.SetCenter(x - 30, y - 19, 0)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(cube_source.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    pressure_label = pressure_labels[get_pressure_label_index(pressure)]
    actor.GetProperty().SetColor(pressure_colors.GetColor3d(pressure_label))
    actor.SetVisibility(is_visible)

    atext = vtk.vtkVectorText()
    atext.SetText("{:.0f}".format(pressure).center(4))
    textMapper = vtk.vtkPolyDataMapper()
    textMapper.SetInputConnection(atext.GetOutputPort())
    textActor = vtk.vtkFollower()
    textActor.SetMapper(textMapper)
    textActor.SetScale(8, 8, 8)
    textActor.AddPosition(x - 15 - 30, y - 23, 1)
    textActor.GetProperty().SetColor(1, 1, 1)
    textActor.SetVisibility(is_visible)

    return actor, textActor


def get_pressure_label_index(pressure):
    for index, threshold in enumerate(pressure_thresholds):
        if pressure <= threshold:
            return index
    return len(pressure_thresholds)
