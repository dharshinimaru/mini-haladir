import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8765"

wms = requests.get(f"{BASE_URL}/wms").json()
tms = requests.get(f"{BASE_URL}/tms").json()
oms = requests.get(f"{BASE_URL}/oms").json()

state = {
    "order_id": oms["order_id"],
    "priority": oms["priority"],
    "order_status": oms["status"],
    "inventory_available": wms["inventory_available"],
    "picker_available": wms["picker_available"],
    "dock_available": wms["dock_available"],
    "current_dock": wms["current_dock"],
    "truck_id": tms["truck_id"],
    "truck_leaves_in_min": tms["truck_leaves_in_min"]
}


def make_decision(state):
    if not state["inventory_available"]:
        return "WAIT - INVENTORY NOT AVAILABLE"

    if not state["picker_available"]:
        return "WAIT - NO PICKER AVAILABLE"

    if state["priority"] == "high" and state["truck_leaves_in_min"] < 30:
        if not state["dock_available"]:
            return "MOVE TO ANOTHER DOCK"

        return "SHIP NOW"

    return "WAIT"


decision = make_decision(state)

st.title("Mini Haladir")

st.write("Order:", state["order_id"])
st.write("Priority:", state["priority"])
st.write("Order status:", state["order_status"])
st.write("Truck:", state["truck_id"])
st.write("Truck leaves in:", state["truck_leaves_in_min"], "minutes")
st.write("Inventory available:", state["inventory_available"])
st.write("Picker available:", state["picker_available"])
st.write("Dock available:", state["dock_available"])
st.write("Current dock:", state["current_dock"])

st.subheader("Recommendation")
st.write(decision)

if st.button("Approve"):
    if decision == "MOVE TO ANOTHER DOCK":
        requests.post(f"{BASE_URL}/wms/move-dock")
        st.success("Order moved to an available dock")

    elif decision == "SHIP NOW":
        requests.post(f"{BASE_URL}/oms/ready-to-ship")
        st.success("Order marked ready to ship")

    else:
        st.info("No action executed")

    st.rerun()
