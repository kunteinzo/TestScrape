import json
from asyncio import run, gather

from aiohttp import ClientSession


async def fetch_task(urls, mistext: bool = False):
    async with ClientSession() as session:
        async def mf(u: str, s: ClientSession, istext: bool = False, headers: dict | None = None):
            async with s.get(u, headers=headers) as response:
                if istext:
                    return await response.text()
                return await response.json()

        return await gather(*[mf(url, session, mistext, dict(platform="android-mobile", version="87")) for url in urls])


async def fetch(
        method: str,
        url: str,
        content: str = 'json',
        token: str = "",
        headers: dict | None = None,
        data: dict | None = None
):
    hrs = headers or {}
    hrs['authorization'] = f"Bearer {token}"
    async with ClientSession() as ses:
        async with getattr(ses, method)(url, headers=hrs, data=json.dumps(data)) as rep:
            return await getattr(rep, content)()


def refresh_token():
    return run(
        fetch(
            "post",
            "https://api.maharprod.com/profile/v1/RefreshToken",
            headers={
                "accept-encoding": "gzip",
                "content-type": "application/json",
                "authorization": "Bearer tk"
            },
            data={
                "refreshToken": "AMf-vBzr10X4GLbJpSkwiXSvUISFsrYqtPXq4TRPsvc5XQWazteZFyrLYKgpUuz9_T87VmuFazvcTiJ1CXy_6gjY28YHDcd1aqWy92QZtunauNVajWPaj025LlZsPqb6icWRmsp2UshP3MyTks0215_AEEEB53TTBvQlHTRpiMLwJMRR0n9-60s"
            }
        )
    )['access_token']


def movie_home():
    return json.loads(run(
        fetch("get",
              "https://api.maharprod.com/display/v1/moviebuilder?pageNumber=1",
              token=refresh_token(),
              content='text'
              )
    ))


def movie_category(_id: str = "00d8504d-8935-490e-962e-f4bf4a3d9eac"):
    return run(
        fetch(
            "get",
            f"https://api.maharprod.com/content/v1/MovieFilter?categoryId={_id}&pageNumber=1",
            token=refresh_token()
        )
    )


def movie_detail(_id: str = "165b9620-9db9-48b9-a624-f5ad5d070d73"):
    return run(
        fetch(
            "get",
            f"https://api.maharprod.com/content/v1/MovieDetail/{_id}",
            token=refresh_token()
        )
    )


def movie_stream(_id: str = "7e9dbc93-a4a9-4e7a-81f5-cd981f445e88"):
    return run(
        fetch(
            "get",
            f"https://api.maharprod.com/revenue/url?type=movie&contentId={_id}&isPremiumUser=true&isPremiumContent=true&source=mobile",
            token=refresh_token()
        )
    )


def movie_download(_id: str = "7e9dbc93-a4a9-4e7a-81f5-cd981f445e88", quality: str = "fullHd"):
    return run(
        fetch(
            "get",
            f"https://api.maharprod.com/content/v1/download?type=movie&contentId={_id}&isPremiumUser=true&isPremiumContent=true&fileSize={quality}",
            token=refresh_token()
        )
    )



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

with open('test.txt', 'w') as f:
    f.write(
        "Home:\n" +
        json.dumps(movie_home()) + '\n\nCategory:\n' +
        json.dumps(movie_category()) + '\n\nDetail:\n' +
        json.dumps(movie_detail()) + '\n\nStream:\n' +
        json.dumps(movie_stream()) + '\n\nDownload:\n' +
        json.dumps(movie_download())
    )
