from aiohttp import ClientSession
from asyncio import run

import json


class Api:

    url_req_code = "https://api.maharprod.com/sms/v1/movie/telenor/atom_sms"
    # body {"phoneNumber": "959***"}
    url_verify = "https://api.maharprod.com/profile/v1/PhoneNumber/phLogin"
    """ body
    {
    "phoneNumber": "959***",
    "otpno": "123456",
	"fcmToken": "fsr5oyChR5SSpOX9qQMO_K:APA91bFjfv4L2LcMCnKCA_94UdEKM6T3EzIbHRAgxBG7CXy68qxFSmIIyG7QNym_nOgCKQO6ujsUvRaPfmMAD_nC0Sh2gkOK7eN1VG3-hlKuoUUvxLioRmM",
	"deviceId": "",
	"deviceName": "I Phone 20 Pro Max ++",
	"deviceType": "superuser",
	"mobileCarrier": "",
	"os": "Linux",
	"osVersion": "1500",
	"operatorName": "Ball Ma"
	}"""

    url_live = "https://api.maharprod.com/content/v1/titles?select=id,titleEn,titleMm,descriptionEn,descriptionMm,type,isPremium,resolution,rating,sorting,status&filter=type%20eq%20'channel'&expand=media(select=imageType,image),channel(select=streamingUrl)"

    refresh_token = "AMf-vBwNKNmDEzv4BXB8X2s50f-TLJJG3qpf_UuhaobP8jmtm2wbj5hSf1OgE1vuPia3nV8_D2ksrJ-FyETShA6sciBh2UiOhZxFpPmFZs6SL5jsPsG5ptmVxIKopcFiuUxYXxbVN68N5JuDEqMd68HZH8UY_rtWIvofEq0y4v5eP7GEzVXil0Y"
    url_refresh = "https://api.maharprod.com/profile/v1/RefreshToken"
    url_playlist = lambda self, playlist_id, page_num: f"https://api.maharprod.com/display/v1/playlistDetail?id={playlist_id}&pageNumber={page_num}"

    # I don't know why they put return of /display/*Builder 
    url_movie_home = lambda self, page_num:  f"https://api.maharprod.com/display/v1/moviebuilder?pageNumber={page_num}"
    url_movie_genres = "https://api.maharprod.com/content/v1/Genres?&filter=type+eq+%27movie%27and+status+eq+true&select=nameMm%2CnameEn%2Cid%2Ctype"
    url_movie_category = lambda self, category_id, page_num : f"https://api.maharprod.com/content/v1/MovieFilter?categoryId={category_id}&pageNumber={page_num}"
    url_movie_detail = lambda self, movie_id: f"https://api.maharprod.com/content/v1/MovieDetail/{movie_id}"
    url_movie_stream = lambda self, content_id : f"https://api.maharprod.com/revenue/url?type=movie&contentId={content_id}&isPremiumUser=true&isPremiumContent=true&source=mobile"
    url_movie_download = lambda self, content_id, quality: f"https://api.maharprod.com/content/v1/download?type=movie&contentId={content_id}&isPremiumUser=true&isPremiumContent=true&fileSize={quality}"

    # I don't know why they put return of /display/*Builder
    url_series_home = lambda self, page_num: f"https://api.maharprod.com/display/v1/seriesbuilder?pageNumber={page_num}"
    url_series_genres = "https://api.maharprod.com/content/v1/Genres?&filter=type+eq+%27series%27and+status+eq+true&select=nameMm%2CnameEn%2Cid%2Ctype"
    url_series_category = lambda self, category_id, page_num: f"https://api.maharprod.com/content/v1/SeriesFilter?categoryId={category_id}&pageNumber={page_num}"
    url_series_detail = lambda self, series_id: f"https://api.maharprod.com/content/v1/SeriesDetail/{series_id}"
    url_series_season = lambda self, series_id: f"https://api.maharprod.com/content/v1/Seasons?&filter=seriesId+eq+{series_id}&select=nameMm%2CnameEn%2Cid"
    url_series_episode = lambda self, season_id, sorting, top, skip: f"https://api.maharprod.com/content/v1/Episodes?&filter=status+eq+true+and+seasonId+eq+{season_id}&orderby=sorting+{sorting}&top={top}&skip={skip}"
    Url_series_stream = lambda self, content_id : f"https://api.maharprod.com/revenue/url?type=episodes&contentId={content_id}&isPremiumUser=true&isPremiumContent=true&source=mobile"
    url_series_download = lambda self, content_id, quality : f"https://api.maharprod.com/content/v1/download?type=episodes&contentId={content_id}&isPremiumUser=true&isPremiumContent=true&fileSize={quality}"

