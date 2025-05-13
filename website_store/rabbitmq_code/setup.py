from setuptools import find_packages, setup

setup(
    name='rabbitmq_common_code',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "pika==1.3.2",
        "jsonschema==4.23.0",
        "jsonschema-specifications==2024.10.1"
    ]
)

