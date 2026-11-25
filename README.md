# Dragon-Nest-Mobile-Server

[Русская версия](README_RU.md)

This is the server-side component for the **Dragon Nest Mobile** game. The code has been partially refactored, and all necessary `.exe` files have been compiled, allowing the server to be run without additional setup. Below are the instructions for configuring and running the server.

---

## Table of Contents
1. [Description](#description)
2. [Requirements](#requirements)
3. [Server Setup](#server-setup)
4. [Running the Server](#running-the-server)
5. [Client Connection](#client-connection)
6. [Repository Links](#repository-links)

---

## Description
The server-side component of **Dragon Nest Mobile** is responsible for handling game logic, storing data, and interacting with the client. The project has been partially refactored, and all necessary `.exe` files have been compiled, allowing the server to be run without additional compilation.

---

## Requirements
- **MySQL 8.0**: Database server.
- **Visual Studio 10 (C++ 10)**: For working with the server's source code (if modifications are needed).
- **Python 3.12**: For running auxiliary scripts.
- **Git**: For cloning the repository.

---

## Server Setup
1. **Extract Heavy Files**
   Run `LFSUtility.bat` from the project root and choose option `1` to restore the files.
2. **Configure MySQL**
   Install and run MySQL 8.0. The sample configuration currently uses `root@127.0.0.1` with an empty password for isolated local testing only. For network deployment, create a dedicated database user with a strong password and update the database settings in `exe/conf/*.xml`.
3. **Initialize the Database**
   Run `INITIALIZE_DATABASE.bat`. It creates the required databases, server data, and the default test account. The seed account is `depdep` with password `spiraldnm`.

---

## Running the Server
Run `START_SERVER.bat` after database initialization. It starts eight server processes in separate minimized command windows. Check each process log and confirm all required ports are listening before connecting a client.

---

## Client Connection
Launch the matching Dragon Nest Mobile client build. For the local test account, use:
- Username: `depdep`
- Password: `spiraldnm`

Successful startup and client login have not yet been verified on a live Windows/MySQL/client environment.

---

## Repository Links
- **Client Repository**: [Dragon-Nest-Mobile-Client](https://github.com/MaximFonariuc/Dragon-Nest-Mobile-Client)
- **Server Repository**: [Dragon-Nest-Mobile-Server](https://github.com/MaximFonariuc/Dragon-Nest-Mobile-Server)

---

## Notes
- Use the same client build expected by this server.
- Keep GM administration listeners and MySQL private.
- Do not expose administrative or database ports directly to the public internet.
