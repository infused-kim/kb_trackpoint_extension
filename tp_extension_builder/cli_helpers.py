from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    # Importing these classes causes build123d to be imported, which is very
    # slow. So we only import it when it is needed and during type checking.
    from build123d import Shape, export_step, export_stl
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
                                    'TrackPointExtensionRedT460S',
                                    'TrackPointExtensionGreenT430',
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
        return mapping.get(self)

    @property
    def build_cap(self) -> Union[
                                'TrackPointCapRedT460S',
                                'TrackPointCapGreenT430',
                           ]:
        from tp_extension_builder.tp_caps import (
            TrackPointCapRedT460S,
            TrackPointCapGreenT430,
        )
        mapping = {
            TrackPointModel.tp_red_t460s: TrackPointCapRedT460S,
            TrackPointModel.tp_green_t430: TrackPointCapGreenT430,
        }
        return mapping.get(self)


class ExportFormat(str, Enum):
    step = "step"
    stl = "stl"

    def export(self, to_export: 'Shape', file_path: str) -> None:
        '''
        Exports a shape using the selected format's build123d exporter
        function.
        '''
        file_path = self.add_extension_to_path(file_path)

        print(f'Exporting to {file_path} ...')

        self._bd_export_func(to_export, file_path)

    def add_extension_to_path(self, file_path: str) -> str:
        '''
        Replaces the file extension of a path with the extension for the
        selected type.
        '''
        new_path = Path(file_path)
        new_path.with_suffix(f'.{self}')

    @property
    def _bd_export_func(self) -> Union['export_step', 'export_stl']:
        '''
        Returns the build123d export function for the selected format.
        '''
        from build123d import (
            export_step,
            export_stl,
        )
        mapping = {
            ExportFormat.step: export_step,
            ExportFormat.stl: export_stl,
        }
        return mapping.get(self)


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
