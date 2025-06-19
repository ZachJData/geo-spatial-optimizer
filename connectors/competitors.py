from abc import ABC, abstractmethod
import osmnx as ox
from shapely.geometry import Point
import pandas as pd

class CompetitorSource(ABC):
    @abstractmethod
    def load(self) -> pd.DataFrame:
        """
        Returns a DataFrame with columns:
        ['comp_id','latitude','longitude']
        """
        pass

class OSMCompetitorAdapter(CompetitorSource):
    def __init__(self, place_name: str, tags: dict):
        """
        place_name: e.g. "Austin, Texas, USA"
        tags: OSM tags to filter competitor types,
              e.g. {'shop': True} or {'amenity':'fast_food'}
        """
        self.place_name = place_name
        self.tags = tags

    def load(self) -> pd.DataFrame:
        # 1. fetch all matching features
        gdf = ox.features_from_place(self.place_name, tags=self.tags)

        # 2. keep only Point geometries
        pts = gdf[gdf.geometry.type == 'Point'].reset_index()

        # 3. pick an ID column: osmid if present, else the generic index
        if 'osmid' in pts.columns:
            comp_ids = pts['osmid'].astype(str)
        else:
            comp_ids = pts[pts.columns[0]].astype(str)

        # 4. build canonical DataFrame
        df = pd.DataFrame({
            'comp_id':    comp_ids,
            'latitude':   pts.geometry.y,
            'longitude':  pts.geometry.x
        })
        return df[['comp_id','latitude','longitude']]