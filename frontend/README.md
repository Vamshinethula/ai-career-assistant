# AI Career Assistant frontend

React + Vite dashboard for registration, login, PDF uploads, extracted text,
skill mentions and illustrative role overlaps.

See the [project README](../README.md) for complete setup, architecture,
API usage, verification and limitations.

From this `frontend/` directory:

```powershell
npm.cmd ci
npm.cmd run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

FastAPI must also run on `http://127.0.0.1:8000`. Open
`http://127.0.0.1:5173/`. Reuse an existing server on that port.

```powershell
npm.cmd run build
npm.cmd run lint
```

`src/services/api.js` owns requests and response validation. Components live in
`src/components/`; login state lives in `App.jsx` and clears on refresh.
Set VITE_API_BASE_URL in .env.local to override the local API default. See .env.example. Restart Vite after edits; rebuild production output. VITE_ values are public: never put secrets there.
