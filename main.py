import requests, aiohttp, json, asyncio

def testc(n):
    r = requests.get(
        f"https://95tv.live/api/client/v1/content/display/movie/items?page={n}&length=10",
        headers={
            "platform": "android",
            "version": "1"
        }
    )
    return r.status_code
    mov = json.loads(r.content)
    tem = "Name: {}\nPoster: {}\nYear: {}\nThumbnail: {}\nVote: {}\nSynopsis: {}"
#    print(tem.format(
#        mov['name'],
#        mov['domainImage']+'/'+mov['poster'],
#        mov['prodYear'],
#        mov['domainImage']+'/'+mov['thumbnail'],
#        mov['vote'],
#        mov['synopsis'].strip()
#    ))

async def root_movie_fetch(outputfile: str|None = None):
    async with aiohttp.ClientSession() as ses:
        async def mfetch(n, sess):
            async with sess.get(f"https://95tv.live/api/client/v1/content/display/movie/items?page={n}&length=10", headers={'platform': 'android', 'version': '1'}) as rep:
                return await rep.json()
        urls = [n for n in range(0, 175)]
        tasks = [mfetch(url, ses) for url in urls]
        results = await asyncio.gather(*tasks)
        fin = []
        for r in results:
            fin += r
        if outputfile:
            with open(outputfile, "w") as f:
                f.write(json.dumps(fin))
        else:
            print(json.dumps(fin))
        return fin

async def mov_content_fetch(url, text: bool = False):
    async with aiohttp.ClientSession() as ses:
        async with ses.get(url, headers=dict(platform='android', version='1')) as rep:
            if text:
                return await rep.text()
            return await rep.json()

def testc1():
    n = 0
    while True:
        if testc(n) == 200:
            print(n)
        else:
            break
        n += 1


#asyncio.run(root_movie_fetch())
#print(asyncio.run(mov_content_fetch("https://95tv.live/api/client/v1/content/movies/Mxbj34UHg")))
#print(asyncio.run(mov_content_fetch("https://95tv.live/api/client/v1/content/movies/Mxbj34UHg/link")))
print(asyncio.run(mov_content_fetch("https://vod.95tv.live/public/uploads/2025/07/14/7b9dc785-c593-4671-9e92-bfa03df8fe14/Dcyge48Ng/index.m3u8?signKey=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb250ZW50SUQiOiJEY3lnZTQ4TmcifQ.jbFNpH5B2LzSfVLNMcsAdutfbs0dHiueZyFEjhVygpo", True)))

