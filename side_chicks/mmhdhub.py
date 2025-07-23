import aiohttp, asyncio, requests, re, yt_dlp, json
from bs4 import BeautifulSoup
from os.path import abspath, join


async def fetch(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as rp:
        return await rp.text()


async def query(urls: list):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*[fetch(session, url) for url in urls])


mp = BeautifulSoup(requests.get('https://mmhdhub.com').content, 'html.parser').find('a', string="Last").get('href')

mp = int(mp[mp.rindex('/') + 1:])

# for p in range(1,mp+1)

rpgs = [
    [
        href.get('href')
        for href in BeautifulSoup(pg, 'html.parser').find_all('a', href=re.compile('https://mmhdhub.com/archives'))
    ]
    for pg in asyncio.run(query([
        "https://mmhdhub.com/?filter=latest" if p < 2 else f"https://mmhdhub.com/page/{p}/?filter=latest"
        for p in range(1, mp + 1)
    ]))
]

pages = []

for rpg in rpgs:
    pages.extend(rpg)

for pg in pages:
    root = BeautifulSoup(requests.get(pg).content, 'html.parser')
    print('Check', root.find('title'))
    title = root.find('strong', class_='bread-current').get('title')
    with yt_dlp.YoutubeDL() as ydl:
        tmp_file = join(abspath('.'), 'tmp.json')
        with open(tmp_file, 'w') as f:
            f.write(json.dumps(ydl.sanitize_info(ydl.extract_info(root.find('iframe').get('src')))))
        err = ydl.download_with_info_file(tmp_file)
        if err:
            print('Download error')
            exit(err)
        print("Downloaded")
    break
