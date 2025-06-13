import plotting_helper as plth
import numpy as np
from matplotlib import pyplot as plt
import yaml
import pathlib

path = pathlib.Path(__file__).parent.resolve()
data = yaml.safe_load(open("sediment_resules.yml"))