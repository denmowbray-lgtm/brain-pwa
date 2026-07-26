#!/usr/bin/env python3
# skin-patch-p2.py — Phase 2: Mission Control skin + embedded=1 mode into 4 satellites; Deck v7.2 passes embedded=1
import json,urllib.request,base64
JWT="__JWT__"
H={"X-N8N-API-KEY":JWT,"Content-Type":"application/json"}
API="http://localhost:5678/api/v1/workflows/"
SK=json.loads(base64.b64decode("eyJyZWFjdG9yIjogIjxzdHlsZSBpZD1cIm1jLXNraW5cIj46cm9vdHstLWJnOiMwMDA7LS1jeTojNDNlNWZmOy0tY3kyOiM0M2U1ZmY7LS1zYW5zOnVpLW1vbm9zcGFjZSxcIlNGIE1vbm9cIixcIkpldEJyYWlucyBNb25vXCIsTWVubG8sQ29uc29sYXMsbW9ub3NwYWNlfWh0bWwsYm9keXtiYWNrZ3JvdW5kOiMwMDAhaW1wb3J0YW50fWJvZHk6OmJlZm9yZXtiYWNrZ3JvdW5kOnJhZGlhbC1ncmFkaWVudCgxMjAwcHggNTYwcHggYXQgNTAlIC04JSxyZ2JhKDY3LDIyOSwyNTUsLjA3KSx0cmFuc3BhcmVudCA2MCUpIWltcG9ydGFudDthbmltYXRpb246bm9uZSFpbXBvcnRhbnR9Lm1jLWVtYiAudG9we2Rpc3BsYXk6bm9uZX08L3N0eWxlPjxzY3JpcHQ+KGZ1bmN0aW9uKCl7dHJ5e2lmKG5ldyBVUkxTZWFyY2hQYXJhbXMobG9jYXRpb24uc2VhcmNoKS5nZXQoXCJlbWJlZGRlZFwiKT09PVwiMVwiKWRvY3VtZW50LmRvY3VtZW50RWxlbWVudC5jbGFzc0xpc3QuYWRkKFwibWMtZW1iXCIpO31jYXRjaChlKXt9fSkoKTs8L3NjcmlwdD4iLCAic2VjdXJpdHkiOiAiPHN0eWxlIGlkPVwibWMtc2tpblwiPjpyb290ey0tYWNjZW50OiM0M2U1ZmY7LS1vazojMzRlMGEwOy0taW5rOiNkYmU3ZjI7LS1tdXQ6IzY0NzY4OX1odG1sLGJvZHl7YmFja2dyb3VuZDojMDAwIHJhZGlhbC1ncmFkaWVudCgxMjAwcHggNTYwcHggYXQgNTAlIC04JSxyZ2JhKDY3LDIyOSwyNTUsLjA3KSx0cmFuc3BhcmVudCA2MCUpIWltcG9ydGFudDtiYWNrZ3JvdW5kLWF0dGFjaG1lbnQ6Zml4ZWQhaW1wb3J0YW50O2ZvbnQtZmFtaWx5OnVpLW1vbm9zcGFjZSxcIlNGIE1vbm9cIixcIkpldEJyYWlucyBNb25vXCIsTWVubG8sQ29uc29sYXMsbW9ub3NwYWNlIWltcG9ydGFudH0ubWMtZW1iIC50b3B7ZGlzcGxheTpub25lfTwvc3R5bGU+PHNjcmlwdD4oZnVuY3Rpb24oKXt0cnl7aWYobmV3IFVSTFNlYXJjaFBhcmFtcyhsb2NhdGlvbi5zZWFyY2gpLmdldChcImVtYmVkZGVkXCIpPT09XCIxXCIpZG9jdW1lbnQuZG9jdW1lbnRFbGVtZW50LmNsYXNzTGlzdC5hZGQoXCJtYy1lbWJcIik7fWNhdGNoKGUpe319KSgpOzwvc2NyaXB0PiIsICJqYXJ2aXMiOiAiPHN0eWxlIGlkPVwibWMtc2tpblwiPjpyb290ey0tYmc6IzAwMDstLXN1cmY6IzBiMTIxYjstLWxpbmU6IzE2MjIyZjstLXR4dDojZGJlN2YyOy0tbXV0OiM2NDc2ODl9Ym9keXtmb250LWZhbWlseTp1aS1tb25vc3BhY2UsXCJTRiBNb25vXCIsXCJKZXRCcmFpbnMgTW9ub1wiLE1lbmxvLENvbnNvbGFzLG1vbm9zcGFjZSFpbXBvcnRhbnQ7YmFja2dyb3VuZDojMDAwIHJhZGlhbC1ncmFkaWVudCgxMjAwcHggNTYwcHggYXQgNTAlIC04JSxyZ2JhKDY3LDIyOSwyNTUsLjA3KSx0cmFuc3BhcmVudCA2MCUpIWltcG9ydGFudH0ubWMtZW1iIGhlYWRlcntkaXNwbGF5Om5vbmV9PC9zdHlsZT48c2NyaXB0PihmdW5jdGlvbigpe3RyeXtpZihuZXcgVVJMU2VhcmNoUGFyYW1zKGxvY2F0aW9uLnNlYXJjaCkuZ2V0KFwiZW1iZWRkZWRcIik9PT1cIjFcIilkb2N1bWVudC5kb2N1bWVudEVsZW1lbnQuY2xhc3NMaXN0LmFkZChcIm1jLWVtYlwiKTt9Y2F0Y2goZSl7fX0pKCk7PC9zY3JpcHQ+IiwgImNhcHR1cmUiOiAiPHN0eWxlIGlkPVwibWMtc2tpblwiPmJvZHl7YmFja2dyb3VuZDojMDAwIHJhZGlhbC1ncmFkaWVudCgxMjAwcHggNTYwcHggYXQgNTAlIC04JSxyZ2JhKDI1MSwxOTEsMzYsLjA2KSx0cmFuc3BhcmVudCA2MCUpIWltcG9ydGFudH0ubWMtZW1iIC5sb2dve2Rpc3BsYXk6bm9uZX08L3N0eWxlPjxzY3JpcHQ+KGZ1bmN0aW9uKCl7dHJ5e2lmKG5ldyBVUkxTZWFyY2hQYXJhbXMobG9jYXRpb24uc2VhcmNoKS5nZXQoXCJlbWJlZGRlZFwiKT09PVwiMVwiKWRvY3VtZW50LmRvY3VtZW50RWxlbWVudC5jbGFzc0xpc3QuYWRkKFwibWMtZW1iXCIpO31jYXRjaChlKXt9fSkoKTs8L3NjcmlwdD4ifQ==").decode())
def get(w): return json.loads(urllib.request.urlopen(urllib.request.Request(API+w,headers={"X-N8N-API-KEY":JWT})).read())
def put(wf):
    p=json.dumps({"name":wf["name"],"nodes":wf["nodes"],"connections":wf["connections"],"settings":wf.get("settings",{})}).encode()
    r=json.loads(urllib.request.urlopen(urllib.request.Request(API+wf["id"],data=p,method="PUT",headers=H)).read())
    print("updated:",r.get("id"),r.get("name"))
