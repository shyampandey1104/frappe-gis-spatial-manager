"""Unit tests for SpatialEngine geometric computations."""

from spatial_manager.engine import SpatialEngine


def test_area_and_unit_conversion():
    engine = SpatialEngine()
    # Simple 100m x 100m square polygon in WGS84 coordinates approx
    sq_poly = {
        "type": "Polygon",
        "coordinates": [
            [[72.8000, 19.4600], [72.8010, 19.4600], [72.8010, 19.4610], [72.8000, 19.4610], [72.8000, 19.4600]]
        ]
    }
    area_sqm = engine.compute_area_sqm(sq_poly)
    assert area_sqm > 0

    units = engine.convert_sqm_to_local_units(area_sqm)
    assert units["sq_meters"] == round(area_sqm, 2)
    assert units["acres"] > 0
    assert units["gunthas"] > 0


def test_overlap_detection():
    engine = SpatialEngine()
    poly_a = {
        "type": "Polygon",
        "coordinates": [[[0.0, 0.0], [2.0, 0.0], [2.0, 2.0], [0.0, 2.0], [0.0, 0.0]]]
    }
    poly_b = {
        "type": "Polygon",
        "coordinates": [[[1.0, 1.0], [3.0, 1.0], [3.0, 3.0], [1.0, 3.0], [1.0, 1.0]]]
    }
    res = engine.check_overlap(poly_a, poly_b)
    assert res["overlaps"] is True
    assert res["overlap_percentage"] > 0


def test_point_in_polygon():
    engine = SpatialEngine()
    poly = {
        "type": "Polygon",
        "coordinates": [[[10.0, 10.0], [20.0, 10.0], [20.0, 20.0], [10.0, 20.0], [10.0, 10.0]]]
    }
    # Point inside (lat=15, lng=15)
    assert engine.is_point_inside(15.0, 15.0, poly) is True
    # Point outside (lat=5, lng=5)
    assert engine.is_point_inside(5.0, 5.0, poly) is False
