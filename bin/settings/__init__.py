import os
from configparser import ConfigParser, ExtendedInterpolation

configsPath = os.path.realpath(__file__).rstrip("/__init__.py")

config = ConfigParser(interpolation = ExtendedInterpolation())
config.read(os.path.join(configsPath, "config.ini"))
