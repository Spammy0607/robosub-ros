#!/usr/bin/env python
import json
from pprint import pprint
from robot_localization.srv import SetPose
from geometry_msgs.msg import PoseWithCovarianceStamped
from mavros_msgs.srv import StreamRate
import sys
import rospy
import importlib

class TaskPlanner:
    
    NODE_NAME = 'task_planner'
    
    # REFACTOR THIS
    CONTINUE = 1
    FINISHED = 2
    
    def __init__(self):
        plans_filename = sys.argv[1]
        tasks_path = sys.argv[2]
        self.plan_name = sys.argv[3]

        sys.path.append(tasks_path)

        with open(plans_filename) as plans_file:
            self.masterplan = json.load(plans_file)
        
        self.init_tasks(self.masterplan)
        self.plan = self.init_plan(self.masterplan, self.plan_name)
        
        rospy.init_node(self.NODE_NAME, log_level=rospy.INFO)
        
    def init_tasks(self, masterplan):
        self.tasks = []
        for task_info in masterplan['tasks']:
            task = getattr(importlib.import_module(task_info['modulename']), task_info['classname'])()
            self.tasks.append(task)
    
    def init_plan(self, masterplan, plan_name):
        target_plan = None
        for plan in masterplan['plans']:
            if plan['name'] == plan_name:
                target_plan = plan
                break
        
        if target_plan is None:
            raise Exception('Plan ' + plan_name + ' not found')
        
        task_names = target_plan['tasks']
        self.tasks_plan = map(self._get_task_from_name, task_names)
    
    def _get_task_from_name(self, name):
        return list(filter(lambda task: task.name == name, self.tasks))[0]
    
    def run(self):
        rospy.wait_for_service('/set_pose')
        sp = rospy.ServiceProxy('/set_pose', SetPose)
        zero_pose = PoseWithCovarianceStamped()
        zero_pose.pose.pose.orientation.w = 1
        sp(zero_pose)

        rospy.wait_for_service('/mavros/set_stream_rate')
        ssr = rospy.ServiceProxy('/mavros/set_stream_rate', StreamRate)
        ssr(0, 15, 1)

        rate = rospy.Rate(15)
        for task in self.tasks_plan:
            rospy.loginfo('Starting task: ' + task.name)
            task.pre_run()
            while not rospy.is_shutdown():
                result = task.run()
                if result == self.CONTINUE:
                    pass
                elif result == self.FINISHED:
                    break
                rate.sleep()


if __name__ == '__main__':
    TaskPlanner().run()