import requests
import numpy as np
import urllib.parse
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from math import ceil


def getitem(item_name="CS:GO Weapon Case"):
    url = f"http://127.0.0.1:8002/marketplace/730?item=" \
          f"{urllib.parse.quote_plus(item_name)}" \
          f"&fill=true&unquote=true"
    r = requests.get(url)
    print(item_name)
    assert (r.status_code == 200)
    vals = [x["value"] for x in r.json()]
    return np.asarray(vals)


def getdata(items=[("★ M9 Bayonet | Fade (Factory New)", "Knife")], lookback=60, split=0.8, lookahead=30):
    timeinputs = []
    idxinputs = []
    typeinputs = []
    totidxinputs = []
    y = []
    for item in items:
        item, type_ = item
        v = getitem(item)
        for i in range(lookback, len(v)+1-lookahead):
            timeinputs.append(v[i - lookback:i])
            idxinputs.append(i)
            typeinputs.append(type_)
            totidxinputs.append(len(v))
            y.append(v[i+lookahead-1])
    timeinputs = np.asarray(timeinputs)
    idxinputs = np.asarray(idxinputs)
    typeinputs = np.asarray(typeinputs)
    totidxinputs = np.asarray(totidxinputs)
    y = np.asarray(y)
    y = y.reshape(y.shape[0], 1)
    # scaler = MinMaxScaler(feature_range=(0,1))
    # timeinputs = scaler.fit_transform(timeinputs.reshape(-1,lookback)).reshape(-1,lookback, 1)
    timeinputs = timeinputs.reshape(-1, lookback, 1)

    # perform split ♥

    timeinputstrain, timeinputstest, idxinputstrain, idxinputstest, typeinputstrain, typeinputstest, totidxinputstrain, totidxinputstest, ytrain, ytest = train_test_split(
        timeinputs, idxinputs, typeinputs, totidxinputs, y, train_size=split)

    xtrain = [timeinputstrain, idxinputstrain, typeinputstrain, totidxinputstrain]
    xtest = [timeinputstest, idxinputstest, typeinputstest, totidxinputstest]

    print(
        f"{timeinputstrain.shape=}\n{idxinputstrain.shape=}\n{typeinputstrain.shape=}\n{totidxinputstrain.shape=}\n{ytrain.shape=}\n{timeinputstest.shape=}\n{idxinputstest.shape=}\n{typeinputstest.shape=}\n{totidxinputstest.shape=}\n{ytest.shape=}")
    return xtrain, ytrain, xtest, ytest
