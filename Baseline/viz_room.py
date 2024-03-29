import pickle
from collections import defaultdict
import json 
from ai2thor.controller import Controller
import pickle
from collections import defaultdict
import json 
import numpy as np
import math
import copy
import random
import math

def dd():
	return defaultdict(ddd)

def ddd():
	return defaultdict(list)

def slam_viz_hidden_room(room,seen_room,robot_position,gridSize=0.25):
	minx = 1000000
	minz = 1000000
	maxx = -1000000
	maxz = -1000000

	robox = int(robot_position[0]/gridSize)
	roboz = int(robot_position[1]/gridSize)

	freespace = []
	for xyz in room:
		x = int(xyz['x']/gridSize)
		z = int(xyz['z']/gridSize)

		if x <= minx:
			minx = x
		if x >= maxx:
			maxx = x
		if z <= minz:
			minz = z
		if z >= maxz:
			maxz = z
		freespace.append([x,z])

	for i in range(minx-3,maxx+3):
		rowstr = ""
		for j in range(minz-3,maxz+3):
			if [i,j] in seen_room:
				if i == robox and j == roboz:
					rowstr += "R"
				elif [i,j] in freespace:
					rowstr += "."
				else:
					rowstr += "+"
			else:
				rowstr += " "
		print(rowstr)

def slam_viz_room(room,robot_position,gridSize=0.25):
	minx = 1000000
	minz = 1000000
	maxx = -1000000
	maxz = -1000000

	robox = int(robot_position[0]/gridSize)
	roboz = int(robot_position[1]/gridSize)

	freespace = []
	for xyz in room:
		x = int(xyz['x']/gridSize)
		z = int(xyz['z']/gridSize)

		if x <= minx:
			minx = x
		if x >= maxx:
			maxx = x
		if z <= minz:
			minz = z
		if z >= maxz:
			maxz = z
		freespace.append([x,z])

	for i in range(minx-3,maxx+3):
		rowstr = ""
		for j in range(minz-3,maxz+3):
			if i == robox and j == roboz:
				rowstr += "R"
			elif [i,j] in freespace:
				rowstr += "."
			else:
				rowstr += "+"
		print(rowstr)

def viz_room(room,robot_position,gridSize=0.25):
	minx = 1000000
	minz = 1000000
	maxx = -1000000
	maxz = -1000000
	freespace = []
	for xyz in room:
		x = int(xyz['x']/gridSize)
		z = int(xyz['z']/gridSize)

		if x <= minx:
			minx = x
		if x >= maxx:
			maxx = x
		if z <= minz:
			minz = z
		if z >= maxz:
			maxz = z
		freespace.append([x,z])

	for i in range(minx-3,maxx+3):
		rowstr = ""
		for j in range(minz-3,maxz+3):
			if i == robot_position[0] and j == robot_position[1]:
				rowstr += "."
			elif [i,j] in freespace:
				rowstr += " "
			else:
				rowstr += "."
		print(rowstr)

def viz_object_action_poses(room,object_position,action_positions,gridSize=0.25):
	minx = 1000000
	minz = 1000000
	maxx = -1000000
	maxz = -1000000
	freespace = []
	for xyz in room:
		x = int(xyz['x']/gridSize)
		z = int(xyz['z']/gridSize)

		if x <= minx:
			minx = x
		if x >= maxx:
			maxx = x
		if z <= minz:
			minz = z
		if z >= maxz:
			maxz = z
		freespace.append([x,z])

	for i in range(minx-3,maxx+3):
		rowstr = ""
		for j in range(minz-3,maxz+3):
			printed = False
			for a in action_positions:
				if i == int(a[0]/gridSize) and j == int(a[2]/gridSize):
					rowstr += "A"
					printed = True
					break
			if printed:
				pass
			elif i == int(object_position[0]/gridSize) and j == int(object_position[1]/gridSize):
				rowstr += "O"
			elif [i,j] in freespace:
				rowstr += " "
			else:
				rowstr += "."
		print(rowstr)

