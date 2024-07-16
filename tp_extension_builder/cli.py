#!/usr/bin/env python

import typer

from pathlib import Path
from typing import Annotated, Optional, List, Union
from enum import Enum

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


app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    context_settings={
        'help_option_names': ['-h', '--help'],
    },
)


D_EXPORT_PATH = get_export_path(
    'tp_extension_<tp_model>_<parameters>.<format>'
)
D_EXPORT_PATH_KICAD = get_export_path(
    'tp_extension_kicad_<tp_model>_<parameters>.<format>'
)
D_EXPORT_PATH_COMBINED = get_export_path(
    'tp_extensions_combined.<format>'
)


def substitute_export_path(export_path: Union[str, Path],
                           tp_model: Union[TrackPointModel, str],
                           export_format: ExportFormat) -> Path:
    if isinstance(tp_model, Enum):
        tp_model = tp_model.value

    export_path = export_format.substitute_file_path(
        file_path=export_path,
        extra_substitutions={
            '<tp_model>': tp_model
        },
        param_suffix_exclude_list=[
            'trackpoint_model',
        ],
        param_suffix_func_offset=1,
    )

    return export_path


#
# Build Command
#

ArgTrackPointModel = Annotated[
    TrackPointModel,
    typer.Argument(
        show_choices=True,
        help='The TrackPoint model',
    )
]

OptExportPath = Annotated[
    Optional[Path],
    typer.Option(
        '--export-path', '-e',
        help='The path where the 3D models should be exported to',
    )
]

OptExportFormat = Annotated[
    Optional[ExportFormat],
    typer.Option(
        '--export-format', '-f',
        help='The format for the export.',
    )
]

