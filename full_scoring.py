import os
import yaml
import requests
import zipfile
import io
from pathlib import Path
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

cfg = yaml.safe_load(open("config.yaml"))
state = cfg["state_fips"]
county = cfg["county_fips"]

# 1. Download & extract block-group shapefile (once)
tiger_url = "https://www2.census.gov/geo/tiger/TIGER2021/BG/tl_2021_48_bg.zip"
raw_dir   = Path("data/raw")
shp_zip   = raw_dir / "tl_2021_48_bg.zip"
shp_dir   = raw_dir / "tl_2021_48_bg"

raw_dir.mkdir(parents=True, exist_ok=True)
if not shp_dir.exists():
    # Download the zip
    print(f"⏬ Downloading TIGER BG shapefile…")
    resp = requests.get(tiger_url)
    resp.raise_for_status()
    # Extract it
    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        z.extractall(shp_dir)

# 1.2 Read the shapefile from local folder
bg = gpd.read_file(shp_dir / "tl_2021_48_bg.shp")

# 1.3 Filter to your county and ensure string IDs
bg = bg[bg["COUNTYFP"] == "453"].rename(columns={"GEOID":"block_group_id"})
bg["block_group_id"] = bg["block_group_id"].astype(str)

# 2.1 Demographics (no geometry yet)
df_demo = pd.read_csv(
    "data/processed/demographics.csv",
    dtype={"block_group_id": str}
)

# 2.2 Foot-Traffic points
df_ft = pd.read_csv("data/processed/foot_traffic.csv")
gdf_ft = gpd.GeoDataFrame(
    df_ft,
    geometry=[Point(x,y) for x,y in zip(df_ft.longitude, df_ft.latitude)],
    crs=bg.crs
)

# 2.3 Competitor points
df_comp = pd.read_csv("data/processed/competitors.csv")
gdf_comp = gpd.GeoDataFrame(
    df_comp,
    geometry=[Point(x,y) for x,y in zip(df_comp.longitude, df_comp.latitude)],
    crs=bg.crs
)

# --- Diagnostics before joins ---
print("🔍 Block-groups:", len(bg), "records")
print("   ▶ CRS:", bg.crs)
print("   ▶ Bounds:", bg.total_bounds)

print("🔍 Foot-traffic points:", len(gdf_ft), "records")
print("   ▶ CRS:", gdf_ft.crs)
print("   ▶ Bounds:", gdf_ft.total_bounds)

print("🔍 Competitor points:", len(gdf_comp), "records")
print("   ▶ CRS:", gdf_comp.crs)
print("   ▶ Bounds:", gdf_comp.total_bounds)

# Check dtype for block_group_id in demographics
print("▶ df_demo.block_group_id dtype:", df_demo['block_group_id'].dtype)

# 3.1 Foot-traffic counts
ft_join = gpd.sjoin(gdf_ft, bg, how="inner", predicate="within")
print("✔️ FT join rows:", len(ft_join))
ft_counts = (
    ft_join.groupby("block_group_id")
           .size()
           .rename("ft_count")
           .reset_index()
)

# 3.2 Competitor counts
comp_join = gpd.sjoin(gdf_comp, bg, how="inner", predicate="within")
print("✔️ Comp join rows:", len(comp_join))
comp_counts = (
    comp_join.groupby("block_group_id")
             .size()
             .rename("comp_count")
             .reset_index()
)

# 4.1 Base merge on demographics
df = df_demo.merge(ft_counts, on="block_group_id", how="left") \
            .merge(comp_counts, on="block_group_id", how="left") \
            .fillna(0)

# 4.2 Min–max normalization
def norm(s): return (s - s.min()) / (s.max() - s.min())

df["pop_norm"]  = norm(df["population"])
df["inc_norm"]  = norm(df["median_income"])
df["ft_norm"]   = norm(df["ft_count"])
df["comp_norm"] = norm(df["comp_count"])

# 4.3 Opportunity score: reward pop/ft, penalize competition
df["score"] = (
    0.35 * df["pop_norm"] +
    0.35 * df["ft_norm"] +
    0.30 * (1 - df["comp_norm"])
)

# 5. Output top sites
top = df.sort_values("score", ascending=False).head(20)
top.to_csv("data/processed/top_sites.csv", index=False)
print("Top 5 block groups by full score:")
print(top[["block_group_id","population","ft_count","comp_count","score"]].head())


