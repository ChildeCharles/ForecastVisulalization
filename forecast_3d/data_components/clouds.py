import vtk
from constants import colors


def create_actor(x, y, clouds, is_visible):
    cloud_volume = 0
    cloud_volume += clouds.get('all') if clouds is not None and clouds.get('all') is not None else 0

    sphere_source = vtk.vtkSphereSource()
    radius = cloud_volume / 5
    sphere_source.SetRadius(radius)
    sphere_source.SetPhiResolution(50)
    sphere_source.SetThetaResolution(50)
    sphere_source.SetCenter(x - 25, y + 10, 35)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(sphere_source.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('clouds'))
    actor.GetProperty().SetOpacity(cloud_volume / 100)
    actor.SetVisibility(is_visible)

    return actor
