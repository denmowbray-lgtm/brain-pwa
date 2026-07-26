# Deck v6 injector — run on 7090. GET workflow -> splice Serve Deck HTML -> replace Deny 401 params -> PUT.
# -*- coding: utf-8 -*-
import json, urllib.request, subprocess, sys, re

WFID = "R4es7I5lGGySML1I"
KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmNDA5YzUxYi0wZDIwLTQwODYtOGM3ZS1kODE4ODAzZGRiZGQiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiYzNhZDk4NmUtYjViNS00NjcyLWFiMDUtMjhiODE5ZTFkYTBkIiwiaWF0IjoxNzgwOTIwNTU5fQ.N6apR2MVx2RL0quX14fX9srTHt6K0GR1ZV2DFQvgGoQ"
API  = "http://localhost:5678/api/v1/workflows/" + WFID

def req(method, url, body=None):
    r = urllib.request.Request(url, method=method, headers={"X-N8N-API-KEY": KEY, "Content-Type": "application/json"},
                               data=(json.dumps(body).encode() if body is not None else None))
    return json.loads(urllib.request.urlopen(r, timeout=30).read())

wf = req("GET", API)
nodes = wf["nodes"]
serve = next(n for n in nodes if n["name"] == "Serve Deck")
deny  = next(n for n in nodes if n["name"] == "Deny 401")

html = serve["parameters"]["responseBody"]
had_eq = html.startswith("=")
if had_eq: html = html[1:]
orig_len = len(html)

def splice(h, anchor, insert, before=True, must=1):
    c = h.count(anchor)
    assert c == must, "anchor x%d (want %d): %r" % (c, must, anchor[:60])
    return h.replace(anchor, (insert + anchor) if before else (anchor + insert))

def swap(h, old, new, must=1):
    c = h.count(old)
    assert c == must, "swap anchor x%d: %r" % (c, old[:60])
    return h.replace(old, new)

# ---- 1. version bump ----
html = swap(html, "Command Deck v5", "Command Deck v6")
html = swap(html, "GRID v5 \u00b7 PIN-GATED", "GRID v6 \u00b7 PIN-GATED")

# ---- 2. CSS additions ----
CSS = """
.ctl{display:grid;grid-template-columns:repeat(3,1fr);gap:7px}
.cb{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:9px 6px 8px;display:flex;flex-direction:column;align-items:center;gap:5px;font-size:7.5px;letter-spacing:.08em;color:var(--mut);text-align:center;cursor:pointer;transition:transform .1s;user-select:none}
.cb:active{transform:scale(.94)}
.cb .st{font-size:8.5px;font-weight:700;letter-spacing:.06em;color:#4a564e}
.cb .bl2{width:70%;height:5px;border-radius:2px;background:#20261f;transition:background .25s}
.cb.on{border-color:rgba(255,56,67,.55)}.cb.on .bl2{background:var(--red);box-shadow:0 0 8px rgba(255,56,67,.5)}.cb.on .st{color:var(--red)}
.cb.off{border-color:rgba(63,224,139,.4)}.cb.off .bl2{background:var(--grn);box-shadow:0 0 7px rgba(63,224,139,.4)}.cb.off .st{color:var(--grn)}
.cb.arm{border-color:var(--am)}.cb.arm .bl2{background:var(--am);animation:fl .5s steps(2) infinite}.cb.arm .st{color:var(--am)}
.cb.err .bl2{background:var(--red);animation:fl .3s steps(2) infinite}.cb.err .st{color:var(--red)}
.cb.stg::after{content:"2-TAP";font-size:6px;color:var(--am);letter-spacing:.14em;margin-top:1px}
.ctlleg{font-size:7px;color:var(--mut);letter-spacing:.1em;margin-top:7px}
.jcon{margin:0 14px;background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.jcon .fh{padding:8px 12px;border-bottom:1px solid var(--line);font-size:8.5px;letter-spacing:.24em;color:var(--mut);display:flex}
#jlog{max-height:170px;overflow-y:auto;padding:6px 0}
.jm{padding:4px 12px;font-size:10px;display:flex;gap:8px}
.jm .w{flex:0 0 auto;font-size:7.5px;letter-spacing:.1em;align-self:flex-start;margin-top:2px}
.jm.u .w{color:var(--cy)}.jm.j .w{color:var(--grn)}
.jm .b{color:#c3d2c8;white-space:pre-wrap;word-break:break-word}
.jrow{display:flex;gap:7px;padding:8px;border-top:1px solid var(--line)}
#jin{flex:1;background:var(--bg);border:1px solid var(--line);border-radius:6px;color:var(--txt);font-family:var(--mono);font-size:11px;padding:8px 10px;outline:none}
#jin:focus{border-color:var(--grn)}
#jsend{background:none;border:1px solid var(--grn);color:var(--grn);font-family:var(--mono);font-size:9px;letter-spacing:.1em;padding:0 13px;border-radius:6px;cursor:pointer}
.jline{display:none}
"""
html = splice(html, "</style>", CSS, before=True)

