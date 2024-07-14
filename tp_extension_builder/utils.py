import build123d as bd
from typing import Any, List, Union

AlignT = Union[
    bd.Align,
    tuple[bd.Align, bd.Align, bd.Align]
]

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
    '''
    Returns build123d values of self._debug as a list for debugging in
    ocp_viewer if the `self._debug` property exists and has build123d
    shape objects.
    '''
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
