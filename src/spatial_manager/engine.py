"""Geospatial computational engine for Frappe Land & Property assets."""

from typing import Dict, Any, List, Tuple, Optional
import math
from shapely.geometry import shape, mapping, Polygon, Point, MultiPolygon
from shapely.ops import transform
import pyproj


class SpatialEngine:
    """Performs geometric calculations, buffer analysis, and overlap detection."""

    def __init__(self):
        # WGS84 (GPS standard) to Web Mercator projection transformer
        self.wgs84_to_mercator = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True).transform
        self.mercator_to_wgs84 = pyproj.Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True).transform

    def compute_area_sqm(self, geojson_geom: Dict[str, Any]) -> float:
        """Compute surface area in Square Meters projected in EPSG:3857."""
        geom = shape(geojson_geom)
        projected = transform(self.wgs84_to_mercator, geom)
        return float(projected.area)

    def convert_sqm_to_local_units(self, area_sqm: float) -> Dict[str, float]:
        """Convert square meters to Acres, Hectares, Sq Yards, and Gunthas."""
        return {
            "sq_meters": round(area_sqm, 2),
            "acres": round(area_sqm / 4046.8564224, 4),
            "hectares": round(area_sqm / 10000.0, 4),
            "sq_yards": round(area_sqm * 1.19599, 2),
            "gunthas": round(area_sqm / 101.17, 3),  # Standard Indian land unit
        }

    def check_overlap(self, subject_geom: Dict[str, Any], reservation_geom: Dict[str, Any]) -> Dict[str, Any]:
        """Check if subject parcel encroaches or overlaps a reservation zone."""
        poly_subject = shape(subject_geom)
        poly_res = shape(reservation_geom)

        if not poly_subject.intersects(poly_res):
            return {
                "overlaps": False,
                "overlap_area_sqm": 0.0,
                "overlap_percentage": 0.0,
                "overlap_geojson": None,
            }

        intersection = poly_subject.intersection(poly_res)
        subject_proj = transform(self.wgs84_to_mercator, poly_subject)
        intersect_proj = transform(self.wgs84_to_mercator, intersection)

        overlap_area = intersect_proj.area
        total_area = subject_proj.area
        pct = (overlap_area / total_area * 100.0) if total_area > 0 else 0.0

        return {
            "overlaps": True,
            "overlap_area_sqm": round(overlap_area, 2),
            "overlap_percentage": round(pct, 2),
            "overlap_geojson": mapping(intersection),
        }

    def create_buffer_zone(self, geojson_geom: Dict[str, Any], distance_meters: float) -> Dict[str, Any]:
        """Generate a buffer polygon around a parcel (e.g. 50m road buffer)."""
        geom = shape(geojson_geom)
        projected = transform(self.wgs84_to_mercator, geom)
        buffered_proj = projected.buffer(distance_meters)
        buffered_wgs84 = transform(self.mercator_to_wgs84, buffered_proj)
        return mapping(buffered_wgs84)

    def is_point_inside(self, lat: float, lng: float, geojson_geom: Dict[str, Any]) -> bool:
        """Check if a coordinate point falls inside a cadastral boundary."""
        pt = Point(lng, lat)  # (x, y) = (lng, lat)
        poly = shape(geojson_geom)
        return bool(poly.contains(pt))
