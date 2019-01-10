import vtk
from math import sin, cos, radians
from constants import GALE_SPEED


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def create_actor(x, y, wind, is_visible):
    wind_speed = wind.get('speed') if wind is not None and wind.get('speed') is not None else 0
    direction = wind.get('deg') if wind is not None and wind.get('deg') is not None else 0
    arrow_length = wind_speed * 10

    arrow_source = vtk.vtkArrowSource()
    arrow_source.SetShaftResolution(50)
    arrow_source.SetTipResolution(50)

    start_point = [x, y, 15]
    end_point = [x - arrow_length * sin(radians(direction)), y - arrow_length * cos(radians(direction)), 15]

    # Compute a basis
    normalized_x = [0, 0, 0]
    normalized_y = [0, 0, 0]
    normalized_z = [0, 0, 0]

    # The X axis is a vector from start to end
    math = vtk.vtkMath()
    math.Subtract(end_point, start_point, normalized_x)
    length = math.Norm(normalized_x)
    math.Normalize(normalized_x)

    # The Z axis is an arbitrary vector cross X
    arbitrary = [1, 1, 1]
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

    transform_filter = vtk.vtkTransformPolyDataFilter()
    transform_filter.SetTransform(transform)
    transform_filter.SetInputConnection(arrow_source.GetOutputPort())

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(transform_filter.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    # wind equal or faster than gale speed - 30 m/s (108 km/h) - will be full red
    actor.GetProperty().SetColor(clamp(2 * wind_speed / GALE_SPEED, 0, 1),
                                 clamp(2 * (1 - (wind_speed / GALE_SPEED)), 0, 1),
                                 0)
    actor.SetVisibility(is_visible)

    return actor