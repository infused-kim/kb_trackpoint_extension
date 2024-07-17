import platform
import sys

from setuptools import setup, find_packages


# build123d require cadquery_ocp, but it's currently not available for arm
# macOS on pypi. But it is available as a wheel on github. This function
# installs the correct version on Apple Silicon systems
def gen_cadquery_ocp_requirement(system=None, machine=None):
    if system is None:
        system = platform.system()
    if machine is None:
        machine = platform.machine()

    python_version = f'cp{sys.version_info.major}{sys.version_info.minor}'

    requirement_str = 'cadquery-ocp'
    if system == 'Darwin' and machine == 'arm64':
        requirement_str = f'cadquery-ocp @ https://github.com/CadQuery/ocp-build-system/releases/download/7.7.2.0/cadquery_ocp-7.7.2-{python_version}-{python_version}-macosx_11_0_arm64.whl'

    return requirement_str


setup(
    name='tp_extension_builder',
    version='1.1',
    packages=find_packages(),
    package_data={
        'tp_extension_builder': ['scripts/*'],
    },
    install_requires=[
        gen_cadquery_ocp_requirement(),
        'build123d',
        'ocp_vscode',
        'typer',
    ],
    extras_require={
        'dev': [
            'ruff',
            'mypy',
        ],
    },
    entry_points={
        'console_scripts': [
            'tp_extension_builder=tp_extension_builder.cli:app',
        ],
    },
)