OptExportOverwrite = Annotated[
    bool,
    typer.Option(
        '--overwrite/--ask-before-overwriting',
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


@app.command(
    help='Creates a trackpoint extension model for 3d printing.',
    no_args_is_help=True,
)
def build(trackpoint_model: ArgTrackPointModel,

          export_path: OptExportPath = D_EXPORT_PATH,
          export_format: OptExportFormat = ExportFormat.stl,
          export_overwrite: OptExportOverwrite = False,
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

    if export_path is None:
        export_path = D_EXPORT_PATH

    if export_format is None:
        export_format = ExportFormat.step

    export_path = substitute_export_path(
        export_path, trackpoint_model, export_format
    )

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

    print(f'\n{tp_extension.info}\n')

    if interactive is False:
        export_format.export(
            to_export=tp_extension,
            file_path=export_path,
            overwrite=export_overwrite,
        )
    else:
        from ocp_vscode import show
        print('Showing extension in VSCode OCP Viewer...')
        show(tp_extension, measure_tools=True)


#
# KiCad Model Command
#

OptIncludeCap = Annotated[
    bool,
    typer.Option(
        '--cap/--no-cap', '--c/--nc',
        help=(
            'Allows you to include or exclude the red TrackPoint cap.'
        )
    )
]


@app.command(
    help=(
        'Creates a 3D model of the extension and cap that can be used in '
        'KiCad. The model is positioned at the mounting distance.'
    ),
    no_args_is_help=True,
)
def build_kicad_model(
        trackpoint_model: ArgTrackPointModel,

        export_path: OptExportPath = D_EXPORT_PATH_KICAD,
        export_format: OptExportFormat = ExportFormat.step,
        export_overwrite: OptExportOverwrite = False,
        interactive: OptInteractive = False,
        include_cap: OptIncludeCap = True,
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

    if export_path is None:
        export_path = D_EXPORT_PATH_KICAD

    if export_format is None:
        export_format = ExportFormat.step

    export_path = substitute_export_path(
        export_path, trackpoint_model, export_format
    )

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

    kicad_model = tp_extension.for_kicad(include_cap=include_cap)

    print(f'\n{tp_extension.info}\n')

    if interactive is False:
        export_format.export(kicad_model, export_path, export_overwrite)
    else:
        from ocp_vscode import show
        print('Showing extension in VSCode OCP Viewer...')
        show(kicad_model, measure_tools=True)


#
# Combine Command
#

ArgCombineFileList = Annotated[
    List[str],
    typer.Argument(
        help='A list of files you want to combine.',
    )
]

OptCombineShapeDistance = Annotated[
    float,
    typer.Option(
        '--shape-distance', '--sd',
        help=(
            'Allows you to adjust how far the shapes are placed from '
            'each other.'
        ),
    )
]

OptAddSprue = Annotated[
    bool,
    typer.Option(
        '--add-sprue/--no-sprue', '--as/--ns',
        help=(
            'Allows you to add or remove the sprue connector.'
        )
    )
]

OptSprueRadius = Annotated[
    float,
    typer.Option(
        '--sprue-radius', '--sr',
        help=(
            'Allows you to adjust the radius of the sprue cylinder.'
        ),
    )
]

OptSprueOffsetX = Annotated[
    float,
    typer.Option(
        '--sprue-offset-x', '--sox',
        help=(
            'Allows you to move the sprue location to a different '
            'location on the X axis.'
        ),
    )
]

OptSprueOffsetY = Annotated[
    float,
    typer.Option(
        '--sprue-offset-y', '--soy',
        help=(
            'Allows you to move the sprue location to a different '
            'location on the Y axis.'
        ),
    )
]

OptSprueOffsetZ = Annotated[
    float,
    typer.Option(
        '--sprue-offset-z', '--soz',
        help=(
            'This allows you to move the sprue location to a different '
            'location on the Z axis.'
        ),
    )
]


@app.command(
    help=(
        'Combines multiple stl or step files into one (optionally) sprued '
        'file.'
    ),
    no_args_is_help=True,
)
def combine(files_to_combine: ArgCombineFileList,
            export_path: OptExportPath = D_EXPORT_PATH_COMBINED,
            export_format: OptExportFormat = None,
            export_overwrite: OptExportOverwrite = False,
            interactive: OptInteractive = False,
            shape_distance: OptCombineShapeDistance = 0.5,
            add_sprue: OptAddSprue = True,
            sprue_radius: OptSprueRadius = 0.75,
            sprue_offset_x: OptSprueOffsetX = 0.0,
            sprue_offset_y: OptSprueOffsetY = -0.1,
            sprue_offset_z: OptSprueOffsetZ = 0.0,
            ) -> None:

    file_pathes = [
        Path(file_path)
        for file_path in files_to_combine
    ]

    if export_format is None:
        if file_pathes[0].suffix == '.stl':
            export_format = ExportFormat.stl
        else:
            export_format = ExportFormat.step

    if export_path is None:
        export_path = D_EXPORT_PATH_COMBINED

    print(f'Combining {len(files_to_combine)} files...')
    import build123d as bd
    from tp_extension_builder.utils import combine_shapes
    shapes = []
    for file_path in file_pathes:
        if file_path.suffix in ['.step', '.stp']:
            shape = bd.import_step(str(file_path))
        elif file_path.suffix == '.stl':
            shape = bd.import_stl(str(file_path))
        else:
            raise ValueError(
                f'Files with suffix {file_path.suffix} are not supported.')
        shapes.append(shape)

    shapes_sprued = combine_shapes(
        shapes=shapes,
        distance=shape_distance,
        add_sprue=add_sprue,
        sprue_radius=sprue_radius,
        sprue_offset=bd.Vector(
            sprue_offset_x,
            sprue_offset_y,
            sprue_offset_z,
        )
    )

    if interactive is False:
        export_format.export(shapes_sprued, export_path, export_overwrite)
    else:
        from ocp_vscode import show
        print('Showing extension in VSCode OCP Viewer...')
        show(shapes_sprued, measure_tools=True)


if __name__ == "__main__":
    app()
