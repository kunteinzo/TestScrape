from aiohttp import ClientSession
from asyncio import run

import json

class Api:
    rtk = "AMf-vBzr10X4GLbJpSkwiXSvUISFsrYqtPXq4TRPsvc5XQWazteZFyrLYKgpUuz9_T87VmuFazvcTiJ1CXy_6gjY28YHDcd1aqWy92QZtunauNVajWPaj025LlZsPqb6icWRmsp2UshP3MyTks0215_AEEEB53TTBvQlHTRpiMLwJMRR0n9-60s"
    refresh = "https://api.maharprod.com/profile/v1/RefreshToken"
    plist = "https://api.maharprod.com/display/v1/playlistDetail?id={}&pageNumber=1"
    mhome="https://api.maharprod.com/display/v1/moviebuilder?pageNumber=1"
    mgenres="https://api.maharprod.com/content/v1/Genres?&filter=type+eq+%27movie%27and+status+eq+true&select=nameMm%2CnameEn%2Cid%2Ctype"
    mcat="https://api.maharprod.com/content/v1/MovieFilter?categoryId={_id}&pageNumber=1"
    mdet="https://api.maharprod.com/content/v1/MovieDetail/{_id}"
    mstream="https://api.maharprod.com/revenue/url?type=movie&contentId={_id}&isPremiumUser=true&isPremiumContent=true&source=mobile"
    mdown="https://api.maharprod.com/content/v1/download?type=movie&contentId={_id}&isPremiumUser=true&isPremiumContent=true&fileSize={quality}"

    shome="https://api.maharprod.com/display/v1/seriesbuilder?pageNumber=1",
    sgenres="https://api.maharprod.com/content/v1/Genres?&filter=type+eq+%27series%27and+status+eq+true&select=nameMm%2CnameEn%2Cid%2Ctype"
    scat="https://api.maharprod.com/content/v1/SeriesFilter?categoryId=2d2b4532-1f16-41bd-9a91-42a29222bb2f&pageNumber=1"
    sdet="https://api.maharprod.com/content/v1/SeriesDetail/{}"
    ssession="https://api.maharprod.com/content/v1/Seasons?&filter=seriesId+eq+{}&select=nameMm%2CnameEn%2Cid"
    seps="https://api.maharprod.com/content/v1/Episodes?&filter=status+eq+true+and+seasonId+eq+{}&orderby=sorting+asc&top=6&skip=0"
    sstream="https://api.maharprod.com/revenue/url?type=episodes&contentId=90d3ab39-bb50-4784-ae56-90b0ce07d33e&isPremiumUser=false&isPremiumContent=true&source=mobile"
    sdown="https://api.maharprod.com/content/v1/download?type=episodes&contentId=90d3ab39-bb50-4784-ae56-90b0ce07d33e&isPremiumUser=false&isPremiumContent=true&fileSize=fullHd"

async def fetch(
    method: str, 
    url: str, 
    response_type: str,
    headers: dict = {},
    body: dict = {}
):
    async with ClientSession() as ss:
        async with getattr(ss, method)(url, headers=headers, data=json.dumps(body)) as rp:
            return await getattr(rp, response_type)()

tk = run(fetch('post', Api().refresh, 'json', {"content-type": "application/json"},{"refreshToken": Api().rtk}))['access_token']

print(run(fetch(
    'get',
    Api().mhome,
    'text',
    {
        'authorization': f'Bearer {tk}'
    }
)))

#print(run(fetch("get", api['ser']['eps'].format("2a69ccca-1e6a-4e60-84e9-4f76d90db3ca"), "json", dict(authorization=f"Bearer {tk}"))))
