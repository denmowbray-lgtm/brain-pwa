// build.js — regenerates worker.js from index.html
// Usage: node build.js
// The apex worker (Cloudflare script "soft-limit-2cfc") serves index.html as a
// base64 blob. Edit index.html, run this, then deploy worker.js to Cloudflare.
const fs = require("fs");
const html = fs.readFileSync(__dirname + "/index.html", "utf8");
const b64 = Buffer.from(html, "utf8").toString("base64");
const worker =
'addEventListener("fetch", function (e) { e.respondWith(serve()); });\n' +
'function serve() {\n' +
'  var b64 = "' + b64 + '";\n' +
'  var bin = atob(b64);\n' +
'  var bytes = new Uint8Array(bin.length);\n' +
'  for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);\n' +
'  var html = new TextDecoder("utf-8").decode(bytes);\n' +
'  return new Response(html, { headers: { "content-type": "text/html;charset=UTF-8", "cache-control": "no-store" } });\n' +
'}';
fs.writeFileSync(__dirname + "/worker.js", worker);
console.log("worker.js regenerated — " + worker.length + " bytes, html " + html.length + " chars");
