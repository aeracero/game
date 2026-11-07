from setuptools import setup, find_packages

setup(
    name="starfall-pocket",
    version="3.0.0",
    description="A pocket card-pack opening game with Gmail card abilities, written entirely in Python",
    packages=find_packages(exclude=["examples"]),
    package_data={"starfall_pocket": ["assets/*/*", "assets/*/*/*"]},
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=["pygame-ce>=2.5.6", "Pillow>=9.0", "certifi", "pillow-heif"],
    entry_points={"console_scripts": ["starfall-pocket=starfall_pocket.main:run"]},
)
