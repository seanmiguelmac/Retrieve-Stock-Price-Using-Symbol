import requests
import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()
BASE_URL = "https://www.alphavantage.co/query"
API_KEY = "2IKO2WWAF5CTVM2X"

@app.get("/stock/{symbol}")
def get_stock_price(symbol: str):
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if "Global Quote" in data:
            price = float(data["Global Quote"]["05. price"])
            return {"symbol": symbol, "price": price}
        else:
            raise HTTPException(status_code=404, detail="Symbol not found")
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    
    print(f"Server running at: http://{host}:{port}")
    
    uvicorn.run(app, host=host, port=port)
