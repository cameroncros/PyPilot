from setuptools import setup

setup(
    name='PyPilot',
    version='0.1',
    packages=['pypilot', 'pypilot.planner', 'pypilot.planner_test'],
    url='https://github.com/cameroncros/PyPilot/',
    license='MIT',
    author='cameron',
    author_email='cameroncros@gmail.com',
    description='Tool to plan flight plans.', install_requires=['cmd2', 'geopy']
)
