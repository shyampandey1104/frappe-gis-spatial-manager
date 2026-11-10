"""FastAPI endpoints & Frappe Whitelist handlers for Spatial Manager."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from spatial_manager.engine import SpatialEngine

app = FastAPI(
    title="Frappe GIS & Spatial Manager API",
    description="Geospatial computation engine for ERPNext Land & Property Assets.",
    version="1.0.0",
)

engine = SpatialEngine()


class OverlapCheckRequest(BaseModel):
    subject_geometry: Dict[str, Any]
    reservation_geometry: Dict[str, Any]


class AreaCalcRequest(BaseModel):
    geometry: Dict[str, Any]


class PointQueryRequest(BaseModel):
    latitude: float
    longitude: float
    geometry: Dict[str, Any]


@app.post("/api/v1/spatial/calculate-area")
async def calculate_area(req: AreaCalcRequest):
    """Compute land surface area and convert to Indian & Imperial units."""
    try:
        area_sqm = engine.compute_area_sqm(req.geometry)
        units = engine.convert_sqm_to_local_units(area_sqm)
        return {"status": "success", "units": units}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/spatial/check-overlap")
async def check_overlap(req: OverlapCheckRequest):
    """Verify if a property boundary intersects a protected municipal reservation zone."""
    try:
        res = engine.check_overlap(req.subject_geometry, req.reservation_geometry)
        return {"status": "success", "analysis": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/spatial/point-in-polygon")
async def point_in_polygon(req: PointQueryRequest):
    """Check if GPS coordinate lies within parcel boundary."""
    try:
        inside = engine.is_point_inside(req.latitude, req.longitude, req.geometry)
        return {"status": "success", "inside": inside}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
