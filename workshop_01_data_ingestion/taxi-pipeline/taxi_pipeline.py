import dlt
from dlt.sources.rest_api import rest_api_source


source = rest_api_source({
    "client": {
        "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api",
    },
    "resources": [
        {
            "name": "rides",
            "write_disposition": "append",
            "endpoint": {
                "path": "",
                "data_selector": "$",
                "paginator": {
                    "type": "page_number",
                    "base_page": 1,
                    "page_param": "page",
                    "total_path": None,
                    "stop_after_empty_page": True,
                },
            },
        }
    ],
})


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="taxi_rides_ny",
        progress="log",
    )
    load_info = pipeline.run(source)
    print(load_info)
