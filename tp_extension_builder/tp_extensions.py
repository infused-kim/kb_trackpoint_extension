import build123d as bd
import math

from typing import Union, List, Optional

from tp_extension_builder.tp_caps import (
    TrackPointCapBase,
    TrackPointCapRedT460S,
    TrackPointCapGreenT430,
)

from tp_extension_builder.utils import (
    get_bd_debug_objects,
    ALIGN_CENTER_BOTTOM,
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
                 label: str,
                 color: bd.Color = bd.Color('gray'),
                 rotation: bd.RotationLike = (0, 0, 0),
                 align: Union[
                     bd.Align,
                     tuple[bd.Align, bd.Align, bd.Align]
                 ] = ALIGN_CENTER_BOTTOM,
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
        self._adapter_hole_corner_distance = (
            math.sqrt(
                self._adapter_hole_width * self._adapter_hole_width
                + self._adapter_hole_width * self._adapter_hole_width
            ) / 2
        )
        self._adapter_wall_thickness_below_pcb = (
            self._adapter_width_below_pcb/2
            - self._adapter_hole_corner_distance
        )
        self._adapter_wall_thickness_above_pcb = (
            self._adapter_width_above_pcb/2
            - self._adapter_hole_corner_distance
        )
        self._adapter_wall_thickness_top = (
            self._adapter_height
            - self._adapter_hole_height
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
        self._above_pcb_height = (
            self._total_height
            - self._adapter_height_below_pcb
        )
        self._above_pcb_height_with_cap = (
            self._above_pcb_height
            + self._tp_cap.cap_extra_height
        )

        extension = self._build_extension()

        super().__init__(
            part=extension,
            rotation=rotation,
            align=bd.tuplify(align, 3),
            mode=mode,
        )

        self.label = label
        self.color = color

    @property
    def debug(self) -> List[bd.Shape]:
        '''
        Returns a list of build123d objects for debugging in ocp_viewer.
        '''
        return get_bd_debug_objects(self)

    def _build_extension(self,
                         align: Union[
                             bd.Align,
                             tuple[bd.Align, bd.Align, bd.Align]
                         ] = ALIGN_CENTER_BOTTOM,
                         ) -> bd.Shape:
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
                height=self._adapter_hole_height +  + self._adapter_hole_incr,
                mode=bd.Mode.SUBTRACT,
                align=ALIGN_CENTER_BOTTOM,
            )

        tp_extension = tp_extension.part

        return tp_extension


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
                 align: Union[
                     bd.Align,
                     tuple[bd.Align, bd.Align, bd.Align]
                 ] = ALIGN_CENTER_BOTTOM,
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
                 label='TrackPoint Extension - Red T460S',

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
                 align: Union[
                     bd.Align,
                     tuple[bd.Align, bd.Align, bd.Align]
                 ] = ALIGN_CENTER_BOTTOM,
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
                 label='TrackPoint Extension - T430',

                 color=color,
                 align=align,
                 rotation=rotation,
                 mode=mode,
        )
