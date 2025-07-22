import json
from asyncio import run, gather

from aiohttp import ClientSession


async def c_fetch(
        url: str,
        session: ClientSession,
        method: str = 'get',
        response_type: str = 'json',
        headers: dict | None = None,
        data: dict | str | None = None
):
    async with getattr(session, method)(url, headers=headers, data=data) as response:
        return await getattr(response, response_type)()


async def fetch_task(urls):
    async with ClientSession() as session:
        return await gather(
            *[c_fetch(url, session, headers=dict(platform="android-mobile", version="87")) for url in urls])


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
    return run(fetch(
        "post", "https://api.maharprod.com/profile/v1/RefreshToken",
        headers={"content-type": "application/json", "authorization": "Bearer tk"},
        data={
            "refreshToken": "AMf-vBzr10X4GLbJpSkwiXSvUISFsrYqtPXq4TRPsvc5XQWazteZFyrLYKgpUuz9_T87VmuFazvcTiJ1CXy_6gjY28YHDcd1aqWy92QZtunauNVajWPaj025LlZsPqb6icWRmsp2UshP3MyTks0215_AEEEB53TTBvQlHTRpiMLwJMRR0n9-60s"}
    ))['access_token']


def movie_home():
    return json.loads(run(
        fetch("get",
              "https://api.maharprod.com/display/v1/moviebuilder?pageNumber=1",
              token=refresh_token(),
              content='text'
              )
    ))


def movie_genres():
    return run(
        fetch(
            "get",
            "https://api.maharprod.com/content/v1/Genres?&filter=type+eq+%27movie%27and+status+eq+true&select=nameMm%2CnameEn%2Cid%2Ctype",
            token=refresh_token()
        )
    )


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


# Series Genres
# https://api.maharprod.com/content/v1/Genres?&filter=type+eq+%27series%27and+status+eq+true&select=nameMm%2CnameEn%2Cid%2Ctype

# Series Gen
# https://api.maharprod.com/content/v1/SeriesFilter?categoryId=2d2b4532-1f16-41bd-9a91-42a29222bb2f&pageNumber=1

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

# Ep download
# https://api.maharprod.com/content/v1/download?type=episodes&contentId=90d3ab39-bb50-4784-ae56-90b0ce07d33e&isPremiumUser=false&isPremiumContent=true&fileSize=fullHd

# Ep Stream
# https://api.maharprod.com/revenue/url?type=episodes&contentId=90d3ab39-bb50-4784-ae56-90b0ce07d33e&isPremiumUser=false&isPremiumContent=true&source=mobile

print(movie_genres())

# Auth stuff
# https://api.maharprod.com/sms/v1/movie/telenor/atom_sms
# {"phoneNumber": "959***"}

# https://api.maharprod.com/profile/v1/PhoneNumber/phLogin
# {
#  "phoneNumber": "959***",
#  "otpno": "123456",
#  "fcmToken": "fsr5oyChR5SSpOX9qQMO_K:APA91bFjfv4L2LcMCnKCA_94UdEKM6T3EzIbHRAgxBG7CXy68qxFSmIIyG7QNym_nOgCKQO6ujsUvRaPfmMAD_nC0Sh2gkOK7eN1VG3-hlKuoUUvxLioRmM",
#  "deviceId": "",
#  "deviceName": "I Phone 20 Pro Max ++",
#  "deviceType": "superuser",
#  "mobileCarrier": "",
#  "os": "Linux",
#  "osVersion": "1500",
#  "operatorName": "Ball Ma"
# }

# https://api.maharprod.com/profile/v1/Profiles/85ecb8a3-1a40-4fff-adaf-5bebeb91b0b0?%24select=id%2Ctype%2Cemail%2CphoneNumber%2Cname%2Cnumber%2CdateOfBirth%2Cgender%2CimageUrl%2Cstatus%2Clocation%2CdisplayName


# Mahar Live

# https://api.maharprod.com/content/v1/titles?select=id,titleEn,titleMm,descriptionEn,descriptionMm,type,isPremium,resolution,rating,sorting,status&filter=type%20eq%20'channel'&expand=media(select=imageType,image),channel(select=streamingUrl)
