from setuptools import setup

setup(
    name='xblock-pc2judge',
    version='0.1',
    description='Pc2Judge XBlock Tutorial Sample',
    py_modules=['pc2judge'],
    install_requires=['XBlock', 'requests'],
    entry_points={
        'xblock.v1': [
            'pc2judge = pc2judge:Pc2JudgeBlock',
        ]
    }
)
