# Dragon-Nest-Mobile-Server

[Русская версия](README_RU.md)

This repository contains source code, configuration, database initialization scripts, and some prebuilt Windows server binaries for Dragon Nest Mobile. **It is not currently a verified, ready-to-run server package.**

## Requirements
- Windows x64 (the included server executables are Windows binaries).
- MySQL 8.0, configured for local testing before any public deployment.
- Python 3.12 for the LFS helper scripts.
- The exact compatible Dragon Nest Mobile client build.

## Setup
1. Clone or download this repository.
2. Run `LFSUtility.bat` and choose option `1` to restore files recorded in `compression_log.txt`, if that log and its archive parts are present.
3. Install MySQL 8.0 and review every database setting under `exe/conf/`. The sample configuration uses `root@127.0.0.1` with an empty password and is suitable only for an isolated local test environment.
4. Run `INITIALIZE_DATABASE.bat` from the repository root to execute the SQL scripts in filename order.

## Server package status
The startup script checks all eight required server executables and all eight configuration files before starting anything. The current repository snapshot contains these six server executables:
- `audioserver.exe`
- `loginserver.exe`
- `dbserver.exe`
- `gateserver.exe`
- `controlserver.exe`
- `versionserver.exe`

The following required executables are **missing** from the current repository snapshot:
- `gameserver.exe`
- `masterserver.exe`

PDB archives are not executable server binaries and cannot replace them. Consequently, `START_SERVER.bat` will intentionally stop with an error rather than start a broken partial server. Restore the genuine matching binaries from an authorized build or compile them from source using the project's supported Windows toolchain.

## Test account
The database seed script creates a local test account:
- Username: `depdep`
- Password field value: `spiraldnm`

The account row is present in the SQL seed, but the password encoding/protocol and successful client authentication have **not** been verified. Do not treat these credentials as confirmed working until login is tested with the matching client build. This repository is public; change sample credentials before any shared or public deployment.

## Running and stopping
After all required binaries are present and the database is initialized, run `START_SERVER.bat`. It validates the package before launching the eight processes. Use `STOP_SERVER.bat` to stop the server processes.

## Security
- Keep MySQL port 3306 private.
- Keep GM administration listeners bound to loopback or protect remote administration with VPN/SSH.
- Expose only client-facing ports required by the matching client and firewall all other ports.
- Do not enable gate encryption until the matching client protocol has been verified.
- Do not deploy the sample empty MySQL root password or sample account credentials publicly.

## Upstream references
- Client: https://github.com/MaximFonariuc/Dragon-Nest-Mobile-Client
- Server: https://github.com/MaximFonariuc/Dragon-Nest-Mobile-Server
