import vtk
from constants import colors, IMAGES_PATH, CLOUD_FILENAME


def create_actor(x, y, clouds, is_visible):
    cloud_volume = 0
    cloud_volume += clouds.get('all') if clouds is not None and clouds.get('all') is not None else 0

    cloud_source = vtk.vtkSTLReader()
    cloud_source.SetFileName(IMAGES_PATH + CLOUD_FILENAME)

    translation = vtk.vtkTransform()
    translation.Translate(x - 25 - 30, y + 10 - 50, 35)
    translation.Scale(cloud_volume / 100, cloud_volume / 100, cloud_volume / 100)

    transform_filter = vtk.vtkTransformPolyDataFilter()
    transform_filter.SetTransform(translation)
    transform_filter.SetInputConnection(cloud_source.GetOutputPort())

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(transform_filter.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('clouds'))
    actor.GetProperty().SetOpacity(cloud_volume / 200 + 0.5)
    actor.SetVisibility(is_visible)

    return actor
