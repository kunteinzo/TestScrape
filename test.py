from main import s_fetch, run, json
from mahar import Api

api = Api()

tk = run(s_fetch('post', api.url_refresh, token='tk', headers={'content-type': 'application/json'},
                 data=json.dumps(dict(refreshToken=api.refresh_token))))['access_token']


movie_genres = run(s_fetch('get', api.url_movie_genres, token=tk))['value']

movie_in_a_genre = run(s_fetch('get', api.url_movie_category(movie_genres[0]['id'], 1), token=tk))['value']

# Movie Home
mov_home = json.loads(run(s_fetch('get', api.url_movie_home(1), 'text', tk)))['value']

playlistId = mov_home[0]['playlistId']

mov_from_playlist = run(s_fetch('get', api.url_playlist(playlistId, 1), token=tk))['value']

movieId = mov_from_playlist[0]['id']

movieDetail = run(s_fetch('get', api.url_movie_detail(movieId), token=tk))['value']

mov_contentId = movieDetail['contentId']

movieStream = run(s_fetch('get', api.url_movie_stream(mov_contentId), token=tk))

movieDownloadLink = run(s_fetch('get', api.url_movie_download(mov_contentId, 'hd'), token=tk))

# todo: series stuff
