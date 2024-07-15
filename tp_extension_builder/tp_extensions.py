import build123d as bd
import inspect
import math

from copy import copy
from typing import cast, Any, List, Dict, Optional

from tp_extension_builder.tp_caps import (
    TrackPointCapBase,
    TrackPointCapRedT460S,
    TrackPointCapGreenT430,
)

from tp_extension_builder.utils import (
    get_bd_debug_objects,
    ALIGN_CENTER_BOTTOM,
    AlignT,
    align_shape,
)

from tp_extension_builder.defines import (
    D_ADAPTER_WIDTH_BELOW_PCB,
    D_ADAPTER_WIDTH_ABOVE_PCB,
    D_EXTENSION_WIDTH,
    D_PCB_HEIGHT,
    CHOC_SWITCH_MOUNTING_NOTCH_HEIGHT,
)


#
# TP Extension Builder Base Class
#

class TrackPointExtensionBase(bd.BasePartObject):

    def __init__(self,
                 adapter_hole_incr: float,
                 desired_cap_height: float,
                 tp_mounting_distance: float,
                 adapter_width_below_pcb: float,
                 adapter_width_above_pcb: float,
                 extension_width: float,
                 pcb_height: float,
                 space_above_pcb: float,
                 tp_cap: TrackPointCapBase,
                 tp_stem_width: float,
                 tp_stem_height: float,
                 model: str,
                 color: bd.Color = bd.Color('gray'),
                 rotation: bd.RotationLike = (0, 0, 0),
                 align: AlignT = ALIGN_CENTER_BOTTOM,
                 mode: bd.Mode = bd.Mode.ADD,
                 ) -> None:
        context: bd.BuildPart = bd.BuildPart._get_context(self)
        bd.validate_inputs(context, self)

        self._debug: List[bd.Shape] = []

        self._desired_cap_height = abs(desired_cap_height)
        self._tp_mounting_distance = abs(tp_mounting_distance)
        self._adapter_hole_incr = abs(adapter_hole_incr)
        self._adapter_width_below_pcb = abs(
            adapter_width_below_pcb
        )
        self._adapter_width_above_pcb = abs(
            adapter_width_above_pcb
        )
        self._extension_width = abs(extension_width)
        self._pcb_height = abs(pcb_height)
        self._space_above_pcb = abs(space_above_pcb)
        self._tp_stem_width = abs(tp_stem_width)
        self._tp_stem_height = abs(tp_stem_height)
        self._tp_cap = tp_cap

        self._adapter_height = (
            self._tp_mounting_distance
            + self._pcb_height
            + self._space_above_pcb
            - 0.2
        )

        self._adapter_hole_width = (
            self._tp_stem_width
            + self._adapter_hole_incr
        )
        self._adapter_hole_height = (
            self._tp_stem_height
            + self._adapter_hole_incr
        )

        # Since a portion of the extension adapter will be below the top of the
        # pcb, we calculate the length that it will extend above the pcb here
        self._adapter_height_below_pcb = (
            self._pcb_height
            + self._tp_mounting_distance
        )
        self._adapter_height_above_pcb = (
            self._adapter_height
            - self._adapter_height_below_pcb
        )

        # Height of the part between the mount at the bottom and tip at the top
        self._extension_height = (
            self._desired_cap_height
            - self._tp_cap.total_height
            - self._adapter_height_above_pcb
        )

        self._total_height = (
            self._adapter_height
            + self._extension_height
            + self._tp_cap.cap_adapter_height
        )

        self.model = model

        extension = self._build_extension()

        self._init_params = self._get_init_params(
            exclude_list=[
                'color',
                'rotation',
                'align',
                'mode',
                'tp_cap'
            ]
        )

        super().__init__(
            part=extension,
            rotation=rotation,
            align=bd.tuplify(align, 3),
            mode=mode,
        )

        self.label = f'TP Extension - {self.model}'
        self.color = color

    def _get_init_params(self,
                         exclude_list: Optional[List[str]] = None,
                         ) -> Dict[str, Any]:
        if exclude_list is None:
            exclude_list = []
        if 'self' not in exclude_list:
            exclude_list.append('self')

        frame = inspect.currentframe()
        if not frame or not frame.f_back or not frame.f_back.f_back:
            return {}
        else:
            frame = frame.f_back.f_back

        args, _, _, values = inspect.getargvalues(frame)
        params = {
            arg: values[arg]
            for arg in args
            if arg not in exclude_list
        }

        return params

    @property
    def info(self) -> str:

        size = self.bounding_box().size
        cap_size = self._tp_cap.bounding_box().size
        cap_height_incr = cap_size.Z - self._tp_cap.hole_depth

        above_pcb_height = (
            self._total_height
            - self._adapter_height_below_pcb
        )
        above_pcb_height_with_cap = (
            above_pcb_height
            + self._tp_cap.cap_extra_height
        )

        adapter_hole_corner_distance = (
            math.sqrt(
                self._adapter_hole_width * self._adapter_hole_width
                + self._adapter_hole_width * self._adapter_hole_width
            )
        )
        adapter_wall_thickness_below_pcb = (
            (
                self._adapter_width_below_pcb
                - self._adapter_hole_width
            ) / 2
        )
        adapter_wall_thickness_above_pcb = (
            (
                self._adapter_width_above_pcb
                - self._adapter_hole_width
            ) / 2
        )
        adapter_corner_wall_thickness_below_pcb = (
            (
                self._adapter_width_below_pcb
                - adapter_hole_corner_distance
            ) / 2
        )
        adapter_corner_wall_thickness_above_pcb = (
            (
                self._adapter_width_above_pcb
                - adapter_hole_corner_distance
            ) / 2
        )
        adapter_corner_wall_thickness_top = (
            self._adapter_height
            - self._adapter_hole_height
        )

        parameters = '\n'.join([
            f'\t{k}: {v}'
            for k, v in self._init_params.items()
        ])

        def fv(value: float,
               format_str: str = '.2f',
               units: str = 'mm') -> str:
            return f'{value:{format_str}}{units}'

        info_list = [
            'Info:',
            f'\t TrackPoint Model: {self.model}',
            f'\t Cap Model: {self._tp_cap.model}',
            '',
            'Parameters:',
            f'{parameters}',
            '',
            'General Size:',
            f'\tTotal Height: {fv(size.Z)}',
            f'\tTotal Width: {fv(max(size.Y, size.X))}',
            f'\tAbove PCB Height: {fv(above_pcb_height)}',
            f'\tAbove PCB Height (With Cap): {fv(above_pcb_height_with_cap)}',
            '',
            'Adapter Hole:',
            (
                f'\t Width: {fv(self._adapter_hole_width)} '
                f'({fv(self._adapter_hole_incr, "+.2f")})'
            ),
            (
                f'\t Depth: {fv(self._adapter_hole_height)} '
                f'({fv(self._adapter_hole_incr, "+.2f")})'
            ),
            f'\t Corner Distance: {fv(adapter_hole_corner_distance)}',
            '',
            'Adapter:',
            f'\t Total Height: {fv(self._adapter_height)}',
            '',
            f'\t Below PCB Height  {fv(self._adapter_height_below_pcb)}',
            f'\t Below PCB Width: {fv(self._adapter_width_below_pcb)}',
            (
                f'\t Below PCB Wall Thickness: '
                f'{fv(adapter_wall_thickness_below_pcb)}'
            ),
            (
                f'\t Below PCB Wall Thickness Corners: '
                f'{fv(adapter_corner_wall_thickness_below_pcb)}'
            ),
            '',
            f'\t Above PCB Height: {fv(self._adapter_height_above_pcb)}',
            f'\t Above PCB Width: {fv(self._adapter_width_above_pcb)}',
            (
                f'\t Above PCB Wall Thickness: '
                f'{fv(adapter_wall_thickness_above_pcb)}'
            ),
            (
                f'\t Above PCB Wall Thickness Corners: '
                f'{fv(adapter_corner_wall_thickness_above_pcb)}'
            ),
            '',
            f'\t Top Wall Thickness: {fv(adapter_corner_wall_thickness_top)}',
            '',
            'Extension:',
            f'\t Height: {fv(self._extension_height)}',
            f'\t Width: {fv(self._extension_width)}',
            '',
            'Cap Adapter:',
            f'\t Height: {fv(self._tp_cap.cap_adapter_height)}',
            f'\t Width: {fv(self._tp_cap.cap_adapter_width)}',
            f'\t Length: {fv(self._tp_cap.cap_adapter_length)}',
            '',
            'Cap:',
            f'\t Hole Depth: {fv(self._tp_cap.hole_depth)}',
            f'\t Hole Width: {fv(self._tp_cap.hole_width)}',
            f'\t Hole Length: {fv(self._tp_cap.hole_length)}',
            f'\t Cap Height: {fv(cap_size.Z)}',
            f'\t Cap Width: {fv(max(cap_size.X, cap_size.Y))}',
            f'\t Cap Height Increase: {fv(cap_height_incr)}',

        ]

        info_str = '\n'.join(info_list)

        return info_str

    @property
    def debug(self) -> List[bd.Shape]:
        '''
        Returns a list of build123d objects for debugging in ocp_viewer.
        '''
        return get_bd_debug_objects(self)

    def for_kicad(self, include_cap: bool = True) -> bd.Shape:
        tp_extension = align_shape(
            self,
            ALIGN_CENTER_BOTTOM,
        )

        # Rotate into original position
        tp_extension.locate(bd.Location(
            tp_extension.position,
            (0, 0, 0),
        ))

        if include_cap is True:

            # Move cap to top of extension tip
            tp_cap = copy(tp_extension._tp_cap)
            tp_cap.move(bd.Location((
                0,
                0,
                tp_extension._total_height - tp_cap.hole_depth,
            )))

            tp_extension = bd.Compound(
                label='TrackPoint Extension',
                shapes=[],
                children=[
                    tp_extension,
                    tp_cap,
                ]
            )

        # Move extension to mounting distance
        tp_extension.move(bd.Location((
            0,
            0,
            -self._pcb_height - self._tp_mounting_distance
        )))

        return tp_extension

    def _build_extension(self) -> bd.Shape:
        with bd.BuildPart() as tp_extension:

            # Below PCB adapter
            below_pcb_adapter = bd.Cylinder(
                radius=self._adapter_width_below_pcb/2,
                height=self._adapter_height_below_pcb,
                align=ALIGN_CENTER_BOTTOM,
            )

            topf = below_pcb_adapter.faces().sort_by(bd.Axis.Z)[-1]
            with bd.Locations(topf):
                above_pcb_adapter = bd.Cylinder(
                    radius=self._adapter_width_above_pcb/2,
                    height=self._adapter_height_above_pcb,
                    align=ALIGN_CENTER_BOTTOM,
                )

            topf = above_pcb_adapter.faces().sort_by(bd.Axis.Z)[-1]
            with bd.Locations(topf):
                extension = bd.Cylinder(
                    radius=self._extension_width/2,
                    height=self._extension_height,
                    align=ALIGN_CENTER_BOTTOM,
                )

            topf = extension.faces().sort_by(bd.Axis.Z)[-1]
            with bd.Locations(topf):
                cap_adapter = self._tp_cap.build_cap_adapter(
                    align=ALIGN_CENTER_BOTTOM
                )
                bd.add(cap_adapter)

            bd.Box(
                width=self._adapter_hole_width + self._adapter_hole_incr,
                length=self._adapter_hole_width + self._adapter_hole_incr,
                height=self._adapter_hole_height + self._adapter_hole_incr,
                mode=bd.Mode.SUBTRACT,
                align=ALIGN_CENTER_BOTTOM,
            )

        tp_extension = tp_extension.part

        return cast(bd.Shape, tp_extension)


#
# TP Extensions
#

class TrackPointExtensionRedT460S(TrackPointExtensionBase):
    def __init__(self,
                 adapter_hole_incr: float,
                 desired_cap_height: float,
                 tp_mounting_distance: float,
                 adapter_width_below_pcb: float = D_ADAPTER_WIDTH_BELOW_PCB,
                 adapter_width_above_pcb: float = D_ADAPTER_WIDTH_ABOVE_PCB,
                 extension_width: float = D_EXTENSION_WIDTH,
                 pcb_height: float = D_PCB_HEIGHT,
                 space_above_pcb: float = CHOC_SWITCH_MOUNTING_NOTCH_HEIGHT,
                 tp_cap: Optional[TrackPointCapBase] = None,
                 color: bd.Color = bd.Color('gray'),
                 rotation: bd.RotationLike = (0, 0, 0),
                 align: AlignT = ALIGN_CENTER_BOTTOM,
                 mode: bd.Mode = bd.Mode.ADD,
                 ) -> None:

        if tp_cap is None:
            tp_cap = TrackPointCapRedT460S()

        # Height from bottom metal part to stem top
        tp_total_height = 4.0

        # Height of the metal and black, round platform part.
        # This is the height that sticks out below the pcb if the
        # TP is mounted totally flush.
        tp_board_thickness = 1.3

        # The height of the white stem (2.7mm)
        tp_stem_height = tp_total_height - tp_board_thickness
        tp_stem_width = 2.2

        super().__init__(
                 # User Settings
                 adapter_hole_incr=adapter_hole_incr,
                 desired_cap_height=desired_cap_height,
                 tp_mounting_distance=tp_mounting_distance,
                 adapter_width_below_pcb=adapter_width_below_pcb,
                 adapter_width_above_pcb=adapter_width_above_pcb,
                 extension_width=extension_width,
                 pcb_height=pcb_height,
                 space_above_pcb=space_above_pcb,

                 # TP Dimensions
                 tp_cap=tp_cap,
                 tp_stem_width=tp_stem_width,
                 tp_stem_height=tp_stem_height,
                 model='Red T460S',

                 color=color,
                 align=align,
                 rotation=rotation,
                 mode=mode,
        )