def viz_action_objectid_objectpose(room,action_map,gridSize=0.25):
	action1 = "PickupObject"
	objectId1 = "Knife|-00.64|+00.91|+01.62"

	action2 = "SliceObject"
	objectId2 = "Bread|-00.71|+00.98|+00.43"

	action3 = "PutObject"
	objectId3 = "Knife|-00.64|+00.91|+01.62*CounterTop|-00.36|+00.95|+01.09"

	action4 = "PickupObject"
	objectId4 = 'Bread|-00.71|+00.98|+00.43|BreadSliced_1'

	action5 = "PutObject"
	objectId5 = 'Bread|-00.71|+00.98|+00.43|BreadSliced_1*Toaster|-02.57|+00.90|+01.88'

	action6 = "ToggleObjectOn"
	objectId6 = "Toaster|-02.57|+00.90|+01.88"


	#action_object_dict = action_map["PickupObject"]["Bread|-00.71|+00.98|+00.43"]
	action_object_dict = action_map[action2][objectId2]
	print("ma keys:",action_object_dict.keys())

	minx = 1000000
	minz = 1000000
	maxx = -1000000
	maxz = -1000000
	freespace = []
	for xyz in room:
		x = int(xyz['x']/gridSize)
		z = int(xyz['z']/gridSize)

		if x <= minx:
			minx = x
		if x >= maxx:
			maxx = x
		if z <= minz:
			minz = z
		if z >= maxz:
			maxz = z
		freespace.append([x,z])

	for obj in action_object_dict.keys():
		obj_pos = eval(obj)
		robot_poses = action_object_dict[obj]

		for i in range(minx-3,maxx+3):
			rowstr = ""
			for j in range(minz-3,maxz+3):
				printed = False
				for a in robot_poses:
					if i == int(a[0]/gridSize) and j == int(a[2]/gridSize):
						rowstr += "A"
						printed = True
						break
				if printed:
					pass
				elif i == int(obj_pos["x"]/gridSize) and j == int(obj_pos["z"]/gridSize):
					rowstr += "O"
				elif [i,j] in freespace:
					rowstr += " "
				else:
					rowstr += "."
			print(rowstr)



