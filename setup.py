from setuptools import setup

setup(
    name="masonite-foreman",
    version='0.0.2',
    # The project's main homepage.
    url='https://github.com/masoniteframework/foreman',
    py_modules=['foreman'],
    packages=[
        'foreman',
        'foreman.services',
        'foreman.drivers',
        'foreman.commands',
    ],
    install_requires = [
        "pyyaml",
        "cleo"
    ],
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Environment :: Web Environment',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        'Operating System :: MacOS',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: System :: Systems Administration',
    ],
    package_dir={'': 'src'},
    extras_require={
        'test': ['coverage', 'pytest'],
    },
    entry_points={
        'console_scripts': ['foreman=foreman.application:application.run'],
    },
    include_package_data=True
)
