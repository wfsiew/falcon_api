import decimal, datetime, json

def tojson(s):
    return json.dumps(s, ensure_ascii=False)