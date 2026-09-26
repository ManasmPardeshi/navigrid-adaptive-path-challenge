from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    package_share = Path(
        get_package_share_directory("navigrid_description")
    )
    nav2_share = Path(
        get_package_share_directory("nav2_bringup")
    )

    simulation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(package_share / "launch" / "navigrid_sim.launch.py")
        )
    )

    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(nav2_share / "launch" / "bringup_launch.py")
        ),
        launch_arguments={
            "map": str(package_share / "maps" / "navigrid_map.yaml"),
            "params_file": str(
                package_share / "config" / "nav2_params.yaml"
            ),
            "use_sim_time": "True",
            "autostart": "True",
            "slam": "False",
        }.items(),
    )

    delayed_nav2 = TimerAction(
        period=6.0,
        actions=[nav2_bringup],
    )

    return LaunchDescription([
        simulation_launch,
        delayed_nav2,
    ])
