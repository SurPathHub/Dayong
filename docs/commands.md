Here's the list of commands available in Dayong.

## Message Commands

| Name                | Description                      | Usage                | Permission                | Cooldown |
| ------------------- | -------------------------------- | :------------------: | :-----------------------: | :------: |
| **ping**            | Shows bot reachability.          | `<prefix>ping`       |    View Audit Log (128)   |   null   |
| **whois**           | Shows information about a user   | `<prefix>whois <id>` |    View Audit Log (128)   |   null   |

## Slash Commands

| Name                | Description                      | Usage                            | Cooldown  |
| ------------------- | -------------------------------- | :------------------------------: | :-------: |
| **anon**            | Sends an anonymized message.     | `/anon message: <message>`       |    null   |
| **content**         | Schedules a recurring task that retrieves content from a microservice, API, or email subscription. For `source`, see [vendors](./vendors.md#content-providers). | `/content source: <content provider> interval: <seconds> action: <start \| stop>` |    null   |
