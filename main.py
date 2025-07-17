from aiohttp import ClientSession
from asyncio import run, gather
import json, asyncio


async def fetch_task(urls, mistext: bool = False):
    async with ClientSession() as session:
        async def mf(u, s, istext: bool = False, headers: dict|None = None):
            async with s.get(u, headers=headers) as response:
                if istext:
                    return await response.text()
                return await response.json()
        return await gather(*[mf(url, session, mistext, dict(platform="android-mobile", version="87")) for url in urls])


async def fetch(url, headers: dict|None = None, data: dict|None = None, isget: bool = True, text: bool|None = False):
    async with ClientSession() as ses:
        if isget:
            async with ses.get(url, headers=headers, data=data) as rep:
                if text == None:
                    return await rep.read()
                if text:
                    return await rep.text()
                return await rep.json()
        else:
            async with ses.post(url, headers=headers, data=data) as rep:
                if text == None:
                    return await rep.read()
                if text:
                    return await rep.text()
                return await rep.json()


def refresh_token():
    return run(fetch(
        "https://api.maharprod.com/profile/v1/RefreshToken",
        headers={
            "accept-encoding": "gzip",
            "content-type": "application/json",
            "authorization": "Bearer tk"
        },
        data=json.dumps({
            "refreshToken": ""
        }),
        isget=False
    ))['access_token']

def movie_home():
    return json.loads(run(
        fetch(
            "https://api.maharprod.com/display/v1/moviebuilder?pageNumber=1",
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {refresh_token()}"
            },
            text=True
        )
    ))

def mov_cat(_id: str = "00d8504d-8935-490e-962e-f4bf4a3d9eac"):
    return run(fetch(
        f"https://api.maharprod.com/content/v1/MovieFilter?categoryId={_id}&pageNumber=1",
        headers={ "authorization": f"Bearer {refresh_token()}" }
    ))

def mov_detail(_id:str = "165b9620-9db9-48b9-a624-f5ad5d070d73"):
    return run(
        fetch(
            f"https://api.maharprod.com/content/v1/MovieDetail/{_id}",
            headers={ "authorization": f"Bearer {refresh_token()}"}
        )
    )

def mov_stream(_id: str = "7e9dbc93-a4a9-4e7a-81f5-cd981f445e88"):
    return run(
        fetch(
            f"https://api.maharprod.com/revenue/url?type=movie&contentId={_id}&isPremiumUser=true&isPremiumContent=true&source=mobile",
            headers={ "authorization": f"Bearer {refresh_token()}"}
        )
    )
# Stream
# https://api.maharprod.com/revenue/url?type=movie&contentId=7e9dbc93-a4a9-4e7a-81f5-cd981f445e88&isPremiumUser=true&isPremiumContent=true&source=mobile

def mov_down(_id: str = "7e9dbc93-a4a9-4e7a-81f5-cd981f445e88", quality: str = "fullHd"):
    return run(
        fetch(
            f"https://api.maharprod.com/content/v1/download?type=movie&contentId={_id}&isPremiumUser=true&isPremiumContent=true&fileSize={quality}",
            headers={ "authorization": f"Bearer {refresh_token()}"}
        )
    )

# Download
# https://api.maharprod.com/content/v1/download?type=movie&contentId=7e9dbc93-a4a9-4e7a-81f5-cd981f445e88&isPremiumUser=true&isPremiumContent=true&fileSize=fullHd


# Series Home
# https://api.maharprod.com/display/v1/seriesbuilder?pageNumber=1

# Latest List
# https://api.maharprod.com/display/v1/playlistDetail?id=43e33141-d488-4fe6-bae8-9a3cdfc7f972&pageNumber=1

# Series Details
# https://api.maharprod.com/content/v1/SeriesDetail/c2a856b0-e9be-401e-9f35-022274d68b08

# Series Season 
# https://api.maharprod.com/content/v1/Seasons?&filter=seriesId+eq+2f919008-d882-4389-9d98-cb212ec3407c&select=nameMm%2CnameEn%2Cid

# Series Ep
# https://api.maharprod.com/content/v1/Episodes?&filter=status+eq+true+and+seasonId+eq+6a1e7c87-2ff8-492e-8e5b-7862773e4df1&orderby=sorting+asc&top=6&skip=0

print(mov_down())
