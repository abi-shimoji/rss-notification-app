#!/bin/bash

aws --endpoint-url http://localhost:2773 ssm put-parameter --name '/rss-notification-app/slack/endpoint' --type 'String' --value 'https://hooks.slack.com/services/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'
aws --endpoint-url http://localhost:2773 ssm put-parameter --name '/rss-notification-app/slack/api-key' --type 'String' --value 'value/String'
aws --endpoint-url http://localhost:2773 ssm put-parameter --name '/rss-notification-app/spreadsheet/api-key' --type 'String' --value 'AIzaSyD6UD0yF-_Vx0ZEiLoSqndQnk6BrDkY16k'