def backup(wf):
    open("/tmp/p2-backup-"+wf["id"]+".json","w").write(json.dumps(wf))
def inject_html(wf,node,skin):
    hit=False
    for n in wf["nodes"]:
        if n["name"]==node:
            b=n["parameters"]["responseBody"]
            assert "</head>" in b, wf["id"]+" no </head>"
            if "mc-skin" in b: print(wf["id"],"already skinned"); return False
            n["parameters"]["responseBody"]=b.replace("</head>",skin+"</head>",1); hit=True
    assert hit, node+" not found in "+wf["id"]
    return True
# reactor / security / jarvis-ui: HTML lives in respond nodes
for wid,node,key in (("aDfiPkkin1TgbIgs","Serve Reactor","reactor"),("v2n0bRhqmSRx4syU","Serve Security Map","security"),("avPI3ObW3ZKjNNMw","Serve Page","jarvis")):
    wf=get(wid); backup(wf)
    if inject_html(wf,node,SK[key]): put(wf)
# capture: HTML template lives inside Build Capture HTML code node (skin is quote-safe: no single quotes/backticks)
wf=get("GEkwWaast1hU3xA2"); backup(wf)
done=False
for n in wf["nodes"]:
    if n["name"]=="Build Capture HTML":
        js=n["parameters"]["jsCode"]
        assert "</head>" in js, "capture: no </head> in jsCode"
        if "mc-skin" in js: print("capture already skinned"); done=True; break
        n["parameters"]["jsCode"]=js.replace("</head>",SK["capture"]+"</head>",1); done=True
        put(wf)
assert done,"Build Capture HTML not found"
# deck v7.2: pass embedded=1 in VIEWS
wf=get("R4es7I5lGGySML1I"); backup(wf)
for n in wf["nodes"]:
    if n["name"]=="Serve Deck":
        b=n["parameters"]["responseBody"]
        b=b.replace("/webhook/reactor?k=","/webhook/reactor?embedded=1&k=")
        b=b.replace("/webhook/security?k=","/webhook/security?embedded=1&k=")
        b=b.replace("/webhook/capture?tab=ag&k=","/webhook/capture?tab=ag&embedded=1&k=")
        b=b.replace("Command Deck v7.1","Command Deck v7.2")
        n["parameters"]["responseBody"]=b
        put(wf)
print("done")
