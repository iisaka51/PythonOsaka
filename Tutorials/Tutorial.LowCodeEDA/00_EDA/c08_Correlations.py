# %matplotlib
import pandas as pd
from matplotlib import pyplot as plt
from palmerpenguins import load_penguins

df = load_penguins()

df.corr()
