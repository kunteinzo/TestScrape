from typing import Any
from aiohttp import ClientSession
import json, asyncio


async def fetch_task(urls, mistext: bool = False):
    async with ClientSession() as session:
        async def mf(u, s, istext: bool = False, headers: dict|None = None):
            async with s.get(u, headers=headers) as response:
                if istext:
                    return await response.text()
                return await response.json()
        return await asyncio.gather(*[mf(url, session, mistext, dict(platform="android-mobile", version="87")) for url in urls])


async def fetch(url, headers: dict|None = None, data: dict|None = None, isget: bool = True, text: bool|None = False):
    async with ClientSession() as ses:
        if isget:
            async with ses.get(url, headers=headers) as rep:
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
    return asyncio.run(fetch(
        "https://api.maharprod.com/profile/v1/RefreshToken",
        headers={
            "accept-encoding": "gzip",
            "content-type": "application/json",
            "authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImE4ZGY2MmQzYTBhNDRlM2RmY2RjYWZjNmRhMTM4Mzc3NDU5ZjliMDEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vbWFoYXItY2MyOTMiLCJhdWQiOiJtYWhhci1jYzI5MyIsImF1dGhfdGltZSI6MTc1MTY5NjQxNiwidXNlcl9pZCI6Ijg4Y2E2ZTRjLTVlMjctNGM3Ni1hNTJmLTVlYWQwZWVhOGU0NCIsInN1YiI6Ijg4Y2E2ZTRjLTVlMjctNGM3Ni1hNTJmLTVlYWQwZWVhOGU0NCIsImlhdCI6MTc1MjcyNzIxOCwiZXhwIjoxNzUyNzMwODE4LCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7fSwic2lnbl9pbl9wcm92aWRlciI6ImN1c3RvbSJ9fQ.A-NISGkr_tIo4beS_2Lu5o4lp5wIsFxqv1Mg7xcqxRh0vlNgdB1om0HXW2yEYn1Xs-6gWFQqTMmRInchANn8ND0OJ-jyHvMrsnEOUR5NI-_GzT80TeMVcn_soZHz17dz0p7QM5BsRZhHRGonGvNMPx3hqJi6VdMOZscX1F3YdU1LjZ53XODtOwNZR4qkj6d62G6gtzWQBIBE3Z3NsPQlEy5lvgdFNvBUlQVKoDKJ1Vnle3zZVKzaWu5YiO5ruCp_OQuvP4qWP84faA6UatIwJkNJUeR-wMGxfgsTd7BzsL1wscEkgUYmrWRVMcQjMof6O_vMaM2URPfeD8PZ-jOXSw"
        },
        data=json.dumps({
            "refreshToken": "AMf-vBw4ehKn9frVEAvte_UkLSjIuntAgzC-b9wMJbEkDcyiXv5HdS-0aiJRPC3BfbEmTanxhPC_dKzwlSllYGEio08xqlUpcUpstzOfmRAWia6vp4kwim6m0XSqxaTtOGOca16Dbm54sKDjnxozhv9kw-RdSvJZVkYUDRmp-2jvymU_Aq7GgNFqigQ9Unv2lR3S7Lc8CJsy"
        }),
        isget=False
    ))

def movie_home():
    return json.loads(asyncio.run(
        fetch(
            "https://api.maharprod.com/display/v1/moviebuilder?pageNumber=1",
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {refresh_token()['access_token']}"
            },
            text=True
        )
    ))

def mov_detail():
    return asyncio.run(
        fetch(
            "https://api.maharprod.com/content/v1/MovieDetail/165b9620-9db9-48b9-a624-f5ad5d070d73",
            headers={
                "authorization": f"Bearer {refresh_token()['access_token']}"
            }
        )
    )

print(mov_detail())
