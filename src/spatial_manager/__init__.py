"""Frappe GIS & Spatial Asset Manager."""

from spatial_manager.engine import SpatialEngine
from spatial_manager.geojson_parser import GeoJSONParser, LandParcelFeature

__version__ = "1.0.0"
__all__ = ["SpatialEngine", "GeoJSONParser", "LandParcelFeature"]
