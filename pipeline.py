import yaml
import importlib
from pathlib import Path

def get_adapter(class_path: str, **kwargs):
    module_name, cls_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    Adapter = getattr(module, cls_name)
    return Adapter(**kwargs)

def main():
    # 1. Load config
    cfg = yaml.safe_load(open("config.yaml"))

    # 2. Foot Traffic
    ft_cfg = {
        "tags": cfg.get("osm_tags", {}),
        "week_start": cfg.get("week_start")
    }
    ft_adapter = get_adapter(cfg["foot_traffic_source"], **ft_cfg)
    df_ft = ft_adapter.load()
    print("▶️ Foot-traffic sample:")
    print(df_ft.head(), "\n")

    # 3. Demographics
    demo_cfg = {
        "year": cfg.get("acs_year"),
        "state_fips": cfg.get("state_fips"),
        "county_fips": cfg.get("county_fips")
    }
    demo_adapter = get_adapter(cfg["demographics_source"], **demo_cfg)
    df_demo = demo_adapter.load()
    print("▶️ Demographics sample:")
    print(df_demo.head(), "\n")

    # 4. Competitors
    comp_cfg = {
        "place_name": cfg.get("competitor_place"),
        "tags": cfg.get("competitor_tags", {})
    }
    comp_adapter = get_adapter(cfg["competitor_source"], **comp_cfg)
    df_comp = comp_adapter.load()
    print("▶️ Competitor sample:")
    print(df_comp.head(), "\n")

    # 5. Persist outputs
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)
    df_ft.to_csv(out_dir / "foot_traffic.csv", index=False)
    df_demo.to_csv(out_dir / "demographics.csv", index=False)
    df_comp.to_csv(out_dir / "competitors.csv", index=False)
    print(f"✅ Written CSVs to {out_dir}")

if __name__ == "__main__":
    main()
