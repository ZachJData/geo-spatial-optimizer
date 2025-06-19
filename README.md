👤 About Me
Zach Johnson, Data Analyst & Full-Stack Developer

🔗 GitHub

🔗 LinkedIn

✉️ scienceofanalytics@gmail.com

# Geo-Spatial Retail Expansion Optimizer

**A “find-your-next-store” demo that turns free map and census data into clear, ranked expansion opportunities—complete with interactive maps and tables.**

---

## 🚀 What It Is

Imagine deciding where to open your next coffee shop in minutes instead of months. This tool:

1. **Counts nearby hotspots** (using OpenStreetMap POIs as a proxy for foot traffic).  
2. **Checks local demographics** (population size & income via the Census ACS).  
3. **Measures competition** (free-tier Foursquare/Yelp lookups).  
4. **Crunches it all into one “opportunity score”** so you can instantly rank any number of candidate sites.  
5. **Shows results on an interactive map & sortable table** in a simple Streamlit dashboard.

---

## 🎯 Key Features

- **Modular Connectors**: Swap OSMnx for SafeGraph (or any vendor) with one config change.  
- **Zero-Cost Data**: Built on open data (OSM, Census) and open-source libraries.  
- **Interactive Dashboard**: Streamlit + Folium gives you map + table with one-click deploy to their free tier.  
- **Clustering & Insights**: scikit-learn KMeans surfaces geographic hotspots.  
- **Config-Driven**: YAML file controls which data adapters to use—no code rewrites needed.

---

## 🛠 Tech Stack

- **Data & Spatial**: `geopandas`, `osmnx`, `folium`, `shapely`  
- **Demographics API**: `census` Python package  
- **Modeling & Clustering**: `pandas`, `scikit-learn`  
- **Web UI**: `streamlit`  
- **Config**: `PyYAML`  
- **Version Control & CI**: GitHub (Actions, if desired)

---

## 📁 Repo Structure
geo-spatial-retail-optimizer/
├── connectors/ # data-source adapters (OSMnx, SafeGraph stub)
├── data/ # raw & processed sample files
├── notebooks/ # exploratory POCs
├── streamlit_app.py # main dashboard
├── config.yaml # select adapters via class path
├── requirements.txt # pinned dependencies
└── README.md # you are here!