# ---- 3. CONTROL section HTML (before WORK ORDERS) ----
CTL_HTML = """<div class="sec"><div class="lbl">HOUSE FEEDERS \u00b7 CONTROL</div>
<div class="ctl" id="ctl"></div>
<div class="ctlleg">TAP = TOGGLE \u00b7 RED = CLOSED/ON \u00b7 GREEN = OPEN/OFF \u00b7 AMBER 2-TAP = STAGED, TAP AGAIN TO EXECUTE</div>
</div>

"""
html = splice(html, '<div class="sec"><div class="lbl">WORK ORDERS</div>', CTL_HTML, before=True)

# ---- 4. JARVIS console HTML replaces jline ----
JCON_HTML = """<div class="jcon"><div class="fh">JARVIS CONSOLE<span class="liv" id="jx" style="margin-left:auto;color:var(--mut)">READY</span></div>
<div id="jlog"></div>
<div class="jrow"><input id="jin" type="text" placeholder="type a command\u2026" autocomplete="off"><button id="jsend">SEND</button></div>
</div>
"""
i0 = html.find('<div class="jline"')
i1 = html.find('<div id="jfab">')
assert 0 < i0 < i1, "jline/jfab anchors"
html = html[:i0] + JCON_HTML + "\n" + html[i1:]

# ---- 5. AGENDA tab button + handler ----
html = splice(html, '<button id="tb-ha">HA</button>', '<button id="tb-ag">AGENDA</button>\n  ', before=True)
html = splice(html, 'document.getElementById("tb-ha").onclick=function(){go(BASE+"/webhook/reactor?k="+PIN);};',
              '\ndocument.getElementById("tb-ag").onclick=function(){go(BASE+"/webhook/capture?k="+PIN+"&tab=ag");};', before=False)

