from setuptools import setup

setup(
    name="masonite-foreman",
    version='0.0.1',
    py_modules=['foreman'],
    packages=[
        'foreman',
        'foreman.services',
        'foreman.drivers',
        'foreman.commands',
    ],
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': ['foreman=foreman.application:application.run'],
    },
    include_package_data=True,
    package_data= {
        'foreman': [
            'stubs/*'
        ]
    }
)
