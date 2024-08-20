# Disturbance S1 Events

This is a code-base is used to the generate coregistered datasets for DIST-S1 calibration and validation.
The actual datasets are derived from publicaly available datasets (see [Datasets](#datasets) below).
We utilize geojsons in the `external_validation_data_db`, each of which is curated from publicly available datasets.
The provenance of these datasets is included in the properties and the associated event `yml` in the `events/` directory.
This is still very much a work in progress and more information about its use and application will be added as it is refined.

## Installation

Intall the environment and notebook kernel:

```
mamba env update -f environment.yml
conda activate dist-s1
python -m ipykernel install --user --name dist-s1
```

## Generating datasets

```
python run_events --event_name all
```

The datasets should be generated in an `out` directory. The total size currently is about 60 GB of data.

## Datasets

We use the following sources for generating these datasets.


1. The Copernicus Emergency Management Service, specifically the rapid mapping of these events: https://rapidmapping.emergency.copernicus.eu/
2. The UNOSAT data available through humanitarian data exchange: https://data.humdata.org/ (search "flood extents" for example!)
3. The Wildland Fire Interagency Geospatial Services from the National Interagency Fire Center: https://data-nifc.opendata.arcgis.com/datasets/nifc::wfigs-current-interagency-fire-perimeters/about
4. Hand drawn delineations

There are additional sources that will be added but for now this is what is available. We note that all the datasets are derived from *optical* sensors (either Sentinel-1, planet or other VHR sensors). In addition to acquisition times being different than SAR, the actual impacted areas will appear different so this provides some insight into the differences.