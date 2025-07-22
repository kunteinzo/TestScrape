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


async def s_fetch(
        method: str,
        url: str,
        content: str = 'json',
        token: str|None = None,
        headers: dict | None = None,
        data: dict | str | None = None
):
    hrs = None
    if token:
        hrs = headers or {}
        hrs['authorization'] = f"Bearer {token}"
    async with ClientSession() as ses:
        async with getattr(ses, method)(url, headers=hrs, data=data) as rep:
            return await getattr(rep, content)()


def refresh_token():
    return run(s_fetch(
        "post", "https://api.maharprod.com/profile/v1/RefreshToken",
        headers={"content-type": "application/json", "authorization": "Bearer tk"},
        data={
            "refreshToken": "AMf-vBzr10X4GLbJpSkwiXSvUISFsrYqtPXq4TRPsvc5XQWazteZFyrLYKgpUuz9_T87VmuFazvcTiJ1CXy_6gjY28YHDcd1aqWy92QZtunauNVajWPaj025LlZsPqb6icWRmsp2UshP3MyTks0215_AEEEB53TTBvQlHTRpiMLwJMRR0n9-60s"}
    ))


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
