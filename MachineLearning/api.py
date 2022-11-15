from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
import RNNPrediction
import aiohttp
import urllib.parse
import numpy as np
import uvicorn

model = RNNPrediction.loadmodel()
lookback = RNNPrediction.lookback


async def inference(request: Request):
    json = await request.json()
    type_ = json["type"]
    name = json["name"]
    url = f"http://127.0.0.1:8002/marketplace/730?item=" \
          f"{urllib.parse.quote_plus(name)}" \
          f"&fill=true&unquote=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            v = await response.json()

    timeinputs = v[len(v) - 1 - lookback:len(v) - 1]
    idxinputs = [len(v) - 1]
    typeinputs = [type_]
    totidxinputs = [len(v)]

    timeinputs = np.asarray([x["value"] for x in timeinputs])
    idxinputs = np.asarray(idxinputs).reshape(1, 1)
    typeinputs = np.asarray(typeinputs).reshape(1, 1)
    totidxinputs = np.asarray(totidxinputs).reshape(1, 1)

    timeinputs = timeinputs.reshape(-1, lookback, 1)
    # print(timeinputs)
    # print(idxinputs)
    # print(typeinputs)
    # print(totidxinputs)
    v = np.asarray(model([timeinputs, idxinputs, typeinputs, totidxinputs]))
    # print(v)
    return JSONResponse({"output": float(v[0][0])})


async def reload(request):
    global model
    model = RNNPrediction.loadmodel()
    return JSONResponse({":)": ":)"})


routes = [
    Route("/", inference, methods=["POSt"]),
    Route("/reload", reload, methods=["GET"])
]
app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    uvicorn.run("api:app", port=80, log_level="trace", reload=True)
