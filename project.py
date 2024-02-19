import json

import geopandas as gpd
from scipy.spatial import cKDTree
import numpy as np
import matplotlib.pyplot as plt
from pystac_client import Client
import planetary_computer as pc
import requests
import numpy as np
import rasterio
from rasterio.features import shapes
from shapely.geometry import Polygon
import src


def main():
    coord = input('your target coordinate: ')
    coord = json.loads(coord)
    item = grab_item(coord)
    download_tif(item)
    gdf = tif_to_gdf()
    nni = calculate_nni(gdf)
    print(f'the NNI of built unit in target area is {nni}')


def grab_item(coord):
    catalog = Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1"
    )

    # area of interest
    aoi = {
        "type": "Polygon",
        "coordinates": [
            coord
        ]
    }

    # temporal range
    daterange = {"interval": ["2022-01-01T23:59:59Z", "2022-12-31T23:59:59Z"]}

    # search with CQL2 syntax
    search = catalog.search(filter_lang="cql2-json", filter={
        "op": "and",
        "args": [
            {"op": "s_intersects", "args": [{"property": "geometry"}, aoi]},
            {"op": "anyinteracts", "args": [{"property": "datetime"}, daterange]},
            {"op": "=", "args": [{"property": "collection"}, "io-lulc-9-class"]}
        ]
    })

    # Grab the first item from the search results and sign the assets
    first_item = next(search.get_items())
    return first_item


def download_tif(item):
    geotiff_url = item.assets["data"].href
    response = requests.get(geotiff_url)
    if response.status_code == 200:
        filepath = 'dld.tif'
        with open(filepath, 'wb') as file:
            file.write(response.content)
        print(f"Successfully downloaded to：{filepath}")
    else:
        print("Failed to download：", response.status_code)


def tif_to_gdf():
    tif_path = 'dld.tif'
    with rasterio.open(tif_path) as src:
        data = src.read(1)
        target_class = 7
        mask = data == target_class
        results = (
            {'properties': {'raster_val': v}, 'geometry': s}
            for i, (s, v) in enumerate(
            shapes(data, mask=mask, transform=src.transform))
            if v == target_class
        )
        gdf = gpd.GeoDataFrame.from_features(list(results))
        print(gdf.head())
    return gdf


def calculate_nni(gdf):
    gdf_points = gdf.centroid
    area = gdf_points.unary_union.convex_hull.area
    n = len(gdf_points)
    density = n / area
    R_exp = 1 / (2 * np.sqrt(density))
    # 使用 cKDTree 计算每个点的最近邻距离
    points = np.array(list(zip(gdf_points.geometry.x, gdf_points.geometry.y)))
    tree = cKDTree(points)
    distances, _ = tree.query(points, k=2)  # 最近的点是其自身
    R_obs = np.mean(distances[:, 1])  # 跳过最近的点（其自身）
    # 计算 NNI
    nni = R_obs / R_exp
    return nni


if __name__ == "__main__":
    main()

