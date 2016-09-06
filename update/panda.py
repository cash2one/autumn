import pandas as pd
import numpy as np

s = pd.Series(range(5), index=['a', 'b', 'c', 'd', 'e'])
print s['c']
print s[-2]
print s.median()
print 3 in s
print 'e' in s

print s + s
