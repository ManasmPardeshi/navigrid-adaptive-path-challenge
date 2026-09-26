from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node


def generate_launch_description():
    package_share = Path(
        get_package_share_directory("navigrid_description")
    )

    world_file = package_share / "worlds" / "navigrid_world.sdf"
    robot_file = package_share / "urdf" / "navigrid_robot.urdf"
    bridge_file = package_share / "config" / "bridge.yaml"

    robot_description = robot_file.read_text()

    gazebo = ExecuteProcess(
        cmd=[
            "gz",
            "sim",
            "-s",
            "-r",
            str(world_file),
        ],
        output="screen",
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="ros_gz_bridge",
        parameters=[
            {
                "config_file": str(bridge_file),
                "use_sim_time": True,
            }
        ],
        output="screen",
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": True,
            }
        ],
        output="screen",
    )

    spawn_primary_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-world",
            "navigrid_world",
            "-file",
            str(robot_file),
            "-name",
            "navigrid_robot",
            "-x",
            "0",
            "-y",
            "-12",
            "-z",
            "0.15",
        ],
        output="screen",
    )

    delayed_robot_spawn = TimerAction(
        period=3.0,
        actions=[spawn_primary_robot],
    )

    return LaunchDescription(
        [
            gazebo,
            bridge,
            robot_state_publisher,
            delayed_robot_spawn,
        ]
    )