if __name__ == "__main__":
	#fp2 = [{'x': -1.0, 'y': 0.900999248, 'z': -0.75}, {'x': -0.75, 'y': 0.900999248, 'z': -0.75}, {'x': -1.0, 'y': 0.900999248, 'z': -0.5}, {'x': -0.5, 'y': 0.900999248, 'z': -0.75}, {'x': -0.75, 'y': 0.900999248, 'z': -0.5}, {'x': -1.0, 'y': 0.900999248, 'z': -0.25}, {'x': -0.25, 'y': 0.900999248, 'z': -0.75}, {'x': -0.75, 'y': 0.900999248, 'z': -0.25}, {'x': -1.0, 'y': 0.900999248, 'z': 0.0}, {'x': 0.0, 'y': 0.900999248, 'z': -0.75}, {'x': -0.75, 'y': 0.900999248, 'z': 0.0}, {'x': -1.0, 'y': 0.900999248, 'z': 0.25}, {'x': 0.25, 'y': 0.900999248, 'z': -0.75}, {'x': -0.75, 'y': 0.900999248, 'z': 0.25}, {'x': -1.0, 'y': 0.900999248, 'z': 0.5}, {'x': 0.5, 'y': 0.900999248, 'z': -0.75}, {'x': -0.75, 'y': 0.900999248, 'z': 0.5}, {'x': -1.0, 'y': 0.900999248, 'z': 0.75}, {'x': 0.75, 'y': 0.900999248, 'z': -0.75}, {'x': -0.75, 'y': 0.900999248, 'z': 0.75}, {'x': -1.0, 'y': 0.900999248, 'z': 1.0}, {'x': 1.0, 'y': 0.900999248, 'z': -0.75}, {'x': 0.75, 'y': 0.900999248, 'z': -0.5}, {'x': -0.75, 'y': 0.900999248, 'z': 1.0}, {'x': -1.0, 'y': 0.900999248, 'z': 1.25}, {'x': 1.0, 'y': 0.900999248, 'z': -0.5}, {'x': 0.75, 'y': 0.900999248, 'z': -0.25}, {'x': -0.75, 'y': 0.900999248, 'z': 1.25}, {'x': -1.0, 'y': 0.900999248, 'z': 1.5}, {'x': -1.25, 'y': 0.900999248, 'z': 1.25}, {'x': 1.0, 'y': 0.900999248, 'z': -0.25}, {'x': 0.75, 'y': 0.900999248, 'z': 0.0}, {'x': -0.75, 'y': 0.900999248, 'z': 1.5}, {'x': -1.0, 'y': 0.900999248, 'z': 1.75}, {'x': -1.25, 'y': 0.900999248, 'z': 1.5}, {'x': 1.0, 'y': 0.900999248, 'z': 0.0}, {'x': 0.75, 'y': 0.900999248, 'z': 0.25}, {'x': -0.75, 'y': 0.900999248, 'z': 1.75}, {'x': -1.0, 'y': 0.900999248, 'z': 2.0}, {'x': -1.25, 'y': 0.900999248, 'z': 1.75}, {'x': 1.25, 'y': 0.900999248, 'z': 0.0}, {'x': 1.0, 'y': 0.900999248, 'z': 0.25}, {'x': 0.75, 'y': 0.900999248, 'z': 0.5}, {'x': -0.5, 'y': 0.900999248, 'z': 1.75}, {'x': -0.75, 'y': 0.900999248, 'z': 2.0}, {'x': -1.0, 'y': 0.900999248, 'z': 2.25}, {'x': -1.25, 'y': 0.900999248, 'z': 2.0}, {'x': 1.25, 'y': 0.900999248, 'z': 0.25}, {'x': 1.0, 'y': 0.900999248, 'z': 0.5}, {'x': 0.75, 'y': 0.900999248, 'z': 0.75}, {'x': -0.25, 'y': 0.900999248, 'z': 1.75}, {'x': -0.5, 'y': 0.900999248, 'z': 2.0}, {'x': -0.75, 'y': 0.900999248, 'z': 2.25}, {'x': -1.0, 'y': 0.900999248, 'z': 2.5}, {'x': -1.25, 'y': 0.900999248, 'z': 2.25}, {'x': -1.5, 'y': 0.900999248, 'z': 2.0}, {'x': 1.25, 'y': 0.900999248, 'z': 0.5}, {'x': 1.0, 'y': 0.900999248, 'z': 0.75}, {'x': 0.75, 'y': 0.900999248, 'z': 1.0}, {'x': 0.0, 'y': 0.900999248, 'z': 1.75}, {'x': -0.25, 'y': 0.900999248, 'z': 2.0}, {'x': -0.5, 'y': 0.900999248, 'z': 2.25}, {'x': -0.75, 'y': 0.900999248, 'z': 2.5}, {'x': -1.0, 'y': 0.900999248, 'z': 2.75}, {'x': -1.25, 'y': 0.900999248, 'z': 2.5}, {'x': -1.5, 'y': 0.900999248, 'z': 2.25}, {'x': -1.75, 'y': 0.900999248, 'z': 2.0}, {'x': 1.25, 'y': 0.900999248, 'z': 0.75}, {'x': 1.0, 'y': 0.900999248, 'z': 1.0}, {'x': 0.75, 'y': 0.900999248, 'z': 1.25}, {'x': 0.25, 'y': 0.900999248, 'z': 1.75}, {'x': 0.0, 'y': 0.900999248, 'z': 2.0}, {'x': -0.25, 'y': 0.900999248, 'z': 2.25}, {'x': -0.5, 'y': 0.900999248, 'z': 2.5}, {'x': -0.75, 'y': 0.900999248, 'z': 2.75}, {'x': -1.0, 'y': 0.900999248, 'z': 3.0}, {'x': -1.25, 'y': 0.900999248, 'z': 2.75}, {'x': -1.5, 'y': 0.900999248, 'z': 2.5}, {'x': -1.75, 'y': 0.900999248, 'z': 2.25}, {'x': -2.0, 'y': 0.900999248, 'z': 2.0}, {'x': 1.25, 'y': 0.900999248, 'z': 1.0}, {'x': 1.0, 'y': 0.900999248, 'z': 1.25}, {'x': 0.75, 'y': 0.900999248, 'z': 1.5}, {'x': 0.5, 'y': 0.900999248, 'z': 1.75}, {'x': 0.25, 'y': 0.900999248, 'z': 2.0}, {'x': 0.0, 'y': 0.900999248, 'z': 2.25}, {'x': -0.25, 'y': 0.900999248, 'z': 2.5}, {'x': -0.5, 'y': 0.900999248, 'z': 2.75}, {'x': -0.75, 'y': 0.900999248, 'z': 3.0}, {'x': -1.0, 'y': 0.900999248, 'z': 3.25}, {'x': -1.25, 'y': 0.900999248, 'z': 3.0}, {'x': -1.5, 'y': 0.900999248, 'z': 2.75}, {'x': -1.75, 'y': 0.900999248, 'z': 2.5}, {'x': -2.0, 'y': 0.900999248, 'z': 2.25}, {'x': 1.25, 'y': 0.900999248, 'z': 1.25}, {'x': 1.0, 'y': 0.900999248, 'z': 1.5}, {'x': 0.75, 'y': 0.900999248, 'z': 1.75}, {'x': 0.5, 'y': 0.900999248, 'z': 2.0}, {'x': 0.25, 'y': 0.900999248, 'z': 2.25}, {'x': 0.0, 'y': 0.900999248, 'z': 2.5}, {'x': -0.25, 'y': 0.900999248, 'z': 2.75}, {'x': -0.5, 'y': 0.900999248, 'z': 3.0}, {'x': -0.75, 'y': 0.900999248, 'z': 3.25}, {'x': -1.0, 'y': 0.900999248, 'z': 3.5}, {'x': -1.25, 'y': 0.900999248, 'z': 3.25}, {'x': -1.5, 'y': 0.900999248, 'z': 3.0}, {'x': -1.75, 'y': 0.900999248, 'z': 2.75}, {'x': -2.0, 'y': 0.900999248, 'z': 2.5}, {'x': -2.25, 'y': 0.900999248, 'z': 2.25}, {'x': 1.0, 'y': 0.900999248, 'z': 1.75}, {'x': 0.75, 'y': 0.900999248, 'z': 2.0}, {'x': 0.5, 'y': 0.900999248, 'z': 2.25}, {'x': 0.25, 'y': 0.900999248, 'z': 2.5}, {'x': 0.0, 'y': 0.900999248, 'z': 2.75}, {'x': -0.25, 'y': 0.900999248, 'z': 3.0}, {'x': -0.5, 'y': 0.900999248, 'z': 3.25}, {'x': -0.75, 'y': 0.900999248, 'z': 3.5}, {'x': -1.5, 'y': 0.900999248, 'z': 3.25}, {'x': -1.75, 'y': 0.900999248, 'z': 3.0}, {'x': -2.0, 'y': 0.900999248, 'z': 2.75}, {'x': -2.25, 'y': 0.900999248, 'z': 2.5}, {'x': -2.5, 'y': 0.900999248, 'z': 2.25}, {'x': 1.0, 'y': 0.900999248, 'z': 2.0}, {'x': 0.75, 'y': 0.900999248, 'z': 2.25}, {'x': 0.5, 'y': 0.900999248, 'z': 2.5}, {'x': 0.25, 'y': 0.900999248, 'z': 2.75}, {'x': 0.0, 'y': 0.900999248, 'z': 3.0}, {'x': -0.25, 'y': 0.900999248, 'z': 3.25}, {'x': -0.5, 'y': 0.900999248, 'z': 3.5}, {'x': -1.75, 'y': 0.900999248, 'z': 3.25}, {'x': -2.0, 'y': 0.900999248, 'z': 3.0}, {'x': -2.25, 'y': 0.900999248, 'z': 2.75}, {'x': -2.5, 'y': 0.900999248, 'z': 2.5}, {'x': -2.75, 'y': 0.900999248, 'z': 2.25}, {'x': 1.0, 'y': 0.900999248, 'z': 2.25}, {'x': 0.75, 'y': 0.900999248, 'z': 2.5}, {'x': 0.5, 'y': 0.900999248, 'z': 2.75}, {'x': 0.25, 'y': 0.900999248, 'z': 3.0}, {'x': 0.0, 'y': 0.900999248, 'z': 3.25}, {'x': -2.0, 'y': 0.900999248, 'z': 3.25}, {'x': -2.25, 'y': 0.900999248, 'z': 3.0}, {'x': -2.5, 'y': 0.900999248, 'z': 2.75}, {'x': -2.75, 'y': 0.900999248, 'z': 2.5}, {'x': 1.0, 'y': 0.900999248, 'z': 2.5}, {'x': 0.75, 'y': 0.900999248, 'z': 2.75}, {'x': 0.5, 'y': 0.900999248, 'z': 3.0}, {'x': 0.25, 'y': 0.900999248, 'z': 3.25}, {'x': -2.25, 'y': 0.900999248, 'z': 3.25}, {'x': -2.5, 'y': 0.900999248, 'z': 3.0}, {'x': -2.75, 'y': 0.900999248, 'z': 2.75}, {'x': 1.0, 'y': 0.900999248, 'z': 2.75}, {'x': 0.75, 'y': 0.900999248, 'z': 3.0}, {'x': 0.5, 'y': 0.900999248, 'z': 3.25}, {'x': -2.5, 'y': 0.900999248, 'z': 3.25}, {'x': -2.75, 'y': 0.900999248, 'z': 3.0}, {'x': 1.0, 'y': 0.900999248, 'z': 3.0}, {'x': 0.75, 'y': 0.900999248, 'z': 3.25}, {'x': -2.75, 'y': 0.900999248, 'z': 3.25}, {'x': 1.0, 'y': 0.900999248, 'z': 3.25}]
	#viz_room(fp2,[0,0])

	#premade = pickle.load(open("action_maps/new_amap_FloorPlan6_toast_bread.p","rb"))
	#premade = pickle.load(open("action_maps/lotsa_new_amap_FloorPlan6_toast_bread.p","rb"))
	premade = pickle.load(open("action_maps/FloorPlan2_amap.p","rb"))
	room = premade['room']
	action_map = premade['action_map']
	viz_room(room,[0,0])
	#viz_action_objectid_objectpose(room,action_map,gridSize=0.25)