# How To

## Setup a Cronjob

Open crontab editor with `crontab -e`

Add the following

```
*/10 * * * * /path/to/venv/bin/python /path/to/project/manage.py your_command_name >> /path/to/logs/cron.log 2>&1
```

Note: Substitute placeholder pathnames with actual pathnames
