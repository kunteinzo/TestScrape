from aiohttp import ClientSession
from asyncio import run

import json


class Api:
    rtk = "AMf-vBzr10X4GLbJpSkwiXSvUISFsrYqtPXq4TRPsvc5XQWazteZFyrLYKgpUuz9_T87VmuFazvcTiJ1CXy_6gjY28YHDcd1aqWy92QZtunauNVajWPaj025LlZsPqb6icWRmsp2UshP3MyTks0215_AEEEB53TTBvQlHTRpiMLwJMRR0n9-60s"
    url_refresh = "https://api.maharprod.com/profile/v1/RefreshToken"
    url_playlist =lambda playlist_id, page_num: f"https://api.maharprod.com/display/v1/playlistDetail?id={playlist_id}&pageNumber={page_num}"

    # I don't know why they put return of /display/*Builder 
    url_movie_home = lambda page_num:  f"https://api.maharprod.com/display/v1/moviebuilder?pageNumber={page_num}"
    url_movie_genres = "https://api.maharprod.com/content/v1/Genres?&filter=type+eq+%27movie%27and+status+eq+true&select=nameMm%2CnameEn%2Cid%2Ctype"
    url_movie_category = lambda category_id, page_num : f"https://api.maharprod.com/content/v1/MovieFilter?categoryId={category_id}&pageNumber={page_num}"
    url_movie_detail = lambda movie_id: f"https://api.maharprod.com/content/v1/MovieDetail/{movie_id}"
    url_movie_stream = lambda content_id : f"https://api.maharprod.com/revenue/url?type=movie&contentId={content_id}&isPremiumUser=true&isPremiumContent=true&source=mobile"
    url_movie_download = lambda content_id, quality: f"https://api.maharprod.com/content/v1/download?type=movie&contentId={content_id}&isPremiumUser=true&isPremiumContent=true&fileSize={quality}"

    # I don't know why they put return of /display/*Builder
    url_series_home = lambda page_num: f"https://api.maharprod.com/display/v1/seriesbuilder?pageNumber={page_num}"
    url_series_genres = "https://api.maharprod.com/content/v1/Genres?&filter=type+eq+%27series%27and+status+eq+true&select=nameMm%2CnameEn%2Cid%2Ctype"
    url_series_category = lambda category_id, page_num: f"https://api.maharprod.com/content/v1/SeriesFilter?categoryId={category_id}&pageNumber={page_num}"
    url_series_detail = lambda series_id: f"https://api.maharprod.com/content/v1/SeriesDetail/{series_id}"
    url_series_season = lambda series_id: f"https://api.maharprod.com/content/v1/Seasons?&filter=seriesId+eq+{series_id}&select=nameMm%2CnameEn%2Cid"
    url_series_episode = lambda season_id, sorting, top, skip: f"https://api.maharprod.com/content/v1/Episodes?&filter=status+eq+true+and+seasonId+eq+{season_id}&orderby=sorting+{sorting}&top={top}&skip={skip}"
    Url_series_stream = lambda content_id : f"https://api.maharprod.com/revenue/url?type=episodes&contentId={content_id}&isPremiumUser=true&isPremiumContent=true&source=mobile"
    url_series_download = lambda content_id, quality : f"https://api.maharprod.com/content/v1/download?type=episodes&contentId={content_id}&isPremiumUser=true&isPremiumContent=true&fileSize={quality}"

