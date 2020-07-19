from kubernetes import client, config
import os
import time
from pushover import Client


def main():
    print("INFO: {} Starting...".format(datetime.now().strftime("%b %d %H:%M:%S")), flush=True)
    try:
        config.load_kube_config()
    except Exception:
        send_pushover_notification("Kube Config Error", "Unable to get Kubernetes config to talk to the cluster")
        exit("Barf, die, can't get cluster config")
    try:
        v1 = client.CoreV1Api()
        ret = v1.list_pod_for_all_namespaces(watch=False)
        unready_pods = []
        for item in ret.items:
            conditions = item.status.conditions
            for condition in conditions:
                if condition.type == "Ready" and condition.reason != "PodCompleted":
                    if condition.status == "False":
                        print("WARN: Uh-oh, this guy's not ready {}".format(item.metadata.name))
                        unready_pods.append(item.metadata.name)
        if len(unready_pods) > 0:
            send_pushover_notification("There are unready pods", " ".join(unready_pods))
    except Exception:
        send_pushover_notification("Kube Cluster Error", "Unable to query the cluster!")
        exit("Barf, die, can't query the cluster")
    print("INFO: {} Done!".format(datetime.now().strftime("%b %d %H:%M:%S")), flush=True)


def send_pushover_notification(title, message):
    client = Client(PUSHOVER_APP_ID, api_token=PUSHOVER_API_TOKEN)
    client.send_message(message, title=title)


if __name__ == '__main__':
    if not os.environ.get("PUSHOVER_APP_ID"):
        exit("Yo, dude, come on!  I need a PUSHOVER_APP_ID environment variable to work, bra!")
    PUSHOVER_APP_ID = os.environ.get("PUSHOVER_APP_ID")
    if not os.environ.get("PUSHOVER_API_TOKEN"):
        exit("Yo, dude, come on!  I need a PUSHOVER_API_TOKEN environment variable to work, bra!")
    PUSHOVER_API_TOKEN = os.environ.get("PUSHOVER_API_TOKEN")
    while True:
        main()
        time.sleep(3600)
