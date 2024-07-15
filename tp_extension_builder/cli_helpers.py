import typer
import os

from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Type, Union

if TYPE_CHECKING:
    # Importing these classes causes build123d to be imported, which is very
    # slow. So we only import it when it is needed and during type checking.
    from build123d import Shape
    from tp_extension_builder.tp_extensions import (
        TrackPointExtensionRedT460S,
        TrackPointExtensionGreenT430,
    )
    from tp_extension_builder.tp_caps import (
        TrackPointCapRedT460S,
        TrackPointCapGreenT430,
    )


#
# Selecting TPs and Caps
#

class TrackPointModel(str, Enum):
    tp_red_t460s = "tp_red_t460s"
    tp_green_t430 = "tp_green_t430"

    @property
    def build_extension(self) -> Union[
                                    Type['TrackPointExtensionRedT460S'],
                                    Type['TrackPointExtensionGreenT430'],
                                 ]:
        # Importing these classes causes build123d to be imported, which is
        # very slow. So we do it only when it's actually needed.
        from tp_extension_builder.tp_extensions import (
            TrackPointExtensionRedT460S,
            TrackPointExtensionGreenT430,
        )
        mapping = {
            TrackPointModel.tp_red_t460s: TrackPointExtensionRedT460S,
            TrackPointModel.tp_green_t430: TrackPointExtensionGreenT430,
        }

        extension = mapping.get(self)
        if extension is None:
            raise ValueError(f'Cannot build extension for {self}')

        return extension

    @property
    def build_cap(self) -> Union[
                                Type['TrackPointCapGreenT430'],
                                Type['TrackPointCapRedT460S'],
                           ]:
        from tp_extension_builder.tp_caps import (
            TrackPointCapRedT460S,
            TrackPointCapGreenT430,
        )
        mapping = {
            TrackPointModel.tp_red_t460s: TrackPointCapRedT460S,
            TrackPointModel.tp_green_t430: TrackPointCapGreenT430,
        }

        cap = mapping.get(self)
        if cap is None:
            raise ValueError(
                f'Cannot build cap for {self}'
            )
        return cap


class ExportFormat(str, Enum):
    step = "step"
    stl = "stl"

    def export(self,
               to_export: 'Shape',
               file_path: str,
               overwrite: bool = False) -> None:
        '''
        Exports a shape using the selected format's build123d exporter
        function.
        '''
        from build123d import (
            export_step,
            export_stl,
        )

        file_path = self.add_extension_to_path(file_path)

        print(f'Exporting to {file_path} ...')
        if os.path.exists(file_path) is True and overwrite is False:
            typer.confirm(
                'The file already exist. Do you want to overwrite it?',
                abort=True,
            )

        if self is ExportFormat.step:
            export_step(to_export, file_path)
        elif self is ExportFormat.stl:
            export_stl(to_export, file_path)
        else:
            raise ValueError(f'{self.value} is not a supported export format')

    def add_extension_to_path(self, file_path: str) -> str:
        '''
        Replaces the file extension of a path with the extension for the
        selected type.
        '''
        new_path = Path(file_path).with_suffix(f'.{self.value}')

        return str(new_path)


#
# Functions
#

def is_interactive_mode() -> bool:
    try:
        from IPython import get_ipython  # type: ignore
        if 'IPKernelApp' not in get_ipython().config:  # type: ignore
            return False
    except ImportError:
        return False
    except AttributeError:
        return False
    return True


def get_export_path(file_name: str) -> Path:
    current_dir_exports = Path('exports')
    parent_dir_exports = Path('../exports')

    if current_dir_exports.is_dir():
        return current_dir_exports / file_name
    elif parent_dir_exports.is_dir():
        return parent_dir_exports / file_name
    else:
        return Path(file_name)
