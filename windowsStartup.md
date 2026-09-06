## Restarting the Reachy Mini Development Environment

Follow these steps after closing VS Code, Reachy Mini Control, or the simulator.

### 1. Open the project in VS Code with WSL

Open VS Code and start a WSL terminal. Then navigate to the repository:

```bash
cd /mnt/c/Users/Craft/Documents/HRI/HRILab1
code .
```

If the project is already open in VS Code, only the `cd` command is necessary.

### 2. Start the simulator in Terminal 1

Activate the Python virtual environment:

```bash
source reachy_mini_env/bin/activate
```

The terminal prompt should begin with:

```text
(reachy_mini_env)
```

Start the Reachy Mini daemon and MuJoCo simulator:

```bash
reachy-mini-daemon --sim
```

Keep this terminal open while developing or testing. Wait until the terminal reports that the daemon started successfully and the MuJoCo window appears.

### 3. Open Reachy Mini Control

Open **Reachy Mini Control** from the Windows Start menu. It should connect to the simulator running through WSL and display the robot status as **Ready**.

Do not start another simulation if the existing simulation is detected.

### 4. Open Terminal 2 for development

Create another WSL terminal in VS Code. Activate the same environment:

```bash
cd /mnt/c/Users/Craft/Documents/HRI/HRILab1
source reachy_mini_env/bin/activate
```

Use Terminal 2 to validate, install, run, and test applications while Terminal 1 continues running the daemon.

### 5. Shut everything down

Stop a running application normally with `Ctrl+C`. Then stop the daemon in Terminal 1 with `Ctrl+C`.

Exit the virtual environment in either terminal with:

```bash
deactivate
```

Finally, close Reachy Mini Control, MuJoCo, and VS Code.
