import importlib
import inspect
import typer

from enum import Enum
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Type,
    Annotated,
    Any,
    Optional,
    Union,
    Dict,
    List,
    Tuple,
)

if TYPE_CHECKING:
    # Importing these classes causes build123d to be imported, which is very
    # slow. So we only import it when it is needed and during type checking.
    from build123d import Shape
    from tp_extension_builder.tp_extensions import (
        TrackPointExtensionRedT460S,
        TrackPointExtensionGreenT430,
        TrackPointExtensionBlueX1Carbon,
    )
    from tp_extension_builder.tp_caps import (
        TrackPointCapRedT460S,
        TrackPointCapGreenT430,
        TrackPointCapBlueX1Carbon,
    )


#
# Selecting TPs and Caps
#


class TrackPointModel(str, Enum):
    red_t460s = 'red_t460s'
    green_t430 = 'green_t430'
    blue_x1_carbon = 'blue_x1_carbon'

    @property
    def build_extension(
        self,
    ) -> Union[
        Type['TrackPointExtensionRedT460S'],
        Type['TrackPointExtensionGreenT430'],
        Type['TrackPointExtensionBlueX1Carbon'],
    ]:
        # Importing these classes causes build123d to be imported, which is
        # very slow. So we do it only when it's actually needed.
        from tp_extension_builder.tp_extensions import (
            TrackPointExtensionRedT460S,
            TrackPointExtensionGreenT430,
            TrackPointExtensionBlueX1Carbon,
        )

        mapping = {
            TrackPointModel.red_t460s: TrackPointExtensionRedT460S,
            TrackPointModel.green_t430: TrackPointExtensionGreenT430,
            TrackPointModel.blue_x1_carbon: TrackPointExtensionBlueX1Carbon,
        }

        extension = mapping.get(self)
        if extension is None:
            raise ValueError(f'Cannot build extension for {self}')

        return extension

    @property
    def build_cap(
        self,
    ) -> Union[
        Type['TrackPointCapGreenT430'],
        Type['TrackPointCapRedT460S'],
        Type['TrackPointCapBlueX1Carbon'],
    ]:
        from tp_extension_builder.tp_caps import (
            TrackPointCapRedT460S,
            TrackPointCapGreenT430,
            TrackPointCapBlueX1Carbon,
        )

        mapping = {
            TrackPointModel.red_t460s: TrackPointCapRedT460S,
            TrackPointModel.green_t430: TrackPointCapGreenT430,
            TrackPointModel.blue_x1_carbon: TrackPointCapBlueX1Carbon,
        }

        cap = mapping.get(self)
        if cap is None:
            raise ValueError(f'Cannot build cap for {self}')
        return cap


class ExportFormat(str, Enum):
    step = 'step'
    stl = 'stl'

    def export(
        self,
        to_export: 'Shape',
        file_path: Union[str, Path],
        overwrite: bool = False,
    ) -> None:
        """
        Exports a shape using the selected format's build123d exporter
        function.
        """
        from build123d import (
            export_step,
            export_stl,
        )

        file_path = self.add_extension_to_path(file_path)

        print(f'Exporting to {file_path} ...')
        if file_path.exists() is True and overwrite is False:
            typer.confirm(
                'The file already exist. Do you want to overwrite it?',
                abort=True,
            )

        try:
            file_path.parent.mkdir(exist_ok=True, parents=True)
        except (PermissionError, OSError) as e:
            print(f'Could not create dir for export path: {e}')

        if self is ExportFormat.step:
            export_step(to_export, str(file_path))
        elif self is ExportFormat.stl:
            export_stl(to_export, str(file_path))
        else:
            raise ValueError(f'{self.value} is not a supported export format')

    def add_extension_to_path(self, file_path: Union[str, Path]) -> Path:
        """
        Replaces the file extension of a path with the extension for the
        selected type.
        """
        new_path = Path(file_path).with_suffix(f'.{self.value}')

        return new_path

    def substitute_file_path(
        self,
        file_path: Union[str, Path],
        extra_substitutions: Dict[str, str] = {},
        param_suffix_func_offset: int = 0,
        param_suffix_exclude_list: List[str] = [],
        include_only_non_default: bool = True,
    ) -> Path:
        """
        Makes the following replacements in the file path:
          - `<params>` / `<parameters>` to calling function's short parameter
            values
          - `<format>` to the selected format in this enum
          - The dict keys in extra_substitutions to the dict values
        """

        file_path_str = str(file_path)

        # Add additional, common parameters that should be excluded
        param_suffix_exclude_list.extend(
            [
                'export_path',
                'export_format',
                'export_overwrite',
                'interactive',
            ]
        )

        # Replace `<params>` with the parameters of the calling function

        # Increment func offset to get the parameters of the calling
        # function and not of this one
        param_suffix_func_offset += 1
        param_suffix = get_file_name_suffix_from_params(
            exclude_list=param_suffix_exclude_list,
            call_frame_offset=param_suffix_func_offset,
            include_only_non_default=include_only_non_default,
        )
        file_path_str = file_path_str.replace(
            '<params>',
            param_suffix,
        )
        file_path_str = file_path_str.replace(
            '<parameters>',
            param_suffix,
        )

        # Replace format with extension of selected format
        file_path_str = file_path_str.replace(
            '<format>',
            self.value,
        )

        # Do other replacements
        for search_val, replace_val in extra_substitutions.items():
            file_path_str = file_path_str.replace(
                search_val,
                replace_val,
            )

        new_file_path = Path(file_path_str)

        return new_file_path


