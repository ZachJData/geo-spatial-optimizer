from abc import ABC, abstractmethod
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd

class FootTrafficSource(ABC):
    @abstractmethod
    def load(self) -> pd.DataFrame:
        """
        Returns a DataFrame with the canonical schema:
        ['site_id','latitude','longitude','week_start','visitor_count']
        """
        pass

class OSMPOIAdapter(FootTrafficSource):
    def __init__(self, tags: dict, week_start: str):
        self.tags = tags
        self.week_start = week_start

    def load(self) -> pd.DataFrame:
        # 1. Fetch geometries (points + polygons)
        gdf = ox.features_from_place("Austin, Texas, USA", tags=self.tags)

        # 2. Keep only Point geometries
        pts = gdf[gdf.geometry.type == 'Point'].copy()

        # 3. Flatten the MultiIndex into a column
        pts = pts.reset_index()

        # OSMnx usually adds an 'osmid' column when you reset_index()
        if 'osmid' in pts.columns:
            site_ids = pts['osmid'].astype(str)
        else:
            # fallback to the generic index column created by reset_index()
            idx_col = pts.columns[0]
            site_ids = pts[idx_col].astype(str)

        # 4. Build the canonical DataFrame
        df = pd.DataFrame({
            'site_id':       site_ids,
            'latitude':      pts.geometry.y,
            'longitude':     pts.geometry.x,
            'week_start':    self.week_start,
            'visitor_count': 1
        })

        return df[['site_id','latitude','longitude','week_start','visitor_count']]