from setuptools import setup

setup(
    name='configuration-sos',
    version='0.0.1',
    install_requires=[
        'requests',
        'importlib-metadata; python_version<"3.12"',
    ],
)
