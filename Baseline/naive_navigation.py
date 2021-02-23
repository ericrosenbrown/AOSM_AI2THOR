from viz_room import viz_room
from viz_room import viz_object_action_poses
from ai2thor.controller import Controller
import pickle
from collections import defaultdict
import json 
import numpy as np
import math
import copy
import random
import math

from path_planner import rrt_path_planner

from PIL import Image

def nearest_neighbor(p,poses):
	#given a 2d point p ([x,y]) and a planning tree (list consisting of Nodes), return the node that is closest to p
	best_point = None #default point is root
	best_distance = float("inf")
	for point in poses:
		dist = np.linalg.norm(np.array([point['x'],point['z']])-np.array([p['x'],p['z']]))
		if dist < best_distance:
			best_point = point
			best_distance= dist
	return(best_point)

def get_angle(robot_pos,object_pos):
	#get angle for robot_pos to face object_pos
	y = (object_pos["x"] - robot_pos["x"])
	x = object_pos["z"] - robot_pos["z"]
	degree = math.atan2(y,x)*180/(math.pi)
	if degree < 0:
		degree = 360 + degree
	return(degree)

def rotate_test():
	floorPlan='FloorPlan6'
	gridSize = 0.25
	controller = Controller(scene=floorPlan, gridSize=gridSize,width=500,height=500)

	event = controller.step(action='GetReachablePositions')
	room = event.metadata['actionReturn']

	agent = event.metadata['agent']
	print("agent pos:",agent["position"])
	robot_pos = agent["position"]

	print("get angles")
	north = copy.deepcopy(agent["position"])
	north["x"]  -= 0.5
	print("north:",north, robot_pos)
	get_angle(robot_pos,north)
	get_angle(north,robot_pos)

	east = copy.deepcopy(agent["position"])
	east["z"]  += 0.5
	print("east:",east,robot_pos)
	get_angle(robot_pos,east)

	south = copy.deepcopy(agent["position"])
	south["x"]  += 0.5
	print("south:",south,robot_pos)
	get_angle(robot_pos,south)

	west = copy.deepcopy(agent["position"])
	west["z"]  -= 0.5
	print("west:",west,robot_pos)
	get_angle(robot_pos,west)

	#turn agent in different directions
	for degree in [0,90,180,270]:
		print("turn to degree:",degree)
		input()
		event = controller.step(action='TeleportFull', x=agent["position"]['x'], y=agent["position"]['y'], z=agent["position"]['z'], rotation=dict(x=0.0, y=degree, z=0.0), horizon=30.0,raise_for_failure=True)

	input("go north (decrement x)")
	event = controller.step(action='TeleportFull', x=agent["position"]['x']-0.5, y=agent["position"]['y'], z=agent["position"]['z'], rotation=dict(x=0.0, y=270, z=0.0), horizon=30.0,raise_for_failure=True)

	input("go south (increment x)")
	event = controller.step(action='TeleportFull', x=agent["position"]['x']+0.5, y=agent["position"]['y'], z=agent["position"]['z'], rotation=dict(x=0.0, y=270, z=0.0), horizon=30.0,raise_for_failure=True)

	input("go east (increment y)")
	event = controller.step(action='TeleportFull', x=agent["position"]['x'], y=agent["position"]['y'], z=agent["position"]['z']+0.25, rotation=dict(x=0.0, y=270, z=0.0), horizon=30.0,raise_for_failure=True)

	input("go west (decrement y)")
	event = controller.step(action='TeleportFull', x=agent["position"]['x'], y=agent["position"]['y'], z=agent["position"]['z']-0.25, rotation=dict(x=0.0, y=270, z=0.0), horizon=30.0,raise_for_failure=True)
	input("wait")


