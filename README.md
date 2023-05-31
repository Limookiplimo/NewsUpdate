# Auto News Updater

Receive news updates from favourite print media to your email.

## Scrape
Scrape data from The Sun, TechCrunch and Tuko news. The data is stored in postgres database as news items.

## Mail Update
Newly scraped items are formated and a notification is pushed to personal mail.

## Airflow DAG
The news update service incorporates apache airflow to orchestrate the service.
[!The dag](assets/dag.jpeg)

## Contribution
Your contributions to improve and critic are highly welcomed.