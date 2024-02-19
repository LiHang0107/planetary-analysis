# Calculate NNI for built units data from Planetary
  ### Video Demo:  
    <URL HERE>
  ### Description:
    This Python project is designed to perform geospatial analysis on satellite imagery data to calculate the Nearest Neighbor Index (NNI) of built units within a specified target area. It utilizes various libraries such as GeoPandas, SciPy, NumPy, Rasterio, and the Planetary Computer STAC client to download, process, and analyze geospatial data. The core functionality revolves around identifying specific land use classes from satellite imagery, converting these into geospatial data frames, and computing the NNI to assess the distribution pattern of built units.
  #### function description:
+ main(): Orchestrates the workflow from taking user input to computing and displaying the NNI.
+ grab_item(coord): Searches for and retrieves satellite imagery based on specified coordinates.
+ download_tif(item): Downloads the TIFF file for the retrieved satellite imagery.
+ tif_to_gdf(): Converts the specified class of land use in the TIFF file into a GeoDataFrame.
+ calculate_nni(gdf): Calculates the Nearest Neighbor Index based on the processed GeoDataFrame.

    
TODO
