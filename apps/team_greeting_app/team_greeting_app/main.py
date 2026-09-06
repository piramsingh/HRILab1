from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose

import numpy as np

#Without turning off the connection and the media back end, the app wouldn't work!
with ReachyMini(
    connection_mode="localhost_only",
    media_backend="no_media"
) as mini:

    print("Connected to Reachy Mini simulation!")

    #first fun little movement!
    mini.goto_target(
        head=create_head_pose(z=10, mm=True),
        antennas=np.deg2rad([45, 45]),
        body_yaw=np.deg2rad(30),
        duration=2.0,
        method="minjerk",
    )

    #Lets make it a dance (second movement)!
    mini.goto_target(
        head=create_head_pose(z=-10, mm=True),
        antennas=np.deg2rad([-45, -45]),
        body_yaw=np.deg2rad(-30),
        duration=2.0,
        method="minjerk",
    )

    print("Movement complete!")

    # Return the robot to neutral.
    mini.goto_target(
        head=create_head_pose(),
        antennas=[0.0, 0.0],
        body_yaw=0.0,
        duration=2.0,
        method="minjerk",
    )

    print("Returned to neutral!")
