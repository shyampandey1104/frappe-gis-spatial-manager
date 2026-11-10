# 🗺️ Frappe GIS & Spatial Asset Manager

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Shapely](https://img.shields.io/badge/Shapely-2.0+-green.svg)](https://shapely.readthedocs.io)
[![Leaflet](https://img.shields.io/badge/Leaflet-1.9.4-brightgreen.svg?logo=leaflet)](https://leafletjs.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A specialized **Geospatial & Land Asset Management Engine** for **Frappe Framework & ERPNext**. Integrates **QGIS**, Cadastral Survey maps, Municipal Reservations, and GeoJSON layers directly with ERPNext Land, Property, and Infrastructure DocTypes.

---

## 🌟 Why This Exists

Traditional ERP systems track real estate and land assets purely as alphanumeric text in database tables. **Frappe GIS Spatial Manager** bridges this divide by providing:
- Accurate land area calculation in Indian units (**Gunthas, Acres, Hectares, Sq. Meters**) using EPSG:3857 planar projections.
- Automatic boundary collision & encroachment checking against **Municipal Reservations** (Green Zones, Roads, Public Gardens, DP reservations).
- Interactive **Leaflet.js** map viewer embeddable directly into Frappe Custom Desk Pages.
- GeoJSON and Shapefile ingestion pipeline for regional survey numbers.

---

## 🏗️ System Architecture

```
┌─────────────────────────┐               ┌─────────────────────────┐
│     QGIS / Shapefile    │               │  Cadastral Land Survey  │
│  (Municipal DP Layers)  │               │   (7/12 Extract Data)   │
└────────────┬────────────┘               └────────────┬────────────┘
             │                                         │
             ▼                                         ▼
┌──────────────────────────────────────────────────────────────────┐
│              Frappe GIS Spatial Manager (Python Core)            │
│  • Shapely & PyProj Geometric Projection (EPSG:4326 <-> 3857)    │
│  • Encroachment & Buffer Zone Evaluator                          │
│  • Unit Conversion (Gunthas / Acres / Sq.Meters)                 │
│  • Whitelisted REST API Endpoints                                │
└────────────────────────────┬─────────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
┌───────────────────────────┐ ┌───────────────────────────┐
│  ERPNext Land Asset Desk  │ │   Leaflet Dynamic Viewer  │
│    (DocTypes & Reports)   │ │  (Interactive Web Widget) │
└───────────────────────────┘ └───────────────────────────┘
```

---

## 🚀 Quickstart

### 1. Installation

```bash
git clone https://github.com/shyampandey1104/frappe-gis-spatial-manager.git
cd frappe-gis-spatial-manager
pip install -r requirements.txt
```

### 2. Python API Usage

```python
from spatial_manager import SpatialEngine

engine = SpatialEngine()

# Cadastral parcel coordinates
parcel_polygon = {
    "type": "Polygon",
    "coordinates": [
        [[72.798, 19.465], [72.802, 19.465], [72.802, 19.468], [72.798, 19.468], [72.798, 19.465]]
    ]
}

# 1. Calculate Area across units
area_sqm = engine.compute_area_sqm(parcel_polygon)
units = engine.convert_sqm_to_local_units(area_sqm)
print(f"Area: {units['sq_meters']} Sq.M | {units['acres']} Acres | {units['gunthas']} Gunthas")

# 2. Check Overlap with Municipal Reservation Zone
reservation_polygon = {
    "type": "Polygon",
    "coordinates": [
        [[72.801, 19.466], [72.805, 19.466], [72.805, 19.470], [72.801, 19.470], [72.801, 19.466]]
    ]
}

overlap = engine.check_overlap(parcel_polygon, reservation_polygon)
if overlap["overlaps"]:
    print(f"⚠️ Warning: Encroachment detected! Overlap: {overlap['overlap_percentage']}% ({overlap['overlap_area_sqm']} sq.m)")
```

### 3. Launching Interactive Map Viewer

Open `web/leaflet_gis_viewer.html` in any modern web browser or serve it via FastAPI:
```bash
uvicorn spatial_manager.api:app --reload --port 8000
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

Author: **Shyamkumar Bhupendra Pandey** ([@shyampandey1104](https://github.com/shyampandey1104))
