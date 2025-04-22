from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from phase_data import phase_diagram_data

app = FastAPI()

sorted_pressures = sorted(phase_diagram_data.keys())

def interpolate(pressure: float):
    # Punto crítico exacto
    if abs(pressure - 10.0) < 1e-6:
        return {
            "specific_volume_liquid": 0.0035,
            "specific_volume_vapor": 0.0035
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
                "specific_volume_liquid": vl,
                "specific_volume_vapor": vv
            }

@app.get("/phase-change-diagram")
async def get_phase_data(pressure: float = Query(..., gt=0)):
    if pressure <= 0.05 or pressure > 10.0:
        return JSONResponse(
            status_code=404,
            content={"error": "Presión fuera del rango válido (T > 30°C)"}
        )

    result = interpolate(pressure)
    if result is not None:
        return JSONResponse(content={
            "specific_volume_liquid": round(result["specific_volume_liquid"], 10),
            "specific_volume_vapor": round(result["specific_volume_vapor"], 10)
        })

    return JSONResponse(
        status_code=500,
        content={"error": "No se pudo interpolar la presión dada."}
    )