# ---- 6. CONTROL logic block (before JARVIS mic) ----
CTL_JS = """
/* HOUSE CONTROL — breakers via /webhook/ha-control */
var CTL=[
 {e:"light.living_room",n:"LIVING RM",t:"i"},
 {e:"light.foyer_group",n:"FOYER",t:"i"},
 {e:"light.bedroom",n:"BEDROOM",t:"i"},
 {e:"light.garage_group",n:"GARAGE LTS",t:"i"},
 {e:"light.porch_hue",n:"PORCH",t:"i"},
 {e:"switch.master_bed_fan",n:"BED FAN",t:"i"},
 {e:"switch.garage_door",n:"GARAGE DOOR",t:"s"},
 {e:"lock.back_patio_back_patio",n:"PATIO LOCK",t:"s"},
 {e:"alarm_control_panel.alarmo",n:"ALARMO",t:"s"}
];
var CST={},CARM={},CACK={};
function ctlName(e){var c=CTL.filter(function(x){return x.e===e;})[0];return c?c.n:e;}
function ctlAction(c){
 var s=CST[c.e]||"";
 if(c.e.indexOf("lock.")===0)return s==="locked"?"unlock":"lock";
 if(c.e.indexOf("alarm_control_panel")===0)return s==="disarmed"?"arm_home":"disarm";
 return "toggle";}
function ctlLabel(c){var s=CST[c.e];
 if(s===undefined)return "\u2014";
 if(c.e.indexOf("lock.")===0)return s.toUpperCase();
 if(c.e.indexOf("alarm_control_panel")===0)return s.replace("armed_","ARM ").toUpperCase();
 return s==="on"?"CLOSED":"OPEN";}
function ctlClass(c){var s=CST[c.e];
 if(CARM[c.e])return "arm";
 if(s===undefined)return "";
 if(c.e.indexOf("lock.")===0)return s==="locked"?"off":"on";
 if(c.e.indexOf("alarm_control_panel")===0)return s==="disarmed"?"on":"off";
 return s==="on"?"on":"off";}
function ctlRender(){var host=document.getElementById("ctl");host.innerHTML="";
 CTL.forEach(function(c){var d=document.createElement("div");
  d.className="cb "+ctlClass(c)+(c.t==="s"?" stg":"");
  d.innerHTML='<div class="bl2"></div><div>'+c.n+'</div><div class="st">'+(CARM[c.e]?"TAP TO EXECUTE":ctlLabel(c))+'</div>';
  d.onclick=function(){ctlTap(c);};host.appendChild(d);});}
function ctlSync(eid,st){var hit=CTL.filter(function(x){return x.e===eid;})[0];if(!hit)return;
 var prev=CST[eid];CST[eid]=st;
 if(CACK[eid]){clearTimeout(CACK[eid]);delete CACK[eid];soe("ok","CTL",ctlName(eid)+" \u2192 "+st);}
 else if(prev!==undefined&&prev!==st){soe("wn","CTL",ctlName(eid)+" \u2192 "+st);}
 ctlRender();}
function ctlSend(c,action,confirm){
 var body={k:PIN,entity_id:c.e,action:action};if(confirm)body.confirm=true;
 soe("wn","CTL",c.n+" \u2190 "+action+(confirm?" (confirmed)":""));
 CACK[c.e]=setTimeout(function(){delete CACK[c.e];soe("al","CTL",c.n+" NO ACK \u2014 verify device");ctlRender();},8000);
 fetch(BASE+"/webhook/ha-control",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)})
 .then(function(r){return r.json();}).then(function(d){
  if(d&&d.staged&&!confirm){soe("wn","CTL",c.n+" staged \u2014 needs confirm");}
  else if(d&&d.ok===false&&!d.staged){clearTimeout(CACK[c.e]);delete CACK[c.e];soe("al","CTL",c.n+" rejected: "+(d.error||"gate"));ctlRender();}})
 .catch(function(e){clearTimeout(CACK[c.e]);delete CACK[c.e];soe("al","CTL",c.n+" cmd fail: "+e.message);ctlRender();});}
function ctlTap(c){
 if(c.t==="s"){
  if(CARM[c.e]){clearTimeout(CARM[c.e].to);var act=CARM[c.e].a;delete CARM[c.e];ctlSend(c,act,true);ctlRender();return;}
  var a=ctlAction(c);
  CARM[c.e]={a:a,to:setTimeout(function(){delete CARM[c.e];soe("wn","CTL",c.n+" staged action expired");ctlRender();},6000)};
  soe("wn","CTL",c.n+" armed: "+a+" \u2014 tap again in 6s");ctlRender();return;}
 ctlSend(c,ctlAction(c),false);}
ctlRender();
"""
html = splice(html, "/* JARVIS mic */", CTL_JS + "\n", before=True)

# hook control state into WS get_states + state_changed
html = splice(html, "var alm=st.filter(", "st.forEach(function(s){ctlSync(s.entity_id,s.state);});\n   ", before=True)
html = splice(html, 'var d2=m.event.data,eid=d2.entity_id||"",ns=d2.new_state?d2.new_state.state:"";',
              "\n   ctlSync(eid,ns);", before=False)

