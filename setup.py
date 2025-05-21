from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="Chest_CT_scan_detection_mlops",
    version="0.1.0",
    author="Hamed Makian",
    packages=find_packages(),
    install_requires=requirements,
)
