## Running the Application in MuJoCo

The application requires Python 3.10-3.12 and an activated virtual
environment named `reachy_mini_env`.

### Terminal 1: Start the simulator

From the root of the private course repository:

```bash
source reachy_mini_env/bin/activate
reachy-mini-daemon --sim
```

Keep this terminal and the MuJoCo window running.

### Terminal 2: INstall and run the application

Open a second terminal from the repository root: 

```bash
source reachy_mini_env/bin/activate
uv pip install -e apps/team_greeting_app
python -m team_greeting_app.main
```

Press `Ctrl+c` to request a normal stop. The application checks the provided `stop_event` and requests that the head,antennas, and body yaw return to neuutral before exiting. 

### Validating the application

From the repository root: 

```bash
reachy-mini-app-assistant check apps/team_greeting_app
```
### Application behavior 
The application performs three behavioral stages:
1. orient towards and implied user. (with a little dance)
2. Perform a greeting using coordinated head, antenna, and body movements. 
3. return the simiulated robot to its neutral position. 

The application does not access the camera, microphone, cloud, AI, or personal data.

