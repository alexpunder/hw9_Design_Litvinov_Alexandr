terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_container" "postgres" {
  name  = "airflow_postgres"
  image = docker_image.postgres.image_id

  env = [
    "POSTGRES_USER=airflow",
    "POSTGRES_PASSWORD=airflow",
    "POSTGRES_DB=airflow"
  ]

  ports {
    internal = 5432
    external = 5432
  }
}

resource "docker_container" "s3" {
  name  = "minio_storage"
  image = docker_image.s3.image_id

  command = [
    "server",
    "/data"
  ]

  ports {
    internal = 9000
    external = 9000
  }
}

resource "docker_container" "airflow" {
  name  = "airflow_ct"
  image = docker_image.airflow.image_id

  ports {
    internal = 8080
    external = 8080
  }
}
