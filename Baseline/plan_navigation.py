from viz_room import viz_room
from viz_room import viz_object_action_poses
from ai2thor.controller import Controller
import pickle
from collections import defaultdict
import json 
import numpy as np

from path_planner import rrt_path_planner

def dd():
	return defaultdict(ddd)

def ddd():
	return defaultdict(list)

def nearest_neighbor(p,poses):
	#given a 2d point p ([x,y]) and a planning tree (list consisting of Nodes), return the node that is closest to p
	best_point = None #default point is root
	best_distance = float("inf")
	for point in poses:
		dist = np.linalg.norm(np.array([eval(point)['x'],eval(point)['z']])-np.array([p['x'],p['z']]))
		if dist < best_distance:
			best_point = point
			best_distance= dist
	return(best_point)


def plan_navigation(room,action_map,gridSize=0.25,floorPlan='FloorPlan6'):
	controller = Controller(scene=floorPlan, gridSize=gridSize,width=500,height=500)

	event = controller.step(action='GetReachablePositions')

	manip_plan = [["PickupObject","Knife|-00.64|+00.91|+01.62"],["SliceObject","Bread|-00.71|+00.98|+00.43"]]

	for hlp in manip_plan:
		#print(hlp)
		agent = event.metadata['agent']
		robot_pose = [agent['position']['x'],agent['position']['y'],agent['position']['z'],0]

		action, objectId = hlp

		current_object_pose = None
		for allobj in event.metadata['objects']:
			if allobj['objectId'] == objectId:
				current_object_pose = allobj['position']
				break
		action_object_dict = action_map[action][objectId]

		bestObjLoc = nearest_neighbor(current_object_pose,action_object_dict.keys())

		print("possible object locaitons:",action_object_dict.keys())
		print("best obj spot:",bestObjLoc)
		#just choose first valid robot pose ([0] index)
		goal_pose = action_object_dict[bestObjLoc][0]
		#print("a stuff:",action_object_dict[bestObjLoc])
		print("starting_pose:",robot_pose)
		print("goal_pose:",goal_pose)

		clean_room = [[pos_dict['x'],pos_dict['z']] for pos_dict in room]
		plan = rrt_path_planner(clean_room,robot_pose,goal_pose,threshold=0.25)
		plan.reverse()

		print("plan:",plan)

		for pos in plan:
			event = controller.step(action='TeleportFull', x=pos[0], y=goal_pose[1], z=pos[1], rotation=dict(x=0.0, y=goal_pose[3], z=0.0), horizon=30.0,raise_for_failure=True)
			input("go")

		if action == "PickupObject":
			obj1_pos = bestObjLoc
			event = controller.step(action='PickupObject',
				objectId=objectId,
				raise_for_failure=True)
			print("Picked up:",objectId)
			heldObject = objectId

		if action == "SliceObject":
			obj1_pos = bestObjLoc
			event = controller.step(action='SliceObject',
				objectId=objectId,
				raise_for_failure=True)
			print("Sliced:",objectId)



premade = pickle.load(open("action_maps/lotsa_new_amap_FloorPlan6_toast_bread.p","rb"))
room = premade['room']
action_map = premade['action_map']

plan_navigation(room,action_map)
