import sys, os
# Insert the project root (one level up) onto sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from connectors.foot_traffic import OSMPOIAdapter
import pandas as pd

def test_osm_adapter_schema():
    adapter = OSMPOIAdapter(tags={'amenity':'cafe'}, week_start='2025-06-01')
    df = adapter.load()
    expected_cols = ['site_id','latitude','longitude','week_start','visitor_count']
    assert list(df.columns) == expected_cols, f"Cols mismatch: {df.columns}"
    assert isinstance(df, pd.DataFrame)
    print("OSM adapter schema is correct. Sample rows:")
    print(df.head())

if __name__ == "__main__":
    test_osm_adapter_schema()
