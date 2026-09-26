# NaviGrid: The Adaptive Path Challenge

ROS 2 Jazzy and Gazebo Harmonic simulation package for a dual-path autonomous mobile robot arena.

## Platform

- Ubuntu 24.04 LTS
- ROS 2 Jazzy Jalisco
- Gazebo Harmonic, GZ Sim 8
- Colcon and ament_cmake

## Implemented Features

### Arena

- 30 m x 30 m enclosed arena
- LiDAR-detectable boundary walls
- Shared Start Zone A and Goal Zone B
- Direct elevated route with ascending ramp, platform, and descending ramp
- Flat ground-level zig-zag route
- Warehouse rack, structural pillars, and chokepoints
- Animated Gazebo pedestrian actor definition
- Secondary differential-drive robot

### Primary Robot

- Differential drive
- 360-degree GPU LiDAR
- IMU
- Odometry
- Robot State Publisher
- ROS-Gazebo bridge
- ROS 2 velocity control

### ROS 2 Interfaces

- /clock
- /scan
- /imu
- /odom
- /cmd_vel
- /tf
- /tf_static

Verified TF chain:

    odom -> base_link -> lidar_link
                       -> imu_link
                       -> caster

### Mapping

- SLAM Toolbox asynchronous mapping configuration
- 0.05 m occupancy-grid resolution
- 10 m LiDAR range
- Saved navigrid_map.pgm and navigrid_map.yaml

The included occupancy map is a valid partial map generated from the robot starting area. It is not claimed as a complete exploration of the full arena.

## Repository Structure

    src/navigrid_description/
    |-- CMakeLists.txt
    |-- package.xml
    |-- config/
    |   |-- bridge.yaml
    |   `-- slam_toolbox.yaml
    |-- launch/
    |   `-- navigrid_sim.launch.py
    |-- maps/
    |   |-- navigrid_map.pgm
    |   `-- navigrid_map.yaml
    |-- urdf/
    |   `-- navigrid_robot.urdf
    `-- worlds/
        `-- navigrid_world.sdf

## Prerequisites

    sudo apt update
    sudo apt install -y       ros-jazzy-ros-gz       ros-jazzy-robot-state-publisher       ros-jazzy-slam-toolbox       ros-jazzy-navigation2       ros-jazzy-nav2-bringup

## Build

    source /opt/ros/jazzy/setup.bash
    colcon build --packages-select navigrid_description --symlink-install
    source install/setup.bash

If rosdep is installed, dependencies can also be checked with:

    rosdep install --from-paths src --ignore-src -r -y

## Launch Simulation

    ros2 launch navigrid_description navigrid_sim.launch.py

The launch file automatically starts:

1. Gazebo Harmonic in headless server mode
2. The NaviGrid arena
3. ROS-Gazebo bridge
4. Robot State Publisher
5. Primary navigrid_robot

## Launch SLAM

Keep the simulation running and use a second terminal:

    source /opt/ros/jazzy/setup.bash
    source install/setup.bash

    ros2 launch slam_toolbox online_async_launch.py       slam_params_file:=$(ros2 pkg prefix --share navigrid_description)/config/slam_toolbox.yaml       use_sim_time:=true

## Validation

Validate the world:

    gz sdf -k src/navigrid_description/worlds/navigrid_world.sdf

Validate the robot:

    check_urdf src/navigrid_description/urdf/navigrid_robot.urdf

Verify interfaces while the simulation is running:

    ros2 topic list

Verify TF:

    timeout 5s ros2 run tf2_ros tf2_echo odom lidar_link

## Verified Results

- Clean Colcon build completed successfully
- Gazebo world passed SDF validation
- Robot passed URDF validation
- Primary robot spawned automatically
- LiDAR, IMU, odometry, velocity control, clock, and TF were bridged to ROS 2
- LiDAR detected arena collision geometry and boundary walls
- Secondary robot perpendicular movement was demonstrated
- SLAM Toolbox published an occupancy map
- Map files were saved and installed with the package

## Known Limitations

The following competition capabilities are not claimed as complete:

- Full autonomous exploration of the 30 m x 30 m arena
- Complete Nav2 Point A to Point B execution
- Automatic cost-aware selection between the incline and zig-zag routes
- Runtime pedestrian avoidance demonstration
- Velocity-dependent emergency-stop safety node
- Completion-time and collision-penalty reporting
- GUI evidence of pedestrian animation in the headless AWS environment

The pedestrian currently references a Gazebo Fuel walk.dae resource, so internet access may be needed during initial loading.

## License

Apache License 2.0
