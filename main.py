from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from phase_data import phase_diagram_data

app = FastAPI()

sorted_pressures = sorted(phase_diagram_data.keys())

def interpolate(pressure: float):
    if pressure < sorted_pressures[0] or pressure > sorted_pressures[-1]:
        return None

    if pressure in phase_diagram_data:
        data = phase_diagram_data[pressure]
        return {
            "specific_volume_liquid": round(data["specific_volume_liquid"], 4),
            "specific_volume_vapor": round(data["specific_volume_vapor"], 4)
        }

    for i in range(len(sorted_pressures) - 1):
        p1 = sorted_pressures[i]
        p2 = sorted_pressures[i + 1]
        if p1 < pressure < p2:
            v1 = phase_diagram_data[p1]
            v2 = phase_diagram_data[p2]
            vl = v1["specific_volume_liquid"] + (pressure - p1) * (v2["specific_volume_liquid"] - v1["specific_volume_liquid"]) / (p2 - p1)
            vv = v1["specific_volume_vapor"] + (pressure - p1) * (v2["specific_volume_vapor"] - v1["specific_volume_vapor"]) / (p2 - p1)
            return {
                "specific_volume_liquid": round(vl, 4),
                "specific_volume_vapor": round(vv, 4)
            }

@app.get("/phase-change-diagram")
async def get_phase_data(pressure: float = Query(..., gt=0)):
    result = interpolate(pressure)
    if result:
        return result
    return JSONResponse(
        status_code=404,
        content={"error": "Presión fuera del rango válido (0.05 a 10.0 MPa)"}
    )
