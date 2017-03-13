from setuptools import setup

setup(
    name='domi',
    version='0.1',
    py_modules=['domi'],
    include_package_data=True,
    install_requires=[
        'click==6.7',
    ],
    entry_points='''
        [console_scripts]
        domi=domi:cli
    ''',
)