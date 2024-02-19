from project import grab_item
from project import download_tif
from project import tif_to_gdf
from project import calculate_nni
import pytest
import geopandas as gpd
import numpy as np
from shapely.geometry import Point


def mock_gdf():
    # Create a mock GeoDataFrame for testing
    data = {'geometry': [Point(1, 2), Point(2, 3), Point(3, 4)]}
    gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")
    return gdf


def test_calculate_nni(mock_gdf):
    # Test the calculate_nni function with a mock GeoDataFrame
    nni = calculate_nni(mock_gdf)
    # Assert conditions based on expected behavior
    assert nni > 0, "NNI should be greater than 0"
    assert isinstance(nni, float), "NNI should be a floating point number"


def test_grab_item(coord):
    item = grab_item(coord)
    assert item