#
# Get version
#


def get_package_version() -> Tuple[str, str]:
    """
    Returns the main package name and version string.
    """

    def get_package_name() -> str:
        frame = inspect.currentframe()
        try:
            if frame is None:
                raise RuntimeError('No frame found')

            f_globals = frame.f_back.f_globals if frame.f_back else None

            if not f_globals:
                raise RuntimeError('No global variables found')

            package_name = f_globals.get('__package__') or f_globals.get(
                '__name__'
            )

            if not package_name:
                raise RuntimeError('Could not determine package name')

            return package_name.split('.')[0]
        except Exception:
            pass
        finally:
            del frame

        raise RuntimeError('Could not determine package name')

    def get_package_version(package_name: str) -> str:
        try:
            version = importlib.metadata.version(package_name)
        except importlib.metadata.PackageNotFoundError:
            raise RuntimeError(f'{package_name!r} is not installed.') from None

        return version

    package_name = get_package_name()
    version = get_package_version(package_name=package_name)

    return (package_name, version)


def version_param_callback(value: bool):
    """
    To be used as the callback for the Typer.Option() version parameter.
    """
    if value:
        package_name, version = get_package_version()
        typer.echo(f'{package_name} - v{version}')
        raise typer.Exit()


def app_version_callback(
    _: Annotated[
        bool,
        typer.Option(
            '--version',
            '-v',
            help='Show the app version number.',
            callback=version_param_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """
    Allows you to add a --version / -v parameter to a typer app.

    Usage:
        app = typer.Typer()
        app.callback()(app_version_callback)
    """
    pass


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


def get_func_call_history_param_info(
    exclude_list: Optional[List[str]] = None,
    call_frame_offset: int = 0,
) -> Dict[str, Dict[str, Any]]:
    """
    Retrieves parameter information from the call history of functions.

    This function returns the parameter names, their annotations, and their
    values for a function that was called prior to this one, based on the
    specified call frame offset.

    Parameters:
    - exclude_list: Optional[List[str]]
        A list of parameter names to exclude from the results.
    - call_frame_offset: int
        The number of calls to look back in the call history. For example,
        0 refers to the previous function call, 1 refers to the call before
        that, and so on.

    Returns:
    - Dict[str, Dict[str, Any]]:
        A dictionary where each key is a parameter name and the value is
        another dictionary with the following keys:
        - 'value': The value passed to the parameter.
        - 'default': The default value of the parameter.
        - 'annotation': The type annotation of the parameter, or None if
          no annotation is present.

    Example usage:

    ```python
    def example_function(a: int, b: str, c: float = 3.0) -> None:
        info = get_func_call_history_param_info(call_frame_offset=0)
        print(info)


    # It will print the parameter info and values passed to
    # `example_function`.
    ```
    """

    if exclude_list is None:
        exclude_list = []

    # Always exclude self and cls for methods
    if 'self' not in exclude_list:
        exclude_list.append('self')
    if 'cls' not in exclude_list:
        exclude_list.append('cls')

    # Increment call_frame_offset to always skip the current frame.
    call_frame_offset += 1

    # Get the frame of X calls before the current function
    frame = inspect.currentframe()
    for _ in range(call_frame_offset):
        if frame is None:
            break
        else:
            frame = frame.f_back

    if frame is None:
        return {}

    func_name = frame.f_code.co_name

    # Get the function from the frame
    try:
        func = frame.f_globals[func_name]
    except KeyError:
        raise ValueError(
            f'Your call_frame_offset seems to be too high. Could not '
            f'retrieve parameters for function "{func_name}"'
        )

    # Get the function signature and annotations
    signature = inspect.signature(func)
    annotations = {
        param_name: (
            param.annotation
            if param.annotation != inspect.Parameter.empty
            else None
        )
        for param_name, param in signature.parameters.items()
    }

    defaults = {
        param_name: (
            param.default if param.default != inspect.Parameter.empty else None
        )
        for param_name, param in signature.parameters.items()
    }

    # Get the argument values and annotations from the frame
    args, _, _, values = inspect.getargvalues(frame)
    params = {
        arg: {
            'value': values[arg],
            'default': defaults.get(arg),
            'annotation': annotations.get(arg),
        }
        for arg in args
        if arg not in exclude_list
    }

    return params


def get_func_call_history_typer_names(
    exclude_list: Optional[List[str]] = None,
    call_frame_offset: int = 0,
) -> List[Tuple[List[str], Any, Any]]:
    """
    Retrieves Typer parameter names and their values from the call history
    of functions.

    This function returns a list of tuples containing parameter names
    (including aliases defined by Typer) and their values for a function
    that was called prior to this one, based on the specified call frame
    offset.

    Parameters:
    - exclude_list: Optional[List[str]]
        A list of parameter names to exclude from the results.
    - call_frame_offset: int
        The number of calls to look back in the call history. For example,
        0 refers to the previous function call, 1 refers to the call before
        that, and so on.

    Returns:
    - List[Tuple[List[str], Any, Any]]:
        A list of tuples, each containing:
        - A list of parameter names, including any aliases defined by Typer.
        - The value passed to the parameter.

    Example usage:
    def example_function(
            my_arg: Annotated[
                int,
                typer.Argument('--my-arg', '--ma')
            ] = 1,
            b: int = 2) -> None:
        info = get_func_call_history_typer_names(call_frame_offset=1)
        print(info)

    # When example_function(10, 20) is called, it will print:
    # [
    #    (['my_arg', 'my-arg', 'ma'], 10, 1),
    #    (['b'], 20, 2)
    # ]
    """

    def get_typer_info_from_annotation(
        annotation: Any,
    ) -> Optional[typer.models.ParameterInfo]:
        if hasattr(annotation, '__metadata__'):
            for a in annotation.__metadata__:
                if isinstance(a, typer.models.ParameterInfo):
                    return a

        return None

    # Increment call_frame offset to get info about previous func
    # and not this one.
    call_frame_offset += 1

    param_infos = get_func_call_history_param_info(
        exclude_list, call_frame_offset
    )

    param_names_and_values = []
    for param_name, param_info in param_infos.items():
        typer_info = get_typer_info_from_annotation(param_info['annotation'])

        all_names = [param_name]

        if typer_info is not None:
            # The main parameter name
            if typer_info.default is not None:
                all_names.append(typer_info.default)

            if typer_info.param_decls is not None:
                all_names.extend(typer_info.param_decls)

            all_names = [
                param.lstrip('-')
                for param in all_names
                if isinstance(param, str)
            ]

        param_names_and_values.append(
            (all_names, param_info['value'], param_info['default'])
        )

    return param_names_and_values


def get_file_name_suffix_from_params(
    exclude_list: Optional[List[str]] = None,
    param_max_len: int = 3,
    call_frame_offset: int = 0,
    include_only_non_default: bool = False,
) -> str:
    """
    Generates a file name suffix based on parameter values from the call
    history of previous functions.

    This function retrieves Typer parameter names and their values from the
    call history of functions that were called prior to this one, based on
    the specified call frame offset.

    It constructs a suffix for a file name by combining shortened parameter
    names with their corresponding values.

    Parameters:
    - exclude_list: Optional[List[str]]
        A list of parameter names to exclude from consideration when
        generating the suffix.
    - param_max_len: int
        Maximum length for a parameter name to be considered for shortening.
        Parameter names longer than this length will not be included in the
        suffix.
    - call_frame_offset: int
        The number of calls to look back in the call history. For example, 0
        refers to the previous function call, 1 refers to the call before
        that, and so on.
    - include_only_non_default: bool
        Only include parameters where the default value was changed.

    Returns:
    - str:
        A string representing the generated file name suffix, constructed by
        joining shortened parameter names with their corresponding values,
        separated by '-'.
    """

    # Increment call_frame offset to get info about previous func
    # and not this one.
    call_frame_offset += 1

    typer_infos = get_func_call_history_typer_names(
        exclude_list=exclude_list,
        call_frame_offset=call_frame_offset,
    )

    param_values = []
    for names, value, default in typer_infos:
        if isinstance(value, Enum):
            value = value.value

        if isinstance(default, Enum):
            default = default.value

        short_name = None
        for name in names:
            if len(name) <= param_max_len:
                short_name = name
                break

        if short_name is not None:
            if include_only_non_default is False or value != default:
                param_values.append(f'{short_name}-{value}')

    file_name_suffix = '_'.join(param_values)

    return file_name_suffix
