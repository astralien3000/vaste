from setuptools import setup, find_packages


setup(
    name="vaste",
    version="0.1",
    description="Vue.js in python",
    author="Loïc Dauphin",
    author_email="astralien3000@yahoo.fr",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[
        "fastapi",
    ],
)
