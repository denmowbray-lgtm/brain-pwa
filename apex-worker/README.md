# Apex Worker — dmowbray.us

Source of truth for the Cloudflare Worker that serves the **dmowbray.us** apex
homepage (THE CORE — the 3D orbit / pod launcher).

- Cloudflare script name: `soft-limit-2cfc`
- Account: `89cc68baa7677b94496fc19d38ce32df`
- Zone: dmowbray.us (`9ed9fa1b939cbc27ce2fcb0f565f82ee`)

## Files
- `index.html` — the real, editable source (the whole homepage: orbit canvas,
  voice console, PODS array). **Edit this.**
- `worker.js` — the deployed Cloudflare Worker. It carries `index.html` as a
  base64 blob and serves it. **Generated — do not hand-edit.**
- `build.js` — regenerates `worker.js` from `index.html`.

## Editing the homepage / pods
1. Edit `index.html` (e.g. add/flip a pod in the `PODS` array).
2. `node build.js`  → regenerates `worker.js`.
3. Deploy `worker.js` to Cloudflare (see below).

## Deploying
Claude's sandbox cannot reach the Cloudflare API directly, so deploys route
through n8n:

- **Orbit DECK Injector** (`v3AKAVUs6dHS6RRV`) — fetches the live worker,
  splices a single pod, redeploys. Idempotent. Good for one-pod changes.
- **CF Deploy Apex Worker** (`s0LOoeG5ZjYYoX1X`) — raw `application/javascript`
  PUT of a full worker script to
  `accounts/{acct}/workers/scripts/soft-limit-2cfc`. Use for full redeploys of
  this `worker.js`.

The live worker is the only authoritative copy at runtime; this repo is the
version-controlled source so edits no longer require decoding the deployed blob.
