import build123d as bd
from typing import cast, Any, List, Union, Tuple, Optional

AlignT = Union[bd.Align, tuple[bd.Align, bd.Align, bd.Align]]

ALIGN_CENTER = (
    bd.Align.CENTER,
    bd.Align.CENTER,
    bd.Align.CENTER,
)

ALIGN_CENTER_BOTTOM = (
    bd.Align.CENTER,
    bd.Align.CENTER,
    bd.Align.MIN,
)

ALIGN_CENTER_TOP = (
    bd.Align.CENTER,
    bd.Align.CENTER,
    bd.Align.MAX,
)


def get_bd_debug_objects(bd_obj_instance: Any) -> List[bd.Shape]:
    """
    Returns build123d values of self._debug as a list for debugging in
    ocp_viewer if the `self._debug` property exists and has build123d
    shape objects.
    """
    debug = []
    if hasattr(bd_obj_instance, '_debug'):
        if isinstance(bd_obj_instance._debug, list) is True:
            debug.extend(bd_obj_instance._debug)
        elif isinstance(bd_obj_instance._debug, bd.Shape):
            debug.append(bd_obj_instance._debug)
        else:
            raise ValueError(
                f'_debug contains invalid type: {type(bd_obj_instance._debug)}'
            )

    return debug


def align_shape(
    shape: bd.Shape,
    align: AlignT,
) -> bd.Shape:
    """
    Returns a copy of the shape that has been moved to the alignment.
    """

    def get_align_offset(
        shape: bd.Shape,
        align: AlignT,
    ) -> Tuple[float, float, float]:
        """
        Amount to move object to achieve the desired alignment.

        From bd.BoundingBox.to_align_offset, but expanded for a 3d move.
        """
        align = bd.tuplify(align, 3)

        align_offset = []
        for i in range(3):
            if align[i] == bd.Align.MIN:
                align_offset.append(-shape.bounding_box().min.to_tuple()[i])
            elif align[i] == bd.Align.CENTER:
                align_offset.append(
                    -(
                        shape.bounding_box().min.to_tuple()[i]
                        + shape.bounding_box().max.to_tuple()[i]
                    )
                    / 2
                )
            elif align[i] == bd.Align.MAX:
                align_offset.append(-shape.bounding_box().max.to_tuple()[i])
        return (align_offset[0], align_offset[1], align_offset[2])

    align_location = bd.Location(get_align_offset(shape=shape, align=align))

    shape_aligned = shape.moved(align_location)

    return shape_aligned


def combine_shapes(
    shapes: List[bd.Shape],
    distance: float,
    add_sprue: bool,
    sprue_radius: float = 1.0,
    sprue_offset: Optional[bd.Vector] = None,
    align: AlignT = (bd.Align.MIN, bd.Align.MIN, bd.Align.MIN),
) -> bd.Shape:
    if sprue_offset is None:
        sprue_offset = bd.Vector(0, -0.1, 0)

    with bd.BuildPart() as sprued_shapes:
        sprue_align = (bd.Align.MIN, bd.Align.MAX, bd.Align.MIN)
        shapes_aligned = [align_shape(shape, sprue_align) for shape in shapes]

        offset = 0.0
        for shape in shapes_aligned:
            with bd.Locations((offset, 0, 0)):
                bd.add(shape)

            shape_size = shape.bounding_box().size
            offset += shape_size.X + distance

        if add_sprue is True and len(shapes_aligned) > 1:
            sprue_start_x = shapes_aligned[0].position.X
            last_obj_width = shapes_aligned[-1].bounding_box().size.X
            sprue_length = offset - sprue_start_x - last_obj_width / 2

            sprue_start_x += sprue_offset.X
            with bd.BuildSketch(bd.Plane.ZY.offset(-sprue_start_x)):
                with bd.Locations((sprue_offset.Z, sprue_offset.Y)):
                    bd.Circle(
                        radius=sprue_radius,
                        align=(bd.Align.MIN, bd.Align.MIN),
                    )
            bd.extrude(amount=-sprue_length)

    sprued_shapes = sprued_shapes.part

    sprued_shapes = align_shape(sprued_shapes, align)

    return cast(bd.Shape, sprued_shapes)
