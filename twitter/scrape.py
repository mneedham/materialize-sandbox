import twint
import sys
import json

module = sys.modules["twint.storage.write"]

def Json(obj, config):
    tweet = obj.__dict__
    print(json.dumps(tweet))

module.Json = Json

c = twint.Config()
c.Near = "London"
c.Search = "Coronavirus OR COVID"
c.Store_json = True
c.Custom["user"] = ["id", "tweet", "user_id", "username", "hashtags", "mentions"]
c.User_full = True
c.Output = "tweets.json"
c.Hide_output = True

twint.run.Search(c)
