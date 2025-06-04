provider "aws" {
  region = "ap-northeast-1"
}

resource "aws_ssm_parameter" "DISCORD_WEBHOOK_ENDPOINT" {
  name        = "/rss-notification-app/discord/endpoint"
  type        = "SecureString"
  value       = var.discord_webhook_endpoint
  description = "discord webhook endpoint"
  overwrite   = true
}

resource "aws_ssm_parameter" "SLACK_WEBHOOK_ENDPOINT" {
  name        = "/rss-notification-app/slack/endpoint"
  type        = "SecureString"
  value       = var.slack_webhook_endpoint
  description = "slack webhook endpoint"
  overwrite   = true
}

resource "aws_ssm_parameter" "SLACK_API_KEY" {
  name        = "/rss-notification-app/slack/api-key"
  type        = "SecureString"
  value       = var.slack_api_key
  description = "slack api key"
  overwrite   = true
}

resource "aws_ssm_parameter" "SPREADSHEET_API_KEY" {
  name        = "/rss-notification-app/spreadsheet/api-key"
  type        = "SecureString"
  value       = var.spreadsheet_api_key
  description = "google spreadsheet api key"
  overwrite   = true
}