# ---- 7. replace whole JARVIS mic IIFE with console version ----
jstart = html.find("/* JARVIS mic */")
jend = html.rfind("</script>")
assert 0 < jstart < jend, "jarvis block anchors"
JARVIS_JS = """/* JARVIS console — voice + text */
(function(){var JEP=BASE+"/webhook/jarvis";
var fab=document.getElementById("jfab"),jx=document.getElementById("jx"),
    jlog=document.getElementById("jlog"),jin=document.getElementById("jin"),jbtn=document.getElementById("jsend");
var jrec=null,jOn=false,lastVoice=false;
function jset(t){jx.textContent=t;}
function jadd(who,txt){var d=document.createElement("div");d.className="jm "+(who==="YOU"?"u":"j");
 d.innerHTML='<span class="w">'+who+' \u203a</span><span class="b"></span>';
 d.querySelector(".b").textContent=txt;jlog.appendChild(d);jlog.scrollTop=jlog.scrollHeight;
 while(jlog.children.length>24)jlog.removeChild(jlog.firstChild);}
function jspeak(t){if(!window.speechSynthesis)return;try{var u=new SpeechSynthesisUtterance(String(t).replace(/[*#_]/g,""));u.rate=1.02;speechSynthesis.cancel();speechSynthesis.speak(u);}catch(e){}}
function jsend(m,voice){if(!m)return;lastVoice=!!voice;jadd("YOU",m);jset("THINKING\u2026");
fab.classList.remove("listen");fab.classList.add("think");
fetch(JEP,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:m,session:"dennis",pin:PIN})})
.then(function(r){return r.json();}).then(function(d){fab.classList.remove("think");
var rep=(d&&d.locked)?"PIN rejected":((d&&d.reply)?d.reply:"(no reply)");
jadd("JARVIS",rep);jset("READY");if(lastVoice)jspeak(rep);})
.catch(function(e){fab.classList.remove("think");jadd("JARVIS","net err: "+e.message);jset("NET ERR");});}
jbtn.onclick=function(){var v=jin.value.trim();jin.value="";jsend(v,false);};
jin.addEventListener("keydown",function(e){if(e.key==="Enter"){jbtn.onclick();}});
try{var SR=window.SpeechRecognition||window.webkitSpeechRecognition;
if(SR){jrec=new SR();jrec.lang="en-US";jrec.interimResults=true;jrec.continuous=false;
jrec.onresult=function(e){var last=e.results[e.results.length-1];var t=last[0].transcript;
if(last.isFinal){jOn=false;fab.classList.remove("listen");jsend(t,true);}else{jset("\u2026 "+t);}};
jrec.onend=function(){jOn=false;fab.classList.remove("listen");};
jrec.onerror=function(e){jOn=false;fab.classList.remove("listen");jset("MIC ERR: "+(e.error||"?"));};}}catch(err){jrec=null;}
fab.onclick=function(){if(!jrec){jset("NO SR \u2014 USE CHROME");return;}
if(jOn){try{jrec.stop();}catch(e){}return;}
try{if(window.speechSynthesis)speechSynthesis.cancel();jrec.start();jOn=true;fab.classList.add("listen");jset("LISTENING\u2026");}
catch(e){jset("START ERR: "+e.message);}};})();
"""
html = html[:jstart] + JARVIS_JS + html[jend:]

new_len = len(html)
serve["parameters"]["responseBody"] = ("=" + html) if had_eq else html

