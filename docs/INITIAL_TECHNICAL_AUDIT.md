# Spiral-DNM — Initial Technical Audit

Date: 2026-11-26
Repository reviewed: https://github.com/donikrniwantt/Spiral-DNM
Scope: static inspection of repository files only. No binaries, batch files, database scripts, or server processes were executed.

## Executive summary

The repository contains C++ server source, CMake build definitions, prebuilt Windows executables, MySQL schema scripts, XML service configuration, and bundled third-party libraries. It is **not ready for a safe public deployment** based on this static review.

This report records verified findings and safe next steps. It does not certify ownership, licensing, client compatibility, successful compilation, or runtime operation.

## Critical / high-priority findings

### 1. Database credentials are unsafe
- `exe/conf/db_conf.xml` and `exe/conf/gs_conf.xml` configure MySQL as `root` with an empty password.
- `exe/conf/login_conf.xml` also uses the root account with an empty password.
- `INITIALIZE_DATABASE.bat` assumes the same empty-password root account.
- Do not expose MySQL to the public internet. Create a dedicated database user with a strong password and only the minimum required database privileges. Keep secrets outside tracked source/config files.

### 2. Default test account is inserted by SQL
- `DataBaseInits/5. InitServerData.sql` inserts account `Test` with password `12345`.
- The schema stores a password in a varchar column, but this static review does not establish how the application hashes or validates it.
- Treat the test credential as public and disposable. Do not reuse it for an administrator or production account. Determine the expected password-hashing format from authorized application documentation before changing authentication data.

### 3. Login and GM-tool listeners bind to all interfaces
- `exe/conf/login_conf.xml` binds client/login, control, GM-tool, and other listeners to `0.0.0.0`, including port `25002` for `gmtoollink`.
- This can expose administrative services on every network interface.
- Before any external deployment, restrict management listeners to loopback or a private management network, and enforce firewall rules. Do not expose the GM tool port publicly.

### 4. XML configuration appears malformed
- `exe/conf/gs_conf.xml` contains closing comment tokens (`-->`) after self-closing elements such as `SdkUrl`, `AntiAddictionUrl`, and `DataMoreUrl`, without a corresponding opening comment at those positions.
- A strict XML parser is expected to reject these extra tokens. Validate every XML file with a standards-compliant parser before attempting startup.
- Do not blindly delete these tokens until the intended configuration and parser behavior are confirmed.

### 5. README startup instructions do not match the inspected top-level listing
- `README.md` instructs users to run `START_SERVER.bat`.
- The repository top-level listing inspected during this audit did not contain `START_SERVER.bat`.
- The documented startup path is therefore incomplete or stale. A safe, reproducible launcher has not been established.

## Build and compatibility findings

### 6. Build environment is inconsistent / dated
- Root CMake declares a very old minimum version and uses C++0x.
- The game-server CMake file references Linux-style library paths such as `/usr/lib64/mysql` and links a large set of native libraries.
- README also describes prebuilt Windows executables and Visual Studio 10.
- This indicates separate/possibly stale build assumptions. A clean build has not been performed, and no claim of Windows/Linux compatibility can be made.

### 7. Python helper is Python 2-era code
- `exe/conf_create.py` uses `raw_input`, which is not available in Python 3.
- README asks for Python 3.12. The helper will fail under Python 3 unless ported (for example, use `input()` and check file encoding/paths).
- The helper also copies template configuration files and performs broad string replacements; test it only on a disposable copy after reviewing its behavior.

### 8. Database initialization is not safely repeatable
- Most schema statements use `CREATE ... IF NOT EXISTS`, but the seed script uses plain `INSERT` statements.
- Re-running initialization can fail on duplicate rows or create inconsistent seed data.
- Add explicit preflight checks and make seed operations intentionally idempotent only after confirming the correct unique keys and desired account semantics.

## Required verification before any server launch

1. Obtain and review the provenance and usage rights for the server source, client, bundled libraries, binaries, and game assets. A fork or a new repository license does not grant rights to third-party material.
2. Use a disposable isolated environment; never run unknown prebuilt executables on a personal device or public server.
3. Replace root/blank-password database access with a dedicated least-privilege account and private network binding.
4. Restrict or disable GM/control interfaces until their authentication and access controls are verified.
5. Validate all XML files with a strict parser.
6. Reconcile the README with the actual startup files and supported operating system.
7. Port and test Python helper scripts for the chosen Python version.
8. Run SQL initialization against a disposable database, inspect all tables and seed rows, and test repeatability.
9. Build from source in a clean, reproducible environment and record compiler/dependency versions.
10. Perform security review, backup/restore testing, load testing, and client/server compatibility testing before any public release.

## What this audit did not do

- No executable or batch file was run.
- No SQL was applied to a live database.
- No game client was connected.
- No source code was modified to bypass authentication, anti-cheat, platform services, or other protections.
- No claim is made that the server can currently start or accept players.

## Next audit stage

The next stage should be a dependency and source-structure inventory, followed by XML validation and a clean build plan in an isolated environment. Any code changes should be limited to components the project owner is authorized to modify and should be reviewed before deployment.
