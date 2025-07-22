from main import s_fetch, run, json
from mahar import Api

api = Api()

tk = run(s_fetch('post', api.url_refresh, token='tk', headers={'content-type': 'application/json'},
                 data=json.dumps(dict(refreshToken=api.refresh_token))))['access_token']

print(run(s_fetch('get', api.url_movie_home(1), 'text', tk)))
