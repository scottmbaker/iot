import json, sys

#x=json.loads(open("all_dg.json").read())

x=json.loads(sys.stdin.read())

x=x["device-group"]

imsis = {}

for dg in x:
    for ir in dg["imsis"]:
        if ("name" in ir) and (ir["name"]):
            # aether-3.0
            irname = ir["name"]
        elif ("display-name" in ir) and (ir["display-name"]):
            # aether-4.0
            irname = ir["display-name"]
        else:
            irname = ir["imsi-id"]

        first = int(ir["imsi-range-from"])
        if ir["imsi-range-to"]:
            last = int(ir["imsi-range-to"])
        else:
            last = first
        if (last != first):
            index=0
            for imsi in range(first, last):
                index += 1
                name = "%s(%d)" % (irname, index)
                imsis[str(imsi)] = name
        else:
            imsi = str(first)
            name = irname
            imsis[imsi] = name

n=1
mappings = []
for k,v in imsis.items():
    mapping = {"id": n,
               "text": v,
               "type": 1,
               "value": k
               }
    mappings.append(mapping)

print(json.dumps(mappings, indent=4))
