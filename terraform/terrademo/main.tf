terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.12.0"
    }
  }
}

provider "google" {
  # Configuration options
  credentials = "./keys/my-creds.json"
  project     = "potent-well-443419-e3"
  region      = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "potent-well-443419-e3-terra-bucket" # has to be globally unique 
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}