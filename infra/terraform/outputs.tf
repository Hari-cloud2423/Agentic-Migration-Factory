output "cloud_run_url" {
  value       = google_cloud_run_v2_service.api.uri
  description = "Public URL of Agentic Migration Factory API"
}

output "artifact_registry_repo" {
  value       = google_artifact_registry_repository.repo.id
  description = "Artifact Registry repository path"
}
