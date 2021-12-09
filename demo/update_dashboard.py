import json, sys

x=json.loads(sys.stdin.read())

mappings=json.loads(open("value_mappings.json").read())

LOOKFOR = ["menlo-4g-phone-office-pixel", "sentinel"]

updates = 0
for panel_index,panel in enumerate(x["panels"]):
    if not "fieldConfig" in panel:
        continue
    if not "defaults" in panel["fieldConfig"]:
        continue
    if not "mappings" in panel["fieldConfig"]["defaults"]:
        continue
    found = False
    for mapping in panel["fieldConfig"]["defaults"]["mappings"]:
        if mapping["text"] in LOOKFOR:
            found = True
    if not found:
        continue
    x["panels"][panel_index]["fieldConfig"]["defaults"]["mappings"] = mappings
    updates += 1

sys.stderr.write("%d tables updated\n" % updates)

chartUpdates = 0
for panel_index, panel in enumerate(x["panels"]):
    if not "fieldConfig" in panel:
        continue
    if not "overrides" in panel["fieldConfig"]:
        continue
    found = False
    for override in panel["fieldConfig"]["overrides"]:
        if "properties" not in override:
            continue
        for property in override["properties"]:
            if "id" not in property:
                continue
            if "value" not in property:
                continue
            if property["value"] in LOOKFOR:
                found = True
    if not found:
        continue

    chartUpdates += 1
    overrides = []
    for mapping in mappings:
        overrides.append(
          {
            "matcher": {
              "id": "byName",
              "options": mapping["value"]
            },
            "properties": [
              {
                "id": "displayName",
                "value": mapping["text"]
              }
            ]
          }
        )
    x["panels"][panel_index]["fieldConfig"]["overrides"] = overrides

sys.stderr.write("%d charts updated\n" % chartUpdates)

sys.stdout.write(json.dumps(x, indent=4))

if (updates==0):
    sys.stdout.write("mappings not found\n")
    sys.exit(-1)
