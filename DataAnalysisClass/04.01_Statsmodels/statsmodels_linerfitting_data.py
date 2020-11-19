import numpy as np
import pandas as pd
import statsmodels.api as sm

data = """
  x   y y_err
201 592    61
244 401    25
 47 583    38
287 402    15
203 495    21
 58 173    15
210 479    27
202 504    14
198 510    30
158 416    16
165 393    14
201 442    25
157 317    52
131 311    16
166 400    34
160 337    31
186 423    42
125 334    26
218 533    16
146 344    22
"""
try:
    # for Python 2.x
    from StringIO import StringIO
except ImportError:
    from io import StringIO

data = pd.read_csv(StringIO(data),
                   delim_whitespace=True).astype(float)
