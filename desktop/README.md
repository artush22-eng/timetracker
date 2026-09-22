# TimeTracker desktop client (Windows / Linux / macOS)

Electron app that mirrors the native macOS client: clock in/out, activity every minute,
a screenshot every 10 minutes, foreground-app tracking, idle warnings, sync to the API.

## Run locally
    cd desktop
    npm install
    npm start

## Build installers
    npm run dist:win     # TimeTracker-Setup.exe + TimeTracker-Portable.exe (run on Windows, or in CI)
    npm run dist:linux   # TimeTracker.AppImage + TimeTracker.deb
    npm run dist:mac     # TimeTracker.dmg

CI: `.github/workflows/build.yml` builds all three on GitHub. Push a tag (`git tag v1.0.0 && git push --tags`)
and the installers are attached to a GitHub Release; the website links to `releases/latest/download/...`.

Data lives in the OS user-data folder (`%APPDATA%/TimeTracker` on Windows, `~/.config/TimeTracker` on Linux):
`session.json`, `shifts.json`, `queue.json` (failed syncs, retried every minute), `screenshots/`, `tracker.log`.
