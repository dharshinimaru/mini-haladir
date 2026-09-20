from fastapi import FastAPI

app = FastAPI()

wms = {
    "order_id": 101,
    "inventory_available": True,
    "picker_available": True,
    "dock_available": False,
    "current_dock": None
}

tms = {
    "order_id": 101,
    "truck_id": "TRUCK-7",
    "truck_leaves_in_min": 20
}

oms = {
    "order_id": 101,
    "priority": "high",
    "status": "READY"
}


@app.get("/wms")
def get_wms():
    return wms


@app.get("/tms")
def get_tms():
    return tms


@app.get("/oms")
def get_oms():
    return oms


@app.post("/wms/move-dock")
def move_dock():
    wms["current_dock"] = 4
    wms["dock_available"] = True
    return wms


@app.post("/oms/ready-to-ship")
def ready_to_ship():
    oms["status"] = "READY_TO_SHIP"
    return oms