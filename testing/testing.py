#!/usr/bin/env python3

# %% Init
import build123d as bd
import ocp_vscode as ocp
from tp_extension_builder.tp_caps import (
    TrackPointCapRedT460S,
    TrackPointCapGreenT430,
)

from tp_extension_builder.tp_extensions import (
    TrackPointExtensionRedT460S,
)

from tp_extension_builder.utils import (
    ALIGN_CENTER,
    ALIGN_CENTER_BOTTOM,
    ALIGN_CENTER_TOP,
)

# %% Preview Cap T460S

cap = TrackPointCapRedT460S()
adapter = cap.build_cap_adapter()
ocp.show(cap, adapter, cap.debug, measure_tools=True)

# %% Preview Cap T430

align = ALIGN_CENTER
cap = TrackPointCapGreenT430(
    align=align,
)
adapter = cap.build_cap_adapter(
    align=align,
)
ocp.show(cap, adapter, cap.debug, measure_tools=False)

# %% Preview Extension T460S

extension = TrackPointExtensionRedT460S(
    desired_cap_height=10.5,
    tp_mounting_distance=-2.0,
    adapter_hole_incr=0.0,
    align=ALIGN_CENTER_BOTTOM,
    rotation=(0, 0, 45),
)

ocp.show(extension, measure_tools=True)

# %%
