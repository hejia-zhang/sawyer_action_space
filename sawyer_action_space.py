import rospy

from sensor_msgs.msg import JointState


sawyer_velocity_action_space = {}
sawyer_effort_action_space = {}


def on_msg(data):
    joints = data.name
    velocities = data.velocity
    efforts = data.effort

    idx = 0
    for joint in joints:
        velocity = velocities[idx]
        effort = efforts[idx]
        idx += 1

        if joint not in sawyer_velocity_action_space:
            sawyer_velocity_action_space[joint] = round(abs(velocity), 4)
        else:
            if abs(velocity) > sawyer_velocity_action_space[joint]:
                sawyer_velocity_action_space[joint] = round(abs(velocity), 4)

        if joint not in sawyer_effort_action_space:
            sawyer_effort_action_space[joint] = round(abs(effort), 4)
        else:
            if abs(effort) > sawyer_effort_action_space[joint]:
                sawyer_effort_action_space[joint] = round(abs(effort), 4)


def run():
    rospy.init_node('sawyer_action_space')
    rospy.Subscriber("/robot/joint_states", JointState, on_msg)
    rate = rospy.Rate(100)
    try:
        while not rospy.is_shutdown():
            rate.sleep()
    except:
        print('The velocity action space is: ', sawyer_velocity_action_space)
        print('The effort action space is: ', sawyer_effort_action_space)


if __name__ == '__main__':
    run()
