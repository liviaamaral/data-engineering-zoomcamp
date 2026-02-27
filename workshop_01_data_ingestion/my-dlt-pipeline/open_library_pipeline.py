"""REST API Source for the Open Library API.
Docs: https://openlibrary.org/dev/docs/api/books

Run with:
    python open_library_pipeline.py
"""

import dlt
from dlt.sources.rest_api import (
    RESTAPIConfig,
    rest_api_resources,
)


@dlt.source
def open_library_source():
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://openlibrary.org/",
            # Open Library does not require authentication for read endpoints
        },
        "resources": [
            {
                # Top 100 most-read books of the past year
                # Docs: https://openlibrary.org/trending/yearly.json
                "name": "books",
                "endpoint": {
                    "path": "trending/yearly.json",
                    # Response shape: { "works": [...], "days": 0, "hours": 0 }
                    "data_selector": "works",
                    "paginator": {
                        "type": "single_page",
                    },
                },
                "write_disposition": "replace",
            },
        ],
    }

    yield from rest_api_resources(config)


def get_data() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="open_library_pipeline",
        destination="duckdb",
        dataset_name="open_library_data",
        progress="log",
    )

    load_info = pipeline.run(open_library_source())
    print(load_info)


if __name__ == "__main__":
    get_data()
