
import openpyxl
import pandas as pd



def readdfs():
    dfs = pd.read_excel("energy2.xlsx", index_col=0, sheet_name=None)
    return dfs



dfs = readdfs()
sheets = dfs.keys()


def getfactor():
    factor = pd.read_excel("factor.xlsx")
    factor = factor.T
    factor.columns= factor.iloc[0]


    return factor

factor = getfactor()

def process(df):
    df.fillna(0,inplace=True)
    cols = df.iloc[0]
    cols[1] = "groupid"
    df.columns = cols
    df = df.groupby(by="groupid").sum()
    # df = df.reset_index()
    df = df.reset_index(drop=True)

    df.drop(columns=[0],inplace=True)
    df.drop(index=[0],inplace=True)
    f1 = factor[df.columns].loc["排放因子", :]
    f2 = factor[df.columns].loc["transfactor", :]
    return df*f1*f2

with pd.ExcelWriter("pm_by_industry.xlsx") as writer:
    for s in sheets:
        df = dfs.get(s)
        result = process(df)
        result.to_excel(writer,sheet_name=s)

















