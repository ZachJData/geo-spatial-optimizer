import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from connectors.demographics import CensusACSAdapter
import pandas as pd

def test_census_adapter_schema():
    # Use a small county for speed—e.g. FIPS '06','075' (San Francisco, CA)
    adapter = CensusACSAdapter(year=2021, state_fips="06", county_fips="075")
    df = adapter.load()
    expected = ["block_group_id", "population", "median_income"]
    assert list(df.columns) == expected, f"Cols mismatch: {df.columns}"
    assert isinstance(df, pd.DataFrame)
    print("Demographics adapter schema is correct. Sample:")
    print(df.head())

if __name__ == "__main__":
    test_census_adapter_schema()
