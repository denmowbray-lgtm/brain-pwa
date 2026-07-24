// build.js — regenerates worker.js from index.html
// Usage: node build.js
// The apex worker (Cloudflare script "soft-limit-2cfc") serves index.html as a
// base64 blob. Edit index.html, run this, then deploy worker.js to Cloudflare.
// Also serves /manifest.json + /icon.svg so the CORE installs as a real PWA.
const fs = require("fs");
const html = fs.readFileSync(__dirname + "/index.html", "utf8");
const b64 = Buffer.from(html, "utf8").toString("base64");

const manifest = JSON.stringify({
  name: "DMOWBRAY CORE",
  short_name: "CORE",
  start_url: "/",
  display: "standalone",
  background_color: "#0a0e14",
  theme_color: "#0a0e14",
  icons: [{ src: "/icon.svg", sizes: "any", type: "image/svg+xml", purpose: "any" }]
});

const icon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" rx="96" fill="#0a0e14"/><circle cx="256" cy="256" r="150" fill="none" stroke="#1e2d3d" stroke-width="10"/><circle cx="256" cy="256" r="64" fill="#4fc3f7"/><circle cx="256" cy="106" r="18" fill="#3fb950"/></svg>';

const worker =
'addEventListener("fetch", function (e) { e.respondWith(serve(e.request)); });\n' +
'var MANIFEST = ' + JSON.stringify(manifest) + ';\n' +
'var ICON = ' + JSON.stringify(icon) + ';\n' +
'function serve(req) {\n' +
'  var p = "";\n' +
'  try { p = new URL(req.url).pathname; } catch (err) {}\n' +
'  if (p === "/manifest.json") return new Response(MANIFEST, { headers: { "content-type": "application/manifest+json", "cache-control": "no-store" } });\n' +
'  if (p === "/icon.svg") return new Response(ICON, { headers: { "content-type": "image/svg+xml", "cache-control": "max-age=86400" } });\n' +
'  var b64 = "' + b64 + '";\n' +
'  var bin = atob(b64);\n' +
'  var bytes = new Uint8Array(bin.length);\n' +
'  for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);\n' +
'  var html = new TextDecoder("utf-8").decode(bytes);\n' +
'  return new Response(html, { headers: { "content-type": "text/html;charset=UTF-8", "cache-control": "no-store" } });\n' +
'}';
fs.writeFileSync(__dirname + "/worker.js", worker);
console.log("worker.js regenerated — " + worker.length + " bytes, html " + html.length + " chars");
