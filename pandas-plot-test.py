#!/usr/bin/env python

import pandas as pd
import numpy as np

print "--- Test Plot ---"
ts = pd.Series(np.random.randn(1000),
               index=pd.date_range('1/1/1995',
               periods=1000))
ts = ts.cumsum()
ts.plot()