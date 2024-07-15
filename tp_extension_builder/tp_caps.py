import build123d as bd

from typing import cast, List

from tp_extension_builder.utils import (
    get_bd_debug_objects,
    ALIGN_CENTER_TOP,
    ALIGN_CENTER_BOTTOM,
    AlignT,
)


DEFAULT_DOME_DOT_HEIGHT = 0.2
DEFAULT_DOME_DOT_RADIUS = 0.3
DEFAULT_DOME_DOT_SPACING = 0.85
DEFAULT_DOME_DOT_ROWS = [
    3,
    7,
    7,
    9,
    9,
    9,
    7,
    7,
    3,
]


class TrackPointCapBase(bd.BasePartObject):
    def __init__(
        self,
        total_height: float,
        base_height: float,
        base_diameter: float,
        dome_diameter: float,
        hole_length: float,
        hole_width: float,
        hole_depth: float,
        cap_adapter_width_decrease: float,
        cap_adapter_length_decrease: float,
        model: str,
        dome_dot_height: float = DEFAULT_DOME_DOT_HEIGHT,
        dome_dot_radius: float = DEFAULT_DOME_DOT_RADIUS,
        dome_dot_spacing: float = DEFAULT_DOME_DOT_SPACING,
        dome_dot_rows: list[int] = DEFAULT_DOME_DOT_ROWS,
        color: bd.Color = bd.Color('red'),
        rotation: bd.RotationLike = (0, 0, 0),
        align: AlignT = ALIGN_CENTER_BOTTOM,
        mode: bd.Mode = bd.Mode.ADD,
    ):
        context: bd.BuildPart = bd.BuildPart._get_context(self)
        bd.validate_inputs(context, self)

        self._debug: List[bd.Shape] = []

        self.total_height = total_height

        self.base_height = base_height
        self.base_diameter = base_diameter

        self.dome_height = total_height - base_height - dome_dot_height
        self.dome_diameter = dome_diameter

        self.dome_dot_height = dome_dot_height
        self.dome_dot_radius = dome_dot_radius
        self.dome_dot_spacing = dome_dot_spacing
        self.dome_dot_rows = dome_dot_rows

        self.hole_length = hole_length
        self.hole_width = hole_width
        self.hole_depth = hole_depth

        self.cap_adapter_width_decrease = cap_adapter_width_decrease
        self.cap_adapter_length_decrease = cap_adapter_length_decrease

        self.cap_adapter_width = (
            self.hole_width
            - self.cap_adapter_width_decrease
        )
        self.cap_adapter_length = (
            self.hole_length
            - self.cap_adapter_length_decrease
        )
        self.cap_adapter_height = self.hole_depth

        self.cap_extra_height = (
            self.total_height
            - self.hole_depth
        )

        self.model = model

        base_height_total = base_height + (self.dome_height / 2)

        with bd.BuildPart() as tp_cap:
            dome = self._build_dome(
                diameter=self.dome_diameter,
                height=self.dome_height,
                dot_height=self.dome_dot_height,
                dot_radius=self.dome_dot_radius,
                dot_spacing=self.dome_dot_spacing,
                dot_rows=self.dome_dot_rows,
            )
            bd.add(dome)
            base = self._build_base(base_diameter, base_height_total)
            bd.add(base, mode=bd.Mode.ADD)

            # Cut the adapter hole through both the top and bottom
            with bd.Locations((0, 0, -base_height_total)):
                bd.Box(
                    length=self.hole_length,
                    width=self.hole_width,
                    height=self.hole_depth,
                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                    mode=bd.Mode.SUBTRACT,
                )
        tp_cap = tp_cap.part

        super().__init__(
            part=tp_cap,
            rotation=rotation,
            align=bd.tuplify(align, 3),
            mode=mode,
        )

        self.label = f'TP Cap - {self.model}'
        self.color = color

    @property
    def debug(self) -> List[bd.Shape]:
        '''
        Returns a list of build123d objects for debugging in ocp_viewer.
        '''
        return get_bd_debug_objects(self)

    def build_cap_adapter(self,
                          align: AlignT = ALIGN_CENTER_BOTTOM,) -> bd.Shape:
        with bd.BuildPart() as cap_adapter:
            bd.Box(
                length=self.cap_adapter_length,
                width=self.cap_adapter_width,
                height=self.cap_adapter_height,
                align=align,
            )
        cap_adapter = cap_adapter.part
        cap_adapter.label = 'Cap Adapter'

        return cast(bd.Shape, cap_adapter)

    def _build_dome(self,
                    diameter: float,
                    height: float,
                    dot_height: float = DEFAULT_DOME_DOT_HEIGHT,
                    dot_radius: float = DEFAULT_DOME_DOT_RADIUS,
                    dot_spacing: float = DEFAULT_DOME_DOT_SPACING,
                    dot_rows: List[int] = DEFAULT_DOME_DOT_ROWS,
                    ) -> bd.Shape:
        radius = diameter / 2

        with bd.BuildPart() as dome:

            # This is not the actual curvature of the TP dome, but
            # it's close enough.
            with bd.BuildSketch(bd.Plane.XZ) as dome_sketch:
                with bd.BuildLine():

                    # Draw the top half of the profile on the right side
                    l_side = bd.Line((0, 0), (0, height/2))
                    l_bottom = bd.Line(l_side@0, (radius, 0))
                    l_top = bd.Line(l_side@1, (radius * 0.4, height/2))

                    # Create the arc between top end and bottom end of the line
                    arc_mid_point = (
                        (l_top.end_point().X + l_bottom.end_point().X)/2,
                        (l_top.end_point().Y + l_bottom.end_point().Y)/2 * 1.5,
                    )
                    bd.ThreePointArc(
                        l_top@1,
                        arc_mid_point,
                        l_bottom@1
                    )

                bd.make_face()

                # Mirrow it down around the XZ plane
                bd.mirror(about=bd.Plane.XZ)

            dome_sketch = dome_sketch.sketch
            dome_sketch.label = 'Dome Sketch'
            self._debug = [dome_sketch]

            # Create the 3D shape by revolving
            bd.revolve(axis=bd.Axis.Z)

            # Dome Dots
            with bd.BuildSketch(bd.Plane.XY):
                for row_num, dot_num in enumerate(dot_rows):
                    row_offset = (
                        row_num * dot_spacing -
                        ((len(dot_rows) - 1) * dot_spacing) / 2
                    )
                    with bd.Locations((0, row_offset, 0)):
                        grid_loc = bd.GridLocations(
                            dot_spacing, dot_spacing, dot_num, 1
                        )
                        with grid_loc:
                            bd.Circle(
                                dot_radius,
                            )
            bd.extrude(amount=height/2 + dot_height)
        dome = dome.part
        dome.label = 'Cap Dome'

        return cast(bd.Shape, dome)

    def _build_base(self,
                    diameter: float,
                    height: float,
                    align: AlignT = ALIGN_CENTER_TOP) -> bd.Shape:
        radius = diameter / 2

        with bd.BuildPart() as base:
            bd.Cylinder(
                radius=radius,
                height=height,
                align=align,
            )
        base = base.part
        base.label = 'Cap Base'

        return cast(bd.Shape, base)


