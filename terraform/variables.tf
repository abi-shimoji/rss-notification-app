variable "discord_webhook_endpoint" {
  description = "discord webhook endpoint"
  type        = string
  sensitive   = true
}

variable "slack_webhook_endpoint" {
  description = "slack webhook endpoint"
  type        = string
  sensitive   = true
}

variable "slack_api_key" {
  description = "slack api key"
  type        = string
  sensitive   = true
}

variable "spreadsheet_api_key" {
  description = "google spreadsheet api key"
  type        = string
  sensitive   = true
}