class TrackPointExtensionGreenT430(TrackPointExtensionBase):
    def __init__(self,
                 adapter_hole_incr: float,
                 desired_cap_height: float,
                 tp_mounting_distance: float,
                 adapter_width_below_pcb: float = D_ADAPTER_WIDTH_BELOW_PCB,
                 adapter_width_above_pcb: float = D_ADAPTER_WIDTH_ABOVE_PCB,
                 extension_width: float = D_EXTENSION_WIDTH,
                 pcb_height: float = D_PCB_HEIGHT,
                 space_above_pcb: float = CHOC_SWITCH_MOUNTING_NOTCH_HEIGHT,
                 tp_cap: Optional[TrackPointCapBase] = None,
                 color: bd.Color = bd.Color('gray'),
                 rotation: bd.RotationLike = (0, 0, 0),
                 align: AlignT = ALIGN_CENTER_BOTTOM,
                 mode: bd.Mode = bd.Mode.ADD,
                 ) -> None:

        if tp_cap is None:
            tp_cap = TrackPointCapGreenT430()

        # Height from bottom metal part to stem top
        tp_total_height = 5.0

        # Height of the metal and black, round platform part.
        # This is the height that sticks out below the pcb if the
        # TP is mounted totally flush.
        tp_board_thickness = 2.5

        # The height of the white stem (2.5mm)
        tp_stem_height = tp_total_height - tp_board_thickness
        tp_stem_width = 2.2

        super().__init__(
                 # User Settings
                 adapter_hole_incr=adapter_hole_incr,
                 desired_cap_height=desired_cap_height,
                 tp_mounting_distance=tp_mounting_distance,
                 adapter_width_below_pcb=adapter_width_below_pcb,
                 adapter_width_above_pcb=adapter_width_above_pcb,
                 extension_width=extension_width,
                 pcb_height=pcb_height,
                 space_above_pcb=space_above_pcb,

                 # TP Dimensions
                 tp_cap=tp_cap,
                 tp_stem_width=tp_stem_width,
                 tp_stem_height=tp_stem_height,
                 model='Green T430',

                 color=color,
                 align=align,
                 rotation=rotation,
                 mode=mode,
        )
