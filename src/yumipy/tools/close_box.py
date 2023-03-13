"""
Helper script to move YuMi back to home pose
Author: Jeff Mahler
"""
from yumipy import YuMiRobot, YuMiState
from yumipy import YuMiConstants as YMC

if __name__ == '__main__':
    y = YuMiRobot()
    y.set_z('z50')
    y.set_v(500)

    y.left.close_gripper()

    robot = y
    arm = y.left
    arm.goto_pose(YMC.L_PREGRASP_POSE, wait_for_res=True)
    
    # shake test
    radius = 0.1
    angle = np.pi / 8
    delta_T = RigidTransform(translation=[0,0,-radius], from_frame='gripper', to_frame='gripper')
    R_shake = np.array([[1, 0, 0],
                        [0, np.cos(angle), -np.sin(angle)],
                        [0, np.sin(angle), np.cos(angle)]])
    delta_T_up = RigidTransform(rotation=R_shake, translation=[0,0,radius], from_frame='gripper', to_frame='gripper')
    delta_T_down = RigidTransform(rotation=R_shake.T, translation=[0,0,radius], from_frame='gripper', to_frame='gripper')
    T_shake_up = YMC.L_PREGRASP_POSE.as_frames('gripper', 'world') * delta_T_up * delta_T
    T_shake_down = YMC.L_PREGRASP_POSE.as_frames('gripper', 'world') * delta_T_down * delta_T

    robot.set_z(config['control']['approach_zoning'])
    for i in range(5):
        arm.goto_pose(T_shake_up, wait_for_res=False)
        arm.goto_pose(YMC.L_PREGRASP_POSE, wait_for_res=True)
        arm.goto_pose(T_shake_down, wait_for_res=False)
        arm.goto_pose(YMC.L_PREGRASP_POSE, wait_for_res=True)
    robot.set_v(config['control']['standard_velocity'])
    robot.set_z(config['control']['standard_zoning'])

    y.stop()
