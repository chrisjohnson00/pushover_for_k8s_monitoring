# pushover_for_k8s_monitoring
A simple, quick solution to send Pushover messages based on kubernetes pod statuses

## Run locally for development

 * Ensure you have a K8s context
 * `python3 -m venv venv`
 * `source venv/bin/activate`
 * `pip install -r requirements.txt`
 * Set your Pushover API details with
  * `export PUSHOVER_APP_ID=yourid`
  * `export PUSHOVER_API_TOKEN=yourtoken` shhh, it's secret!
 * Fire it up with `python3 monitor.py`
