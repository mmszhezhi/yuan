import  pandas as pd
data = pd.read_excel("pm.xls")
for x in data[["行政区名称","PM2.5"]].groupby(by=['行政区名称']):
    print(x)