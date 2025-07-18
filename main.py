from typing import Any
from aiohttp import ClientSession
import json, asyncio


async def fetch_task(urls, mistext: bool = False):
    async with ClientSession() as session:
        async def mf(u, s, istext: bool = False, headers: dict | None = None):
            async with s.get(u, headers=headers) as response:
                if istext:
                    return await response.text()
                return await response.json()

        return await asyncio.gather(*[mf(url, session, mistext, dict(platform="android", version="1")) for url in urls])


async def content_fetch(url, text: bool | None = False):
    async with ClientSession() as ses:
        async with ses.get(url, headers=dict(platform='android', version='1')) as rep:
            if text is None:
                return await rep.read()
            if text:
                return await rep.text()
            return await rep.json()


root = []
r = asyncio.run(fetch_task(
    [f"https://95tv.live/api/client/v1/content/display/movie/items?page={u}&length=10" for u in range(0, 175)]))
for rr in r:
    root.extend(rr)
fin = []
for dat in root:
    new = dict(
        id=dat['id'],
        name=dat['name'],
        is_series=dat['isSeries'],
        is_subtitle=dat['isSubtitle'],
        year=dat['prodYear'],
        description=dat['synopsis'],
        type=dat['type'],
        rate=dat['vote'],
        poster=dat['domainImage'] + "/" + dat['poster'],
        thumbnail=dat['domainImage'] + "/" + dat['thumbnail']
    )
    fin.append(new)
    break

r2 = asyncio.run(fetch_task([f"https://95tv.live/api/client/v1/content/movies/{mov['id']}" for mov in fin]))
for rr in r2:
    print(dict(
        id=rr['id'],
        duration=rr['duration'],
        rate=rr['vote'],
        name=rr['name'],
        description=rr['synopsis'],
        is_series=rr['isSeries'],
        year=rr['prodYear'],
        poster=rr['domainImage'] + "/" + rr['poster'],
        thumbnail=rr['domainImage'] + "/" + rr['thumbnail']
    ))
    break

r3 = asyncio.run(fetch_task([f"https://95tv.live/api/client/v1/content/movies/{u['id']}/link" for u in r2]))
test1 = {}
for rr in r3:
    test1 = dict(
        name=rr['name'],
        thumbnail=rr['domainImage'] + "/" + rr['thumbnail'],
        src=rr['domainVideo'] + "/" + rr['link']
    )
r4 = asyncio.run(content_fetch(test1['src'].replace('index.m3u8', '720/index.m3u8'), True))

with open("test.m3u8", "w") as f:
    f.write(r4)

# content = asyncio.run(mov_content_fetch("https://95tv.live/api/client/v1/content/movies/Mxbj34UHg"))
# link = asyncio.run(mov_content_fetch("https://95tv.live/api/client/v1/content/movies/Mxbj34UHg/link"))
# print(asyncio.run(mov_content_fetch("https://vod.95tv.live/public/uploads/2025/07/14/7b9dc785-c593-4671-9e92-bfa03df8fe14/Dcyge48Ng/index.m3u8?signKey=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb250ZW50SUQiOiJEY3lnZTQ4TmcifQ.jbFNpH5B2LzSfVLNMcsAdutfbs0dHiueZyFEjhVygpo", True)))
