import json;print(json.dumps([p['slug'][6:] for p in json.load(open('posts.json')) if p['slug'].startswith('video-')]))