class TrackPointCapRedT460S(TrackPointCapBase):
    def __init__(self,
                 rotation: bd.RotationLike = (0, 0, 0),
                 align: AlignT = ALIGN_CENTER_BOTTOM,
                 mode: bd.Mode = bd.Mode.ADD):

        super().__init__(
            total_height=4.0,
            base_height=2.0,
            base_diameter=6.5,
            dome_diameter=8.5,

            hole_width=2.5,
            hole_length=2.5,
            hole_depth=3.0,

            # Since the inside of the cap is rubber, we don't decrease the
            # adapter size for a tighter fit
            cap_adapter_length_decrease=0.0,
            cap_adapter_width_decrease=0.0,

            model='Green T460S',
            rotation=rotation,
            align=bd.tuplify(align, 3),
            mode=mode,
        )


class TrackPointCapGreenT430(TrackPointCapBase):
    def __init__(self,
                 rotation: bd.RotationLike = (0, 0, 0),
                 align: AlignT = ALIGN_CENTER_BOTTOM,
                 mode: bd.Mode = bd.Mode.ADD):

        super().__init__(
            total_height=6.2,
            base_height=4.5,
            base_diameter=6.8,
            dome_diameter=8.0,
            hole_width=2.3,
            hole_length=2.3,
            hole_depth=5.3,

            # Since the inside of the cap is hard plastic and not rubber, we
            # decrease the tip width to make it fit better
            cap_adapter_length_decrease=0.2,
            cap_adapter_width_decrease=0.2,

            model='Green T430',
            rotation=rotation,
            align=bd.tuplify(align, 3),
            mode=mode,
        )
