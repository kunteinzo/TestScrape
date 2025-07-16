import json, time

with open("original.json") as f, open("newroot.json", "w") as f1:
    data = json.loads(f.read())
    fin = []
    po = 1
    total = len(data)
    for dat in data:
        new = dict(
            id=dat['id'],
            name=dat['name'],
            is_series=dat['isSeries'],
            is_subtitle=dat['isSubtitle'],
            year=dat['prodYear'],
            description=dat['synopsis'],
            type=dat['type'],
            rate=dat['vote'],
            poster=dat['domainImage']+"/"+dat['poster'],
            thumbnail=dat['domainImage']+"/"+dat['thumbnail']
        )
        fin.append(new)
        print("Process: {:.2f}%".format((po/total)*100))
        po += 1
    f1.write(json.dumps(fin))