# Data Engineering Zoomcamp - Week 1 Notes

## Module Overview: Docker & Terraform

Week 1 focuses on containerization with Docker and infrastructure as code with Terraform. These are foundational tools for creating reproducible, scalable data engineering environments.

---

## Part 1: Docker

### What is Docker?

Docker is a containerization platform that packages applications with all their dependencies into isolated, portable containers. It solves the "works on my machine" problem by ensuring consistency across different environments.

**Key Concepts:**
- **Container**: A lightweight, isolated environment that runs an application with all dependencies
- **Image**: A read-only template containing code, runtime, libraries, and configurations needed to run a container
- **Dockerfile**: A text file with instructions to build a Docker image

**Benefits:**
- Reproducibility across environments
- Portability (move containers between systems easily)
- Isolation (applications don't interfere with each other)
- Efficiency (lightweight compared to virtual machines)

### Basic Docker Commands

```bash
# Run a simple container
docker run hello-world

# Run container interactively
docker run -it ubuntu bash

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop a container
docker stop <container_name>

# Start a stopped container
docker start <container_name>

# Remove a container
docker rm <container_id>

# List images
docker images

# Remove an image
docker rmi <image_name>
```

---

## Part 2: Running PostgreSQL with Docker

### Setting Up PostgreSQL Container

PostgreSQL is a powerful relational database. Instead of installing it locally, we run it in a Docker container.

```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

**Parameter Explanation:**
- `-e`: Sets environment variables (user, password, database name)
- `-v`: Mounts a volume for data persistence (maps local directory to container directory)
- `-p 5432:5432`: Maps port 5432 from container to host (format: host:container)
- `postgres:13`: The image name and version tag

**Important Note:** The volume mapping ensures your data persists even if the container is stopped or deleted.

### Connecting to PostgreSQL

You can connect using command-line tools like `pgcli`:

```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

---

## Part 3: Data Ingestion with Python

### Creating an Ingestion Script

The course demonstrates ingesting NYC taxi trip data into PostgreSQL using Python, Pandas, and SQLAlchemy.

**Key Libraries:**
- `pandas`: Data manipulation and analysis
- `sqlalchemy`: Database connection and operations
- `psycopg2`: PostgreSQL adapter for Python

**Basic Ingestion Flow:**
1. Download/read the data (CSV or Parquet format)
2. Load data into a pandas DataFrame
3. Create a database connection using SQLAlchemy
4. Write DataFrame to PostgreSQL table using `df.to_sql()`

**Important Considerations:**
- Handle data types correctly (especially date/datetime columns)
- For large datasets, ingest data in chunks to avoid memory issues
- Schema must be correct before loading data

---

## Part 4: pgAdmin - Database Management Tool

### What is pgAdmin?

pgAdmin is a web-based GUI for managing PostgreSQL databases. Instead of installing it locally, we run it in a Docker container.

### Running pgAdmin Container

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```

Access pgAdmin at: `http://localhost:8080`

### Docker Networking

**Problem:** Initially, the pgAdmin container can't see the PostgreSQL container because they're isolated.

**Solution:** Create a Docker network to allow container communication.

```bash
# Create a network
docker network create pg-network

# Run PostgreSQL with network
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13

# Run pgAdmin with network
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

**Key Points:**
- Both containers must be on the same network
- Use `--name` to assign container names
- In pgAdmin, use the container name (e.g., `pg-database`) as the hostname

### Registering PostgreSQL Server in pgAdmin

1. Log into pgAdmin (`admin@admin.com` / `root`)
2. Right-click "Servers" → "Create" → "Server"
3. General tab: Give it a name
4. Connection tab:
   - Host: `pg-database` (the container name)
   - Port: `5432`
   - Username: `root`
   - Password: `root`

---

## Part 5: Dockerizing the Ingestion Script

### Creating a Dockerfile

A Dockerfile defines how to build a custom image for your ingestion script.

```dockerfile
FROM python:3.9

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT ["python", "ingest_data.py"]
```

**Dockerfile Instructions:**
- `FROM`: Base image to start from
- `RUN`: Execute commands during build
- `WORKDIR`: Set working directory
- `COPY`: Copy files from host to image
- `ENTRYPOINT`: Command to run when container starts

### Building and Running the Custom Image

```bash
# Build the image
docker build -t taxi_ingest:v001 .

# Run the container (on the network)
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```

**Note:** The script should use `argparse` to accept command-line parameters for flexibility.

---

## Part 6: Docker Compose

### What is Docker Compose?

Docker Compose is a tool for defining and running multi-container applications using a YAML file. It simplifies the process of managing multiple containers and their connections.

### Creating docker-compose.yml

Instead of running multiple `docker run` commands, define everything in one file:

```yaml
services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    volumes:
      - "./ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"
  
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    volumes:
      - "./pgadmin_data:/var/lib/pgadmin:rw"
    ports:
      - "8080:80"
```

### Docker Compose Commands

```bash
# Start all services (creates network automatically)
docker-compose up

# Start in detached mode (runs in background)
docker-compose up -d

# Stop all services
docker-compose down

# View running services
docker-compose ps
```

**Benefits:**
- Automatic network creation (no need to manually create networks)
- All configuration in one file
- Easy to version control
- Single command to start/stop entire stack

---

## Part 7: Introduction to Terraform

### What is Terraform?

Terraform is an Infrastructure as Code (IaC) tool that allows you to define cloud and on-premises resources in human-readable configuration files. It automates the creation, management, and deletion of infrastructure.

**Benefits:**
- Automation (no manual clicking in cloud consoles)
- Version control for infrastructure
- Reproducibility across environments
- Consistency and reduced errors
- Easy cleanup of resources

### Key Terraform Concepts

- **Provider**: A plugin that enables Terraform to interact with cloud platforms (e.g., Google Cloud, AWS, Azure)
- **Resource**: Infrastructure components you want to create (e.g., storage buckets, databases)
- **Variable**: Parameterized values for flexibility and reusability
- **State**: Terraform tracks current infrastructure state in `terraform.tfstate`

### Basic Terraform Workflow

```bash
# Initialize Terraform (downloads providers)
terraform init

# Preview changes (dry run)
terraform plan

# Apply changes (create resources)
terraform apply

# Destroy all resources
terraform destroy
```

### Example: Creating GCP Resources

**main.tf** - Define resources:
```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

resource "google_storage_bucket" "demo_bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}
```

**variables.tf** - Define variables:
```hcl
variable "project" {
  description = "Your GCP Project ID"
  type        = string
}

variable "region" {
  description = "Region for resources"
  type        = string
  default     = "us-central1"
}

variable "gcs_bucket_name" {
  description = "Storage bucket name"
  type        = string
}

variable "bq_dataset_name" {
  description = "BigQuery dataset name"
  type        = string
}
```

**terraform.tfvars** (optional) - Set variable values:
```hcl
project          = "my-project-id"
gcs_bucket_name  = "my-terraform-bucket"
bq_dataset_name  = "demo_dataset"
```

### Google Cloud Platform Setup

Before using Terraform with GCP:

1. **Create a GCP account** and project
2. **Create a Service Account** with appropriate permissions:
   - Storage Admin
   - BigQuery Admin
3. **Generate and download** a JSON key file for the service account
4. **Set up authentication**:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
   ```

---

## Key Takeaways

### Docker
- Containers provide isolated, reproducible environments
- Docker Compose simplifies multi-container applications
- Volume mapping ensures data persistence
- Networks enable container communication

### Data Engineering Workflow
- Separate concerns (database, admin tool, ingestion script) into different containers
- Use proper schema handling when ingesting data
- Parameterize scripts for flexibility

### Terraform
- Infrastructure as Code enables version-controlled, automated infrastructure
- Variables make configurations reusable and scalable
- Always run `terraform destroy` to clean up resources and avoid costs

---

## Common Issues & Solutions

**Docker on Windows:**
- Install WSL2 (Windows Subsystem for Linux)
- Use Linux paths for volume mounting, not Windows paths
- May need `winpty` prefix for some Docker commands in Git Bash

**Container Name Conflicts:**
- Error: "container name is already in use"
- Solution: Remove old container with `docker rm <container_id>` or use different name

**Network Communication:**
- Containers must be on the same network to communicate
- Use container names (not localhost) as hostnames between containers

**PostgreSQL Connection:**
- If using pgcli or other tools, connect to `localhost` from host
- From within containers, use container name as hostname

---

## Resources

- [Data Engineering Zoomcamp GitHub](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- [Docker Documentation](https://docs.docker.com/)
- [Terraform Documentation](https://www.terraform.io/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- Course Slack: Join #course-data-engineering for discussions and help