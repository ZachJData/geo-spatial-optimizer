import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from connectors.competitors import OSMCompetitorAdapter
import pandas as pd

def test_competitor_adapter_schema():
    adapter = OSMCompetitorAdapter(
        place_name="Austin, Texas, USA",
        tags={'shop': True}
    )
    df = adapter.load()
    expected = ['comp_id','latitude','longitude']
    assert list(df.columns) == expected, f"Cols mismatch: {df.columns}"
    assert isinstance(df, pd.DataFrame)
    print("Competitor adapter schema is correct. Sample:")
    print(df.head())

if __name__ == "__main__":
    test_competitor_adapter_schema()
