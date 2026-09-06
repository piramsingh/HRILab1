# This code uses examples from the Reachy Mini Python SDK link to turn it into an application: https://huggingface.co/docs/reachy_mini/v1.9.0/en/SDK/python-sdk

import threading
import time

import numpy as np

from reachy_mini import ReachyMini, ReachyMiniApp
from reachy_mini.utils import create_head_pose


# ---
# Named motion and timing parameters that need to be varied across 3 trials

# Duration of the main movements (s)
MOTION_DURATION_SECONDS = 1.0

# Size of the up-and-down head movement (degrees).
NOD_ANGLE_DEGREES = 15

# Duration of each part of the head nod(s).
NOD_DURATION_SECONDS = 0.75

# Pause between movements(s).
PAUSE_DURATION_SECONDS = 0.3

# Size of the body rotation (degrees).
BODY_YAW_DEGREES = 30.0

# Size of the antenna movement (degrees).
ANTENNA_ANGLE_DEGREES = 45.0
# ---


def print_stage(message):
    # Print a message with the current date and time.
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


class TeamGreetingApp(ReachyMiniApp):
    # The application does not need a webpage, nore camera or microphone.
    custom_app_url: str | None = None
    request_media_backend: str | None = "no_media"

    def run(
        self,
        reachy_mini: ReachyMini,
        stop_event: threading.Event,
    ):
        greeting_completed = False

        try:
            # Print two variables that are varied across 3 trials
            print_stage(
                "TEST PARAMETERS: "
                f"motion duration = {MOTION_DURATION_SECONDS} seconds, "
                f"nod angle = {NOD_ANGLE_DEGREES} degrees"
            )
            # ---
            # Stage 1: Orient body of Reachy towards user
            # ---

            print_stage(
                "STAGE 1: Looking at the user "
                f"(motion duration = {MOTION_DURATION_SECONDS} seconds)"
            )

            if stop_event.is_set():
                return

            reachy_mini.goto_target(
                head=create_head_pose(z=10, mm=True),
                antennas=np.deg2rad(
                    [ANTENNA_ANGLE_DEGREES, ANTENNA_ANGLE_DEGREES]
                ),
                body_yaw=np.deg2rad(BODY_YAW_DEGREES),
                duration=MOTION_DURATION_SECONDS,
                method="minjerk",
            )

            # The wait ends early if a stop is requested.
            if stop_event.wait(PAUSE_DURATION_SECONDS):
                return

            # ---
            # Stage 2: Perform the dance
            # ---

            print_stage("STAGE 2: Performing the dance")

            if stop_event.is_set():
                return

            reachy_mini.goto_target(
                head=create_head_pose(z=-10, mm=True),
                antennas=np.deg2rad(
                    [-ANTENNA_ANGLE_DEGREES, -ANTENNA_ANGLE_DEGREES]
                ),
                body_yaw=np.deg2rad(-BODY_YAW_DEGREES),
                duration=MOTION_DURATION_SECONDS,
                method="minjerk",
            )

            if stop_event.wait(PAUSE_DURATION_SECONDS):
                return

            # Part 3 nod head!
            print_stage("STAGE 3: nod head up and down")
            print_stage(
                "STAGE 3: nod head up and down"
                f"(nod angle = ±{NOD_ANGLE_DEGREES} degrees)"
            )

            # Down, up, down, up, and center.
            nod_positions = [
                -NOD_ANGLE_DEGREES,
                NOD_ANGLE_DEGREES,
                -NOD_ANGLE_DEGREES,
                NOD_ANGLE_DEGREES,
                0.0,
            ]

            for pitch_degrees in nod_positions:
                # Check stop_event during every loop repetition.
                if stop_event.is_set():
                    return

                reachy_mini.goto_target(
                    head=create_head_pose(
                        pitch=pitch_degrees,
                        degrees=True,
                    ),
                    duration=NOD_DURATION_SECONDS,
                    method="minjerk",
                )

                # Check stop_event during every wait.
                if stop_event.wait(PAUSE_DURATION_SECONDS):
                    return

            greeting_completed = True

        except KeyboardInterrupt:
            # Handle Ctrl+C 
            stop_event.set()
            print_stage("STOP REQUESTED: Control-C received")

        finally:
            # ---
            # Stage 4: Always return to neutral
            # ---

            print_stage("STAGE 4: Returning to neutral")

            try:
                reachy_mini.goto_target(
                    head=create_head_pose(),
                    antennas=[0.0, 0.0],
                    body_yaw=0.0,
                    duration=MOTION_DURATION_SECONDS,
                    method="minjerk",
                )

            except KeyboardInterrupt:
                # If Ctrl+C occurs during Stage 3, make one final shorter request to return to neutral.
                stop_event.set()
                print_stage("STOP REQUESTED DURING NEUTRAL RETURN")

                reachy_mini.goto_target(
                    head=create_head_pose(),
                    antennas=[0.0, 0.0],
                    body_yaw=0.0,
                    duration=0.5,
                    method="minjerk",
                )

            if greeting_completed:
                print_stage("APPLICATION COMPLETED")
            else:
                print_stage("APPLICATION STOPPED SAFELY")


if __name__ == "__main__":
    app = TeamGreetingApp()

    try:
        app.wrapped_run()
    except KeyboardInterrupt:
        app.stop()