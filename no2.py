
import openpyxl
import pandas as pd



def readdfs():
    dfs = pd.read_excel("no2.xlsx", sheet_name=None)
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


def process2(df):
    if df["二氧化氮"].dtype != float:
        df["二氧化氮"] = df["二氧化氮"].astype(str)
        df["二氧化氮"].str.isdigit()
        df = df[df["二氧化氮"].str.isdigit()]
        df["二氧化氮"] = df["二氧化氮"].astype(float)
    no2_per_y = df.groupby(by=["行政区名称"])["二氧化氮"].mean()
    return no2_per_y


def process3(df):
    if df["二氧化氮"].dtype != float:
        df["二氧化氮"] = df["二氧化氮"].astype(str)
        df["二氧化氮"].str.isdigit()
        df = df[df["二氧化氮"].str.isdigit()]
        df["二氧化氮"] = df["二氧化氮"].astype(float)
    df["监测时间"] = df["监测时间"].apply(lambda x: x[:-3])
    no2_per_m = df.groupby(by=["行政区名称", "监测时间"])["二氧化氮"].mean()
    # no2_per_y = df.groupby(by=["行政区名称"])["二氧化氮"].mean()
    return no2_per_m



with pd.ExcelWriter("no2_per_m.xlsx") as writer:
    for s in sheets:
        df = dfs.get(s)
        result = process3(df)
        result.to_excel(writer,sheet_name=s)
        print(s)

















