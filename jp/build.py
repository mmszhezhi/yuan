import re
import datetime
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import sys



def similarity(df, name):
    col = df[name]
    # t = df.drop(["time"], axis=1)
    # t.columns
    col.fillna(method="ffill", inplace=True)
    sims = df.values * col.values.reshape([-1, 1])
    t = pd.DataFrame(sims, columns=df.columns)
    t.fillna(method="ffill", inplace=True)
    similar = np.round(t.sum() / df.shape[0], 2)
    return similar
def simi_filter(tdata, cs, n=6):
    """
    :param tdata: normalized data
    :param cs: ordered by similarity
    :param n: max n
    :return:
    """
    index = cs.index
    # plt.scatter(x, tdata['CHR'], label="CHR")
    # plt.plot(x, tdata['CHR'])
    needed = []
    l = len(cs)
    for i, C in enumerate(cs[::]):
        if C > 0.83 or(len(needed)>5 and C>0.7) or (len(needed)>2 and C>0.6):
            needed.append(index[i])
    return tdata.loc[:, needed[::-1]], cs[needed]

def cut_data(df, n, quantity=0):
    try:
        start = re.sub(":\d\d:", ":00:", str(df.index[0]))
        bins = pd.date_range(start, df.index[-1], freq=f'{n}Min')
        dti = pd.DatetimeIndex([bins[-1] + datetime.timedelta(minutes=n)])
        bins = bins.append(dti)
        cats = pd.cut(pd.to_datetime(df.index), bins=bins, labels=bins[:-1], right=False)
        df["cats"] = cats
        df1 = df.groupby(["cats"]).apply(lambda i: i.iloc[-1] if len(i) > 0 else None)
        df1.fillna(method='bfill', inplace=True)
        df1.index = cats.categories
        df1.drop('cats', axis=1, inplace=True)

        return df1 if quantity == 0 else df1.tail(quantity)
    except Exception as e:
        df.to_csv("fuck.csv")
        print(df.head(5))
        print(df.tail(5))
        print(f"cut data {n}", start, df.index[-1])
        print(repr(e))

def smooth_mean(df3):
    try:
        if df3.shape[0]<10:
            return None, None, None
        df3.fillna(method="ffill", inplace=True)
        agg = df3.mean(axis=1)
        smooth = gaussian_filter1d(agg, sigma=1.5, axis=0)
        sm_grad = np.gradient(smooth, axis=0)
        infls = np.where(np.diff(np.sign(sm_grad), axis=0))
        if infls:
            # tend = bool(sum(sm_grad[-infls[-1][0]:]) > 0)
            tend = bool(smooth[-1] > smooth[infls[0][-1]])
            return smooth, infls[0], tend
        else:
            raise Exception("fuck")
    except Exception as e:
        print(f"smooth_mean  error")
        print(repr(e))
        return None, None, None

slides = [3,4,5,6,7,8,9,10]
crypto = "CHR"
result = []
data = pd.read_csv("data.csv",index_col=0)
# data = data.tail(3600)

slid = 5
length = 100
if len(sys.argv)>1:
    slid = sys.argv[-1]
    try:
        length = sys.argv[-2]
    except:
        pass


from tqdm import tqdm

for delta in tqdm([1,2,3,5,10,15,30,60,120,240,480,720,1440,4320]):
# for delta in [60]:
    tail = data.tail(delta*length)
    df = cut_data(tail,delta)
    # print(f"delta {delta}")
    # for slide in [3,4,5,6,7,8,9,10]:
    for slide in [3,4]:
        # print(f"slide {slide}")
        result = []
        for x in df.rolling(slide):
            if x.shape[0] < slide:
                continue
            scale = StandardScaler()
            t = scale.fit_transform(x)
            item = []
            tdata = pd.DataFrame(data=t, columns=df.columns[:])
            for c in df.columns:
                # print(f"crypt {c}")
                alice_similar = similarity(tdata, c)
                sortedsim = alice_similar.sort_values(ascending=False)
                fdf, cs = simi_filter(tdata, sortedsim, 9)
            #     print(cs)
                item.append(cs.shape[0])
            #     break
            result.append(item)

        support = pd.DataFrame(result,columns=df.columns)
        try:
            support.index = df.index[-support.shape[0]:]
            support.to_csv(f"sup_{delta}_{slide}.csv")
            support = None
        except Exception as e:
            print(repr(e))
            print(support.shape)

