# Miscellaneous GDB Python Scripts
### `gdb_remote_exec.py`
Includes a client and a server that allow you to send commands to two gdb instances at once.
#### Commands:
 - `start_server`: Starts the server (blocking) on port 12354. When it receives commands, it executes them.
 - `exec_remote <command>`: Sends a command to the server at localhost:12354
 - `exec_remote_local <command>`: Executes the given command and sends it to the server at localhost:12354
If you want to change the address/port, modify the source file.
