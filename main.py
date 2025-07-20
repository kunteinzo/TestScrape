import json

from aiohttp import ClientSession
from asyncio import run, gather


async def as_fetch(method: str, url: str, response_type: str, headers: dict | None = None, body: dict | None = None):
    async with ClientSession() as session:
        async with getattr(session, method)(url, headers=headers, data=json.dumps(body)) as response:
            return await getattr(response, response_type)()


def fetch(method: str, url: str, response_type: str, headers: dict | None = None, body: dict | None = None):
    return run(as_fetch(method, url, response_type, headers, body))


async def fetch_task(urls, mistext: bool = False):
    async with ClientSession() as session:
        async def mf(u, s, istext: bool = False, headers: dict | None = None):
            async with s.get(u, headers=headers) as response:
                if istext:
                    return await response.text()
                return await response.json()

        return await gather(*[mf(url, session, mistext, dict(platform="android", version="1")) for url in urls])


movies = fetch('get',
               "https://95tv.live/api/client/v1/content/display/movie/items?page=0&length=10",
               'json',
               dict(platform='android', version='1'))

movie = movies[1]

movie_detail = fetch('get', f"https://95tv.live/api/client/v1/content/movies/{movie['id']}",
                     'json',
                     dict(platform='android', version='1'))

movie_link = fetch('get', f"https://95tv.live/api/client/v1/content/movies/{movie['id']}/link",
                   'json',
                   dict(platform='android', version='1'))

link = movie_link['domainVideo']+'/'+movie_link['link']

print(link)

m3u8 = fetch('get', link.replace('index.m3u8', '480/index.m3u8'), 'text', dict(platform='android', version='1'))

# print(m3u8)

key = fetch('post', 'https://drm.95tv.live/key/vod', 'text', dict(platform='android', version='1'))

print(key)

"""
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:10
#EXT-X-MEDIA-SEQUENCE:0
#EXT-X-PLAYLIST-TYPE:VOD
#EXT-X-KEY:METHOD=AES-128,URI="https://drm.95tv.live/key/vod",IV=0x00000000000000000000000000000000
#EXTINF:10.000000,
480p_000.ts
"""


"""
root = []
r = asyncio.run(fetch_task(
        [f"https://95tv.live/api/client/v1/content/display/movie/items?page={u}&length=10" for u in range(0, 175)],
        True
    )
)
for rr in r:
    try:
        root.extend(json.loads(rr))
    except Exception as e:
        print(e)
        break
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
"""
