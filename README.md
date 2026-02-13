# Data Engineering Zoomcamp

This repository contains my notes, homework, and projects from the
[Data Engineering Zoomcamp 2026](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/README.md).

## Structure

- [`01_docker_terraform/`](01_docker_terraform)
  - Containerization with Docker and Docker Compose
  - PostgreSQL data ingestion with Python/pandas
  - Infrastructure as Code using Terraform
  - GCP setup (BigQuery, Cloud Storage, IAM)
- [`02_workflow_orchestration/`](02_workflow_orchestration)
  - Workflow scheduling and automation
  - Building ETL pipelines with Kestra
  - Data extraction from APIs and files
  - Loading data to PostgreSQL, GCS, and BigQuery
- [`03_data_warehouse/`](03_data_warehouse)
  - Data warehouse architecture and design patterns
  - OLAP vs OLTP database systems
  - BigQuery fundamentals and serverless architecture
  - Partitioning and clustering for query optimization
- [`04_analytics_engineering/`](04_analytics_engineering)
  - Analytics Engineering role and transformation workflows with dbt
  - Dimensional modeling with Kimball methodology (facts & dimensions)
  - Building modular SQL models with testing and documentation
- [`05_data_platforms/`](05_data_platforms)
  - Unified data pipelines with Bruin (ingestion + transformation + quality)
  - Materialization strategies and incremental processing with time_interval
  - Quality checks and metadata-driven development
  - Pipeline variables, lineage tracking, and full-refresh deployments