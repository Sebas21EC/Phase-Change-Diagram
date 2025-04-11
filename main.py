from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from phase_data import phase_diagram_data

app = FastAPI()

@app.get("/phase-change-diagram")
async def get_phase_change_data(pressure: float = Query(..., gt=0)):
    if pressure in phase_diagram_data:
        return phase_diagram_data[pressure]
    return JSONResponse(
        status_code=404,
        content={"error": "Presión no encontrada en la tabla de saturación o fuera del rango permitido (0.05 a 10 MPa)."}
    )
