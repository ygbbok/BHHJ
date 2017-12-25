import pandas as pd

# create a dataframe place holder
df = pd.DataFrame(columns = ['a','b','c','d','e'])


# insert values
df.loc[0] = [1,2,3,4,5]
df.loc[1] = [1,2,3,4,5]
df.loc[2] = [1,2,3,4,5]
df.loc[3] = [1,2,3,4,5]
df.loc[4] = [1,2,3,4,5]

print df

'''
   a  b  c  d  e
0  1  2  3  4  5
1  1  2  3  4  5
2  1  2  3  4  5
3  1  2  3  4  5
4  1  2  3  4  5
'''