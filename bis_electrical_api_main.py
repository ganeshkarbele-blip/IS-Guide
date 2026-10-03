import math
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Indian Electrical Standards Calculation API",
    description="REST API for electrical design calculations based on IS 732, IS 3043, IS 1255, and BIS Codes.",
    version="1.0.0"
)

class BISElectricalCalculator:
    CONDUIT_SIZES_MMS = {
        16: 133.0,
        20: 224.0,
        25: 360.0,
        32: 607.0,
        40: 984.0,
        50: 1541.0,
        63: 2552.0
    }

    CABLE_AREAS_IS694 = {
        0.5: 4.15,
        0.75: 4.91,
        1.0: 5.73,
        1.5: 8.55,
        2.5: 12.57,
        4.0: 16.62,
        6.0: 21.24,
        10.0: 35.26,
        16.0: 47.78
    }

    @staticmethod
    def calculate_conduit_size(cables_dict: Dict[float, int], num_90_bends: int = 0):
        total_cable_area = 0.0
        total_cables_count = sum(cables_dict.values())

        for size_sqmm, qty in cables_dict.items():
            if size_sqmm not in BISElectricalCalculator.CABLE_AREAS_IS694:
                raise ValueError(f"Unsupported cable size: {size_sqmm} sqmm. Supported sizes: {list(BISElectricalCalculator.CABLE_AREAS_IS694.keys())}")
            total_cable_area += BISElectricalCalculator.CABLE_AREAS_IS694[size_sqmm] * qty

        if total_cables_count == 1:
            fill_factor = 0.53
        elif total_cables_count == 2:
            fill_factor = 0.31
        else:
            fill_factor = 0.40

        required_conduit_area = total_cable_area / fill_factor

        if num_90_bends >= 2:
            bend_derating = 0.85 ** (num_90_bends // 2)
        else:
            bend_derating = 1.0

        selected_conduit = None
        for size_mm, area_sqmm in sorted(BISElectricalCalculator.CONDUIT_SIZES_MMS.items()):
            effective_area = area_sqmm * bend_derating
            if effective_area >= required_conduit_area:
                selected_conduit = size_mm
                break

        return {
            "total_cables": total_cables_count,
            "total_cable_area_sqmm": round(total_cable_area, 2),
            "fill_factor_percentage": fill_factor * 100,
            "required_conduit_area_sqmm": round(required_conduit_area, 2),
            "bend_derating_factor": round(bend_derating, 2),
            "recommended_conduit_size_mm": selected_conduit,
            "standard_reference": "IS 732:2019 / IS 9537 Part 3"
        }

    @staticmethod
    def calculate_pipe_earth_resistance(soil_resistivity_ohm_m: float, pipe_length_m: float, pipe_diameter_m: float):
        L_cm = pipe_length_m * 100.0
        d_cm = pipe_diameter_m * 100.0

        R = (100.0 * soil_resistivity_ohm_m / (2.0 * math.pi * L_cm)) * math.log(4.0 * L_cm / d_cm)
        return {
            "soil_resistivity_ohm_m": soil_resistivity_ohm_m,
            "pipe_length_m": pipe_length_m,
            "pipe_diameter_mm": pipe_diameter_m * 1000,
            "calculated_earth_resistance_ohms": round(R, 3),
            "standard_reference": "IS 3043:2018 Section 2 (Clause 9)"
        }

    @staticmethod
    def calculate_plate_earth_resistance(soil_resistivity_ohm_m: float, plate_area_sqm: float):
        R = (soil_resistivity_ohm_m / 4.0) * math.sqrt(math.pi / plate_area_sqm)
        return {
            "soil_resistivity_ohm_m": soil_resistivity_ohm_m,
            "plate_area_sqm": plate_area_sqm,
            "calculated_earth_resistance_ohms": round(R, 3),
            "standard_reference": "IS 3043:2018 Section 2 (Clause 9)"
        }

    @staticmethod
    def calculate_derated_cable_current(base_current_amps: float, ambient_temp_c: int, harmonic_percentage: float = 0.0):
        temp_factors_pvc = {
            20: 1.12, 25: 1.06, 30: 1.00, 35: 0.94,
            40: 0.87, 45: 0.79, 50: 0.71, 55: 0.61
        }
        temp_factor = temp_factors_pvc.get(ambient_temp_c, 1.00)

        if harmonic_percentage <= 15:
            harmonic_factor = 1.0
        elif harmonic_percentage <= 33:
            harmonic_factor = 0.86
        else:
            harmonic_factor = 0.86

        derated_capacity = base_current_amps * temp_factor * harmonic_factor
        return {
            "base_current_amps": base_current_amps,
            "ambient_temp_c": ambient_temp_c,
            "temp_correction_factor": temp_factor,
            "harmonic_reduction_factor": harmonic_factor,
            "derated_safe_current_amps": round(derated_capacity, 2),
            "standard_reference": "IS 732:2019 Annex S / BIS Handbook Table 3"
        }

# Request Models
class ConduitRequest(BaseModel):
    cables: Dict[float, int] = Field(..., example={1.5: 5, 4.0: 2, 2.5: 2}, description="Map of cable size in sqmm to quantity")
    num_90_bends: int = Field(0, example=2, description="Number of 90-degree bends in the run")

class PipeEarthingRequest(BaseModel):
    soil_resistivity_ohm_m: float = Field(..., example=100.0, description="Soil resistivity in Ohm-meter")
    pipe_length_m: float = Field(2.5, example=2.5, description="Pipe length in meters")
    pipe_diameter_m: float = Field(0.050, example=0.050, description="Pipe outer diameter in meters (e.g. 0.050 for 50mm GI pipe)")

class PlateEarthingRequest(BaseModel):
    soil_resistivity_ohm_m: float = Field(..., example=100.0, description="Soil resistivity in Ohm-meter")
    plate_area_sqm: float = Field(0.36, example=0.36, description="Plate area in sq. meters (e.g. 0.6m x 0.6m = 0.36 sq.m)")

class CableDeratingRequest(BaseModel):
    base_current_amps: float = Field(..., example=32.0, description="Rated base current in Amperes")
    ambient_temp_c: int = Field(30, example=45, description="Ambient temperature in degrees Celsius")
    harmonic_percentage: float = Field(0.0, example=20.0, description="Harmonic distortion percentage")

# Endpoints
@app.get("/")
def health_check():
    return {
        "status": "online",
        "app": "Indian Electrical Standards & Compliance API",
        "version": "1.0.0",
        "standards_covered": ["IS 732:2019", "IS 3043:2018", "IS 1255", "IS 9537 Part 3"]
    }

@app.post("/api/v1/calculate/conduit")
def calculate_conduit(request: ConduitRequest):
    try:
        return BISElectricalCalculator.calculate_conduit_size(request.cables, request.num_90_bends)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/calculate/pipe-earthing")
def calculate_pipe_earthing(request: PipeEarthingRequest):
    return BISElectricalCalculator.calculate_pipe_earth_resistance(
        request.soil_resistivity_ohm_m,
        request.pipe_length_m,
        request.pipe_diameter_m
    )

@app.post("/api/v1/calculate/plate-earthing")
def calculate_plate_earthing(request: PlateEarthingRequest):
    return BISElectricalCalculator.calculate_plate_earth_resistance(
        request.soil_resistivity_ohm_m,
        request.plate_area_sqm
    )

@app.post("/api/v1/calculate/cable-derating")
def calculate_cable_derating(request: CableDeratingRequest):
    return BISElectricalCalculator.calculate_derated_cable_current(
        request.base_current_amps,
        request.ambient_temp_c,
        request.harmonic_percentage
    )
