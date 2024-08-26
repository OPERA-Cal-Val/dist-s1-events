from pathlib import Path

import click
import papermill as pm
from tqdm import tqdm


EVENTS_NOT_READY = [
    "paddock_fire_2024",
    "durkee_fire_2024",
    "derna_flood_2023",
    "benghazi_flood_2023",
]

geojson_files = list(Path("external_validation_data_db").glob("*.geojson"))
parquet_files = list(Path("external_validation_data_db").glob("*.parquet"))
ALL_EVENTS = sorted(
    [p.stem for p in geojson_files + parquet_files if p.stem not in EVENTS_NOT_READY]
)


@click.option(
    "--event",
    required=True,
    type=str,
    help=(
        "Provide names of events; multiple events put in quotes separted by string; the possible events are"
        f"{','.join(ALL_EVENTS)}"
    ),
)
@click.option(
    "--start_step",
    required=False,
    type=int,
    default=1,
    help="step to start generation on - not recommended to use with more than one event - see notebooks 1 - 4",
)
@click.option(
    "--stop_step",
    required=False,
    type=int,
    default=4,
    help="step to stop data generation on - not recommended to use with more than one event - see notebooks 1 to 4",
)
@click.option(
    "--exclude_event",
    required=False,
    type=str,
    help="Provide names of event; multiple events seperated_by a space using quotes",
)
@click.command()
def main(event: str, start_step: int, stop_step: int, exclude_event: str):
    events = [e.strip() for e in event.split(" ")]

    if "all" in events:
        events = ALL_EVENTS
    if exclude_event is not None:
        exclude_events = [e.strip() for e in exclude_event.split(" ")]
        events = [e for e in events if e not in exclude_events]

    bad_events = [e for e in events if e not in ALL_EVENTS]
    if bad_events:
        raise ValueError(f'{", ".join(bad_events)} is/are not valid event names')

    print(f'Will run on the following {len(events)} sites:\n {"\n".join(events)}')

    in_nbs = [
        "1__DIST-HLS.ipynb",
        "2__RTC-S1.ipynb",
        "3__Validation_Data.ipynb",
        "4__Water_Mask.ipynb",
    ]

    for step in [start_step, stop_step]:
        assert step in list(range(1, 5)), "start and stop must be 1, 2, 3, 4"

    in_nbs = in_nbs[start_step - 1 : stop_step]

    ipynb_out_dir = Path("out_notebooks")
    ipynb_out_dir.mkdir(exist_ok=True, parents=True)

    for event_name in tqdm(events, desc="events"):
        print(event_name)
        out_site_nb_dir = ipynb_out_dir / event_name
        out_site_nb_dir.mkdir(exist_ok=True, parents=True)
        for in_nb in in_nbs:
            print(in_nb)
            pm.execute_notebook(
                in_nb,
                output_path=out_site_nb_dir / in_nb,
                parameters=dict(EVENT_NAME=event_name),
            )


if __name__ == "__main__":
    main()
