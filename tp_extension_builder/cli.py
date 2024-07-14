#!/usr/bin/env python

import typer

from pathlib import Path
from typing import Annotated, Optional

from tp_extension_builder.cli_helpers import (
    get_export_path,
    TrackPointModel,
    ExportFormat,
)

from tp_extension_builder.defines import (
    CHOC_SWITCH_MOUNTING_NOTCH_HEIGHT,
    CHOC_KEYCAP_HEIGHT,
    D_ADAPTER_HOLE_INCR,
    D_MOUNTING_DISTANCE,
    D_PCB_HEIGHT,
    D_ADAPTER_WIDTH_BELOW_PCB,
    D_ADAPTER_WIDTH_ABOVE_PCB,
    D_EXTENSION_WIDTH,
)


D_EXPORT_PATH = get_export_path(
    Path('tp_extension').with_suffix('.stl').name
)
D_EXPORT_PATH_STR = str(D_EXPORT_PATH)
D_EXPORT_PATH_KICAD = str(
    D_EXPORT_PATH.with_stem(f'{D_EXPORT_PATH.stem}_kicad')
)

#
# CLI Arguments
#

ArgTrackPointModel = Annotated[
    TrackPointModel,
    typer.Argument(
        metavar='trackpoint_model',
        show_choices=True,
        help='The TrackPoint model',
    )
]

OptExportPath = Annotated[
    Optional[str],
    typer.Option(
        '--export-path', '-e',
        help='The path where the 3D models should be exported to',
    )
]

OptExportFormat = Annotated[
    ExportFormat,
    typer.Option(
        '--export-format', '-f',
        help='The format for the export.',
    )
]

OptInteractive = Annotated[
    bool,
    typer.Option(
        '--interactive/--not-interactive', '-i',
        help=(
            "Don't export a file and instead display the model in VSCode OCP "
            "Viewer."
        )
    )
]

OptCapModel = Annotated[
    Optional[TrackPointModel],
    typer.Option(
        '--cap-model', '--cm',
        show_choices=True,
        help=(
            "Create the extension with a tip that fits a different TrackPoint "
            "model's red cap. For example, create an extension for the green "
            "T430 TrackPoint that would be used with the smaller T460S cap."
        ),
    )
]

OptDesiredCapHeight = Annotated[
    float,
    typer.Option(
        '--cap-height', '--ch',
        help=(
            "The height above the PCB where the top of the red cap should "
            "end up. This is NOT the total height of the extension, because "
            "the red cap adds a little bit of height and because a portion of "
            "the extension will be within or below the PCB. The default value "
            "is the keycap height for Khail Choc switches."
        ),
    )
]

OptAdapterHoleIncr = Annotated[
    float,
    typer.Option(
        '--adapter-hole-increase', '--hi',
        help=(
            'In 3D printing holes frequently end up being smaller than '
            'specified. This allows you to compensate for it by increasing '
            'the TrackPoint adapter hole.'
        ),
    )
]

OptMountingDistance = Annotated[
    float,
    typer.Option(
        '--mounting-distance', '--md',
        help=(
            'This allows you to specify how far below the PCB your TrackPoint '
            'is mounted. This refers to the bottom of the white TrackPoint '
            'stem. So if you mount the TrackPoint flush against the PCB, you '
            'would use 0.0 and if you mount it below the hotswap sockets, you '
            'would use 1.85 or 2.00.'
        ),
    )
]

OptPcbHeight = Annotated[
    float,
    typer.Option(
        '--pcb-height', '--ph',
        help=(
            'Adjust the thickness of your keyboard PCB to ensure the total '
            'height above the PCB is correct'
        ),
    )
]

OptSpaceAbovePCB = Annotated[
    float,
    typer.Option(
        '--space-above-pcb', '--sap',
        help=(
            'Specify how much space you have above PCB for the thicker '
            'part of the extension adapter. This is the space between the '
            'PCB and anything above it that might be in the way, such as '
            'a switch plate. On Khail Choc boards without a switch plate, '
            'you have 2.2mm until the switch plate notch, for example.'
        ),
    )
]

OptAdapterWidthBelowPCB = Annotated[
    float,
    typer.Option(
        '--width-below-pcb', '--wbp',
        help=(
            'Specify the max width (diameter) of the extension below and '
            'within the PCB. This should be slightly smaller than your '
            'TrackPoint PCB hole.'
        ),
    )
]

OptAdapterWidthAbovePCB = Annotated[
    float,
    typer.Option(
        '--width-above-pcb', '--wap',
        help=(
            'Specify the max width (diameter) of the extension above the '
            'PCB. This should be smaller than the space available between '
            'your switches. Keep in mind that the stagger of the keys can '
            'significantly affect the available space.'
        ),
    )
]

OptExtensionWidth = Annotated[
    float,
    typer.Option(
        '--width-extension', '--we',
        help=(
            'Specify the max width (diameter) of the extension between '
            'the adapter and the tip. This should be smaller than the '
            'distance between the switches at their widest point (plate '
            'notch) and smaller than the TrackPoint hole in your switch '
            'plate.'
        ),
    )
]

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    context_settings={
        'help_option_names': ['-h', '--help'],
    },
)


@app.command(
    help='Creates a trackpoint extension model for 3d printing.',
    no_args_is_help=True,
)
def build(trackpoint_model: ArgTrackPointModel,

          export_path: OptExportPath = D_EXPORT_PATH_STR,
          export_format: OptExportFormat = ExportFormat.stl,
          interactive: OptInteractive = False,
          adapter_hole_incr: OptAdapterHoleIncr = D_ADAPTER_HOLE_INCR,
          desired_cap_height: OptDesiredCapHeight = CHOC_KEYCAP_HEIGHT,
          tp_mounting_distance: OptMountingDistance = D_MOUNTING_DISTANCE,
          pcb_height: OptPcbHeight = D_PCB_HEIGHT,
          space_above_pcb: OptSpaceAbovePCB = (
              CHOC_SWITCH_MOUNTING_NOTCH_HEIGHT
          ),
          adapter_width_below_pcb: OptAdapterWidthBelowPCB = (
              D_ADAPTER_WIDTH_BELOW_PCB
          ),
          adapter_width_above_pcb: OptAdapterWidthAbovePCB = (
              D_ADAPTER_WIDTH_ABOVE_PCB
          ),
          extension_width: OptExtensionWidth = D_EXTENSION_WIDTH,
          tp_cap_model: OptCapModel = None,
          ) -> None:

    print('Generating extension...')
    tp_cap = None
    if tp_cap_model is not None:
        tp_cap = tp_cap_model.build_cap()

    tp_extension = trackpoint_model.build_extension(
                 adapter_hole_incr=adapter_hole_incr,
                 desired_cap_height=desired_cap_height,
                 tp_mounting_distance=tp_mounting_distance,
                 adapter_width_below_pcb=adapter_width_below_pcb,
                 adapter_width_above_pcb=adapter_width_above_pcb,
                 extension_width=extension_width,
                 pcb_height=pcb_height,
                 space_above_pcb=space_above_pcb,
                 tp_cap=tp_cap,
    )

    if interactive is False:
        if export_path is None:
            export_path = get_export_path(f'{trackpoint_model}')
        export_format.export(tp_extension, export_path)
    else:
        from ocp_vscode import show
        show(tp_extension, measure_tools=True)


if __name__ == "__main__":
    app()
