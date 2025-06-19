from abc import ABC, abstractmethod
import os
from census import Census
import pandas as pd

class DemographicsSource(ABC):
    @abstractmethod
    def load(self) -> pd.DataFrame:
        """
        Returns a DataFrame with columns:
        ['block_group_id', 'population', 'median_income']
        """
        pass

class CensusACSAdapter(DemographicsSource):
    def __init__(self, year: int, state_fips: str, county_fips: str):
        """
        year: ACS year (e.g. 2021)
        state_fips: two-digit state code (e.g. '48' for Texas)
        county_fips: three-digit county code (e.g. '501' for Travis County)
        """
        api_key = os.getenv("CENSUS_API_KEY")
        if not api_key:
            raise EnvironmentError("Set CENSUS_API_KEY in your environment.")
        self.c = Census(api_key)
        self.year = year
        self.state = state_fips
        self.county = county_fips

    def load(self) -> pd.DataFrame:
        # Variables: B01003_001E = total population; B19013_001E = median household income
        raw = self.c.acs5.state_county_blockgroup(
            ["B01003_001E", "B19013_001E"],
            self.state, self.county, Census.ALL
        )
        df = pd.DataFrame(raw)
        # Build block_group_id as state+county+tract+block group
        df["block_group_id"] = (
            df["state"] + df["county"] + df["tract"] + df["block group"]
        )
        return df[["block_group_id", "B01003_001E", "B19013_001E"]].rename(
            columns={
                "B01003_001E": "population",
                "B19013_001E": "median_income"
            }
        )