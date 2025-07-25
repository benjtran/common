"""
Emulates position and attitude to Pixhawk.
"""

import time
from ..mavlink import dronekit


class PositionEmulator:
    """
    Setup for position emulator.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, drone: dronekit.Vehicle
    ) -> "tuple[True, PositionEmulator] | tuple[False, None]":
        """
        Setup position emulator.

        Returns:
            Success, PositionEmulator instance.
        """

        return True, PositionEmulator(cls.__create_key, drone)

    def __init__(self, class_private_create_key: object, drone: dronekit.Vehicle) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is PositionEmulator.__create_key, "Use create() method"

        self.drone = drone

    def inject_position(
        self,
        latitude: float = 43.43405014107003,
        longitude: float = -80.57898027451816,
        altitude: float = 373.0,
    ) -> None:
        """
        Simulates gps coordinates by injecting the desired position of the drone.
        Args:
            latitude: Latitude in degrees.
            longitude: Longitude in degrees.
            altitude: Altitude in meters.
        """
        values = [
            int(time.time() * 1e6),  # time_usec
            0,  # gps_id
            0b111111,  # ignore_flags (all fields valid)
            0,  # time_week_ms
            0,  # time_week
            3,  # fix_type (3D fix)
            int(latitude * 1e7),  # lat
            int(longitude * 1e7),  # lon
            int(altitude * 1000),  # alt (mm)
            100,  # hdop (x100)
            100,  # vdop (x100)
            0,  # vn (cm/s)
            0,  # ve (cm/s)
            0,  # vd (cm/s)
            100,  # speed_accuracy (cm/s)
            100,  # horiz_accuracy (cm)
            100,  # vert_accuracy (cm)
            10,  # satellites_visible
            0,  # yaw (deg*100)
        ]
        print("Packing values:", values)
        gps_input_msg = self.drone.message_factory.gps_input_encode(*values)
        self.drone.send_mavlink(gps_input_msg)
        self.drone.flush()
