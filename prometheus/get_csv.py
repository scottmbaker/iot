from __future__ import print_function
import requests
import sys

def get_metrics_json(metric, start_timestamp, stop_timestamp, step="1m"):
    r = requests.get(url = "http://127.0.0.1:9090/api/v1/query_range",
        params = {
            "query": metric,
            "start": str(start_timestamp),
            "end": str(stop_timestamp),
            "step": step
        })
    
    if r.status_code != 200:
        raise Exception("Status code is %d reason=%s" % (r.status_code, r.reason))

    json = r.json()

    return json

def get_labels(j):
    items = j["data"]["result"]

    labels = []

    for item in items:
        if not ("metric" in item):
             continue
        metric = item["metric"]

        for k in metric.keys():
            if not k in labels:
                labels.append(k)

    return labels

def parse_metrics_json(j):
    items = j["data"]["result"]

    labels = get_labels(j)

    rows = []

    for item in items:
        if not ("metric" in item):
             continue            
        if not ("values" in item):
             continue    

        metric = item["metric"]
        values = item["values"]

        for value in values:
            if len(value)<2:
                continue

            row = []
            for k in labels:
                row.append(str(metric.get(k,"")))

            row.append(str(value[0]))
            row.append(str(value[1]))
            rows.append(row)

    return rows
        

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("syntax: get_csv.py <name> <start_ts> <stop_ts>")
        sys.exit(-1)

    metric = sys.argv[1]
    start = sys.argv[2]
    stop = sys.argv[3]

    metrics_json = get_metrics_json(metric, start, stop)

    labels=get_labels(metrics_json)
    labels.append("timestamp")
    labels.append("value")

    print(",".join(labels))

    rows = parse_metrics_json(metrics_json)

    csv_rows = [",".join(x) for x in rows]

    print("\n".join(csv_rows))
