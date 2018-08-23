from setuptools import setup

setup(
    name='kubeb',
    version='0.0.1',
    packages=['kubeb'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        kubeb=cli:cli
    ''',
)
