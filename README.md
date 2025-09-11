# Disturbance S1 Events

This is a database of high signal events for DIST-S1 analysis.
Analysis of these events and comparison of these events can be found elsewhere.
There is a fair bit of data curation used here - we select various AOIs (or subsets of those published) to provide easier analysis.

There three important pieces sets of data:

1. Event metadata (date, sources for generation of perimeter, news links, relevant MGRS tiles)
2. Perimeter data (perimeter of event e.g. fire perimeter or inunduation extent)
3. Extent data (some area surrounding perimeter where the data is likely valid; some datasets come with such extents in other cases, we estimate the valid area)

## Useage

The idea is that with date and MGRS tile, we can generate DIST-S1 products to understand the retrieval of the DIST-S1 signal.

## Adding Data

To add an event, you need to create:

1. a yml file within `db/events` with the following template

```yaml
event:
  event_name: `fire_2024` # event name, include some token with fire, flood, landslide please!
  event_date: 'date'  # date of event in the form 2025-01-01
  mgrs_tiles: ['MGRS Tile Id1', 'MGRS Tile Id2]
  source_id: 'Source information or provenance of data'
  links:
    - 'link_1'
    - 'link 2'
```

2. A geojson or parquet file in `db/event_perimeters` that is called either `<event_name>.geojson` or `<event_parquet>.parquet`. with the perimeter
3. A geojson or parquet file in `db/event_extents` that is called either `<event_name>.geojson` or `<event_parquet>.parquet`. with the extent

The notebook aggregates this data to make sure everything is properly formatted and included.

