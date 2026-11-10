"""GeoJSON parser and sanitizer for Frappe custom DocTypes."""

import json
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class LandParcelFeature(BaseModel):
    survey_number: str
    village: str
    taluka: Optional[str] = None
    district: Optional[str] = None
    zone_type: str = Field(default="Residential", description="Residential, Commercial, Industrial, Green, No-Development")
    reservation_status: str = Field(default="Clear", description="Clear, Reserved, In-Litigation")
    area_sqm: float
    coordinates: Dict[str, Any]


class GeoJSONParser:
    """Parses GeoJSON FeatureCollections into structured ERPNext records."""

    @staticmethod
    def parse_feature_collection(geojson_data: Dict[str, Any]) -> List[LandParcelFeature]:
        features = geojson_data.get("features", [])
        parcels: List[LandParcelFeature] = []

        for feat in features:
            props = feat.get("properties", {})
            geom = feat.get("geometry", {})

            if not geom or geom.get("type") not in ("Polygon", "MultiPolygon"):
                continue

            parcel = LandParcelFeature(
                survey_number=str(props.get("survey_no") or props.get("survey_number") or props.get("id") or "UNKNOWN"),
                village=str(props.get("village", "Virar")),
                taluka=str(props.get("taluka", "Vasai")),
                district=str(props.get("district", "Palghar")),
                zone_type=str(props.get("zone", "Residential")),
                reservation_status=str(props.get("reservation", "Clear")),
                area_sqm=float(props.get("area_sqm", 0.0)),
                coordinates=geom,
            )
            parcels.append(parcel)

        return parcels