def plan_navigation(plan,gridSize=0.25,floorPlan='FloorPlan2'):
	fname = "baseline_images/"+floorPlan+"_toast_1/"
	counter = 0
	save_images = True

	controller = Controller(scene=floorPlan, gridSize=gridSize,width=500,height=500)

	event = controller.step(action='GetReachablePositions')
	room = event.metadata['actionReturn']

	input("wait")

	heldObject = None

	important_obj_refs = {}

	controller.step("LookDown")
	if save_images:
		im = Image.fromarray(event.frame)
		im.save(fname+str(counter)+".png")
		counter += 1

	for manip_step in manip_plan:
		action, obj, obj_highlevel_ref = manip_step

		obj_ref = None
		#referenced object has been assigned previously
		if obj_highlevel_ref in important_obj_refs.keys():
			obj_ref_id = important_obj_refs[obj_highlevel_ref]

			all_objs = event.metadata['objects']
			for possible_obj in all_objs:
				if possible_obj['objectId'] == obj_ref_id:
					obj_ref = possible_obj
			print("i've seen this object before:",obj_ref_id)


		#assign an object to be the referent, different than one in the existing setup
		else:
			#Find object reference
			all_objs = event.metadata['objects']
			random.shuffle(all_objs)
			for possible_obj in all_objs:
				#get an object of right category but not assigned yet
				if obj in possible_obj['objectId'] and possible_obj['objectId'] not in important_obj_refs.values():
					important_obj_refs[obj_highlevel_ref] = possible_obj['objectId']
					obj_ref = possible_obj
					break
			print("NEW OBJECT BINDING!",possible_obj['objectId'])

		#object loc
		object_loc = obj_ref['position']

		#nearest free pose to object
		closest_free_spot = nearest_neighbor(object_loc,room)

		degree = get_angle(closest_free_spot,object_loc)

		#########event = controller.step(action='TeleportFull', x=closest_free_spot['x'], y=closest_free_spot['y'], z=closest_free_spot['z'], rotation=dict(x=0.0, y=degree, z=0.0), horizon=30.0,raise_for_failure=True)
		clean_room = [[pos_dict['x'],pos_dict['z']] for pos_dict in room]
		agent = event.metadata['agent']
		robot_pose = [agent['position']['x'],agent['position']['y'],agent['position']['z'],0]
		goal_pose = [closest_free_spot['x'],closest_free_spot['y'],closest_free_spot['z'],degree]
		plan = rrt_path_planner(clean_room,robot_pose,goal_pose,threshold=0.25)
		plan.reverse()

		print("plan:",plan)

		##### TELEPORT MOVE #######
		
		for pos in plan:
			print("go to:",pos)
			print(pos[0],goal_pose[1],pos[1],0.0,goal_pose[3],0.0,30.0)
			input("")
			try:
				event = controller.step(action='TeleportFull', x=pos[0], y=goal_pose[1], z=pos[1], rotation=dict(x=0.0, y=goal_pose[3], z=0.0), horizon=30.0,raise_for_failure=True)
				if save_images:
					im = Image.fromarray(event.frame)
					im.save(fname+str(counter)+".png")
					counter += 1
			except:
				pass
		print("finsihed going!")

		###### ACTUAYL MOVE ####
		'''
		for i in range(1,len(plan)):
			print("go to:",plan[i-1],plan[i])
			robot_from = {"x":plan[i-1][0], "z":plan[i-1][1]}
			robot_to = {"x":plan[i][0], "z":plan[i][1]}

			robot_dist = np.linalg.norm(np.array(plan[i-1])-np.array(plan[i]))
			robot_degree_need = get_angle(robot_from,robot_to)

			agent = event.metadata['agent']
			print("robot position:",agent["position"])
			robot_degree_cur = agent['rotation']['y']
			rotation_delta = robot_degree_need - robot_degree_cur
			print("robot_degree_cur:",robot_degree_cur)
			print("Robot need to be:",robot_degree_need)
			print("rotate:",rotation_delta)
			print("robot move:",robot_dist)
			input("")
			event = controller.step(
				action="RotateRight",
				degrees=rotation_delta)
			input("move")
			event = controller.step(
				action="MoveAhead",
				moveMagnitude=robot_dist)

		print("finsihed going!")
		agent = event.metadata['agent']
		agent_pos = agent["position"]
		robot_degree_need = get_angle(agent_pos,object_loc)
		robot_degree_cur = agent['rotation']['y']
		rotation_delta = robot_degree_need - robot_degree_cur
		input("findal correct")
		event = controller.step(
				action="RotateRight",
				degrees=rotation_delta)

		print("robot position:",agent["position"])
		'''

		#################

		input("before manip")
		if action == "PickupObject":
			event = controller.step(action='PickupObject',
				objectId=obj_ref['objectId'],
				raise_for_failure=True)
			print("Picked up:",obj_ref['objectId'])
			heldObject = obj

		elif action == "SliceObject":
			event = controller.step(action='SliceObject',
				objectId=obj_ref['objectId'],
				raise_for_failure=True)
			print("Sliced:",obj_ref['objectId'])

		elif action == "PutObject":
			event = controller.step(action='PutObject',
				receptacleObjectId=obj_ref['objectId'],
				objectId=heldObject,
				raise_for_failure=True)
			print("Put down:",obj_ref['objectId'])

		elif action == "ToggleObjectOn":
			event = controller.step(action='ToggleObjectOn',
				objectId=obj_ref['objectId'],
				raise_for_failure=True)
			print("Toggle on:",obj_ref['objectId'])

		elif action == "ToggleObjectOff":
			event = controller.step(action='ToggleObjectOff',
				objectId=obj_ref['objectId'],
				raise_for_failure=True)
			print("Toggle off:",obj_ref['objectId'])

		if save_images:
			im = Image.fromarray(event.frame)
			im.save(fname+str(counter)+".png")
			counter += 1


		input("wait")



manip_plan = [["PickupObject","Knife","Knife0"],
["SliceObject","Bread","Bread0"],
["PutObject","CounterTop","CounterTop0"],
["PickupObject","BreadSliced","BreadSliced0"],
["PutObject","Toaster","Toaster0"],
["ToggleObjectOn","Toaster","Toaster0"],
["ToggleObjectOff","Toaster","Toaster0"],
["PickupObject","BreadSliced","BreadSliced0"],
]

floor_plans = [1,2,3,4,5,6,7,8,9,10,11]
plan_navigation(manip_plan,gridSize=0.25,floorPlan="FloorPlan6")

#rotate_test()