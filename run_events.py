from pathlib import Path

import click
import papermill as pm
from tqdm import tqdm


EVENTS_NOT_READY = ['attica_fire_2024',
                    'paddock_fire_2024',
                    'durkee_fire_2024']


@click.option(
    "--event_name",
    required=True,
    type=str,
    multiple=True,
    help="Provide names of events",
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
@click.command()
def main(event_name: list | tuple, start_step: int, stop_step: int):
    event_names = list(event_name)

    if 'all' in event_names:
        geojson_files = list(Path('external_validation_data_db').glob('*.geojson'))
        parquet_files = list(Path('external_validation_data_db').glob('*.parquet'))
        event_names = [p.stem for p in geojson_files + parquet_files]

        event_names = [en for en in event_names if en not in EVENTS_NOT_READY]
    print(f'Will run on the following {len(event_names)} sites: {"\n".join(event_names)}')

    in_nbs = [
        "1__DIST-HLS.ipynb",
        "2__RTC-S1.ipynb",
        "3__Validation_Data.ipynb",
        "4__Water_Mask.ipynb",
    ]

    for step in [start_step, stop_step]:
        assert step in list(range(1, 5)), 'start and stop must be 1, 2, 3, 4'

    in_nbs = in_nbs[start_step - 1: stop_step]

    ipynb_out_dir = Path("out_notebooks")
    ipynb_out_dir.mkdir(exist_ok=True, parents=True)

    for event_name in tqdm(event_names, desc="events"):
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