# ---- 8. Deny 401 -> access gate page ----
GATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0b0e0d"><title>DENMOW GRID \u2014 Access</title>
<style>
:root{--bg:#0b0e0d;--panel:#141917;--panel2:#1a201d;--line:#27302b;--txt:#e8efe9;--mut:#7d8a81;--grn:#3fe08b;--am:#ffb832;--red:#ff3843;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--txt);font-family:var(--mono);min-height:100dvh;display:flex;align-items:center;justify-content:center;
background-image:radial-gradient(900px 400px at 50% -5%,rgba(63,224,139,.05),transparent 60%),repeating-linear-gradient(0deg,transparent 0 3px,rgba(255,255,255,.012) 3px 4px)}
.card{width:min(320px,92vw)}
.plate{border:1px solid var(--line);border-bottom:2px solid var(--line);border-radius:10px 10px 0 0;padding:16px;background:var(--panel);text-align:center}
.plate h1{font-size:13px;letter-spacing:.2em}
.plate .rev{font-size:8px;color:var(--mut);letter-spacing:.14em;margin-top:5px}
.lampwin{margin:0;background:#000;border:1px solid var(--line);border-top:0;padding:10px;display:flex;flex-direction:column;align-items:center;gap:7px}
.lamp{width:60%;height:7px;border-radius:2px;background:var(--red);box-shadow:0 0 12px rgba(255,56,67,.6)}
.lamp.deny{animation:fl .4s steps(2) 6}
@keyframes fl{50%{opacity:.2}}
.lst{font-size:8px;letter-spacing:.24em;color:#f5adaf}
.pin{display:flex;gap:9px;justify-content:center;padding:16px 0 6px;background:var(--panel);border:1px solid var(--line);border-top:0}
.pin i{width:13px;height:13px;border-radius:50%;border:1px solid var(--line);background:var(--panel2)}
.pin i.f{background:var(--grn);border-color:var(--grn);box-shadow:0 0 8px rgba(63,224,139,.55)}
.pad{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;padding:12px;background:var(--panel);border:1px solid var(--line);border-top:0;border-radius:0 0 10px 10px}
.pad button{background:var(--panel2);border:1px solid var(--line);border-radius:8px;color:var(--txt);font-family:var(--mono);font-size:16px;padding:13px 0;cursor:pointer;transition:transform .08s}
.pad button:active{transform:scale(.93)}
.pad .fn{font-size:9px;letter-spacing:.1em;color:var(--mut)}
.pad .en{border-color:var(--grn);color:var(--grn)}
.foot{text-align:center;font-size:7.5px;color:var(--mut);letter-spacing:.2em;margin-top:12px}
</style></head><body>
<div class="card">
<div class="plate"><h1>DENMOW SWGR-1</h1><div class="rev">ACCESS CONTROL \u00b7 GRID v6</div></div>
<div class="lampwin"><div class="lamp" id="lamp"></div><div class="lst" id="lst">LOCKED \u2014 ENTER PIN</div></div>
<div class="pin" id="dots"><i></i><i></i><i></i><i></i></div>
<div class="pad">
<button data-d="1">1</button><button data-d="2">2</button><button data-d="3">3</button>
<button data-d="4">4</button><button data-d="5">5</button><button data-d="6">6</button>
<button data-d="7">7</button><button data-d="8">8</button><button data-d="9">9</button>
<button class="fn" id="clr">CLR</button><button data-d="0">0</button><button class="fn en" id="ent">ENTER</button>
</div>
<div class="foot">AUTHORIZED PERSONNEL ONLY</div>
</div>
<script>
(function(){
var u=new URL(location.href),bad=u.searchParams.get("k"),st=null;
try{st=localStorage.getItem("core_k");}catch(e){}
if(!bad&&st){u.searchParams.set("k",st);location.replace(u.href);return;}
if(bad){
 if(st===bad){try{localStorage.removeItem("core_k");}catch(e){}}
 document.getElementById("lamp").className="lamp deny";
 document.getElementById("lst").textContent="ACCESS DENIED \u2014 RE-ENTER PIN";
}
var buf="";
function dots(){var d=document.querySelectorAll("#dots i");d.forEach(function(el,i){el.className=i<buf.length?"f":"";});}
function submit(){if(!buf)return;u.searchParams.set("k",buf);location.replace(u.href);}
document.querySelectorAll(".pad button[data-d]").forEach(function(b){b.onclick=function(){
 if(buf.length>=8)return;buf+=b.getAttribute("data-d");dots();if(buf.length===4)setTimeout(submit,140);};});
document.getElementById("clr").onclick=function(){buf="";dots();};
document.getElementById("ent").onclick=submit;
document.addEventListener("keydown",function(e){
 if(e.key>="0"&&e.key<="9"&&buf.length<8){buf+=e.key;dots();if(buf.length===4)setTimeout(submit,140);}
 else if(e.key==="Backspace"){buf=buf.slice(0,-1);dots();}
 else if(e.key==="Enter"){submit();}});
})();
</script>
</body></html>"""

deny["parameters"] = {
    "respondWith": "text",
    "responseBody": GATE,
    "options": {
        "responseCode": 200,
        "responseHeaders": {"entries": [{"name": "Content-Type", "value": "text/html; charset=utf-8"}]}
    }
}

# ---- verify page script syntax before PUT ----
open("/tmp/deck-v6.html", "w").write(html)
m = re.findall(r"<script>(.*?)</script>", html, re.S)
scr = m[-1]
open("/tmp/deck-v6.js", "w").write(scr)
chk = subprocess.run(["bash", "-c", "node --check /tmp/deck-v6.js 2>&1 || docker exec -i n8n node --check /dev/stdin < /tmp/deck-v6.js 2>&1"],
                     capture_output=True, text=True)
if "rror" in (chk.stdout + chk.stderr):
    print("SYNTAX FAIL:\n", chk.stdout, chk.stderr); sys.exit(1)

gm = re.findall(r"<script>(.*?)</script>", GATE, re.S)
open("/tmp/gate.js", "w").write(gm[0])
chk2 = subprocess.run(["bash", "-c", "node --check /tmp/gate.js 2>&1 || docker exec -i n8n node --check /dev/stdin < /tmp/gate.js 2>&1"],
                      capture_output=True, text=True)
if "rror" in (chk2.stdout + chk2.stderr):
    print("GATE SYNTAX FAIL:\n", chk2.stdout, chk2.stderr); sys.exit(1)

# ---- PUT ----
s = wf.get("settings") or {}
clean = {k: s[k] for k in ["executionOrder","timezone","callerPolicy","errorWorkflow","saveManualExecutions",
                           "saveExecutionProgress","executionTimeout","saveDataErrorExecution","saveDataSuccessExecution"] if k in s}
body = {"name": wf["name"], "nodes": nodes, "connections": wf["connections"], "settings": clean, "staticData": wf.get("staticData")}
res = req("PUT", API, body)
print(json.dumps({"put_ok": bool(res.get("id")), "html_delta": new_len - orig_len,
                  "gate_len": len(GATE), "versionId": res.get("versionId")}))
