import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse,JSONResponse
import uvicorn
import json


app = FastAPI()

# Root function
@app.get("/")
async def root():
    html_content = """
    <html>
        <head>
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                h1 {
                    font-size: 48px;
                    color: #333;
                }
            </style>
        </head>
        <body>
            <h1>Api Made By D</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Get property details for old bill
@app.get("/fetch-water-bill/old-bill/")
async def fetch_old_water_bill(zone: str, ward: str, bill: str, sub: str, total: bool = False, rhtml: bool = False):
    url = "https://bnc.chennaimetrowater.in/svr/bnc-ms.php?getCustomer=true"

    # JSON payload
    payload = {
        "old_zone_no": zone,
        "old_ward_no": ward,
        "old_bill_no": bill,
        "old_sub_code": sub,
        "include_total_dues": total
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)

    if response.status_code == 200:
        if rhtml:
            # Return the raw HTML inside a response if rhtml is True
            return HTMLResponse(content=response.text)
        else:
            # Return the raw HTML inside a JSON object if rhtml is False
            return JSONResponse(content={"html": response.text})
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch details")

# Get property details for new bill
@app.get("/fetch-water-bill/new-bill/")
async def fetch_new_water_bill(zone: str, ward: str, bill: str, total: bool = False, rhtml: bool = False):
    url = "https://bnc.chennaimetrowater.in/svr/bnc-ms.php?getCustomer=true"

    # JSON payload
    payload = {
        "zone_no": zone,
        "ward_no": ward,
        "bill_no": bill,
        "include_total_dues": total
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)

    if response.status_code == 200:
        if rhtml:
            # Return the raw HTML inside a response if rhtml is True
            return HTMLResponse(content=response.text)
        else:
            # Return the raw HTML inside a JSON object if rhtml is False
            return JSONResponse(content={"html": response.text})
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch details")
