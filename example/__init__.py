from dagster import Definitions, load_assets_from_package_module

# from .assets import metrics, trips

from example.assets import topstory_ids


# all_assets = load_assets_from_package_module(package_module=example, group_name="core")
# all_assets = load_assets_from_modules([assets])


defs = Definitions(
    assets=[topstory_ids]
)