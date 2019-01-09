import vtk
from constants import colors


def create_actor(x, y, rain, snow, is_visible):
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

    return actor
