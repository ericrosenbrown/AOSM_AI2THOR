from viz_room import viz_room
from viz_room import viz_object_action_poses
from ai2thor.controller import Controller
from collections import defaultdict
import pickle
import random
from tqdm import tqdm

def dd():
	return defaultdict(ddd)

def ddd():
	return defaultdict(list)

def importantObject(check_obj,task):
	if task == "cook_egg":
		important_objects = ["Egg","Pan","Stove"]
	elif task == "toast_bread":
		important_objects = ["Bread","Toaster","Knife","CounterTop|-00.36|+00.95|+01.09","CounterTop|-01.49|+00.95|+01.32"]

	for io in important_objects:
		if io in check_obj:
			return True
	return False


def make_actionmap(floorPlan='FloorPlan6',task="toast_bread",gridSize=0.25):
	##### INITIALIZE CONTROLLERs
	controller = Controller(scene=floorPlan, gridSize=gridSize,width=500,height=500)

	##### GET MAP
	event = controller.step(action='GetReachablePositions')
	room = event.metadata['actionReturn']
	orientations = [0,90,180,270]

	#action_map[action][tuple of objects ids][list of object poses] = [list of robot poses]
	action_map = defaultdict(dd)

	agent = event.metadata['agent']
	robot_position = [agent['position']['x'],agent['position']['y'],agent['position']['z']]

	#viz_room(room,robot_position,gridSize=gridSize)

	##### GO TO EACH FREE POSE AND TRY ACTIONS
	#shuffle room poses

	attempts = 10
	total_attempts = []

	for _ in range(attempts):
		num_steps = 0

		random.shuffle(room)

		for xyz in tqdm(room):
			if task == "toast_bread":
				stopper_objects = event.metadata['objects']
				objects_cooked = map(lambda x: x['isCooked'], stopper_objects)
				if True in objects_cooked:
					print("LOOKS LIKE SOMETHING COOKED, RESET!")
					event = controller.reset(scene=floorPlan)
					total_attempts.append(num_steps)
					break

			x = xyz['x']
			y = xyz['y']
			z = xyz['z']

			#for each position, try a bunch of different shuffled rotations
			random.shuffle(orientations)
			for rotation in orientations:
				event = controller.step(action='TeleportFull', x=x, y=y, z=z, rotation=dict(x=0.0, y=rotation, z=0.0), horizon=30.0)
				num_steps += 1
				#go through all objects in the scene at this current event in random order
				#TODO randomize action order
				cur_objects = event.metadata['objects']
				random.shuffle(cur_objects)
				for o in cur_objects:
					if not importantObject(o['objectId'],task):
						continue
					#PickUp
					if task == "cook_egg" or task == "toast_bread":
						try:
							obj1_pos = o['position']
							event = controller.step(action='PickupObject',
								objectId=o['objectId'],
								raise_for_failure=True)
							print("Picked up:",o['objectId'])
							num_steps += 1
							heldObject = o['objectId']
							action_map['PickupObject'][o['objectId']][str(obj1_pos)].append([x,y,z,rotation])
						except:
							pass

					if task == "cook_egg" or task == "toast_bread":
						#PutObject
						try:
							obj1_pos = o['position']					
							event = controller.step(action='PutObject',
								receptacleObjectId=o['objectId'],
								objectId=heldObject,
								raise_for_failure=True)
							print("Placed:",heldObject,o['objectId'])
							num_steps += 1
							action_map['PutObject'][heldObject+"*"+o['objectId']][str(obj1_pos)].append([x,y,z,rotation])
						except:
							pass

					if task =="cook_egg" or task == "toast_bread":
						#ToggleOnObject
						try:
							obj1_pos = o['position']					
							event = controller.step(action='ToggleObjectOn',
								objectId=o['objectId'],
								raise_for_failure=True)
							print("Turned On:",o['objectId'])
							num_steps += 1
							action_map['ToggleObjectOn'][o['objectId']][str(obj1_pos)].append([x,y,z,rotation])
						except:
							pass

					if task == "cook_egg" or task == "toast_bread":
						#ToggleObjectOff
						try:
							obj1_pos = o['position']					
							event = controller.step(action='ToggleObjectOff',
								objectId=o['objectId'],
								raise_for_failure=True)
							print("Turned Off:",o['objectId'])
							num_steps += 1
							action_map['ToggleObjectOff'][o['objectId']][str(obj1_pos)].append([x,y,z,rotation])
						except:
							pass

					if task == "cook_egg" or task == "toast_bread":
						#SliceObject
						try:
							obj1_pos = o['position']					
							event = controller.step(action='SliceObject',
								objectId=o['objectId'],
								raise_for_failure=True)
							print("Sliced:",o['objectId'])
							num_steps += 1
							action_map['SliceObject'][o['objectId']][str(obj1_pos)].append([x,y,z,rotation])
						except:
							pass

					'''

					#allows ToggleObjectOn
					if o['visible'] and o['toggleable'] and not o['obstructed']:
						action_map[o['objectId']]['ToggleObjectOn'].append([x_raw,y_raw,z_raw,rotation])
					#allows PutObject
					if o['visible'] and o['receptacle'] and not o['obstructed']:
						action_map[o['objectId']]['PutObject'].append([x_raw,y_raw,z_raw,rotation])
					#allows SliceObject
					if o['visible'] and o['sliceable'] and not o['obstructed']:
						action_map[o['objectId']]['SliceObject'].append([x_raw,y_raw,z_raw,rotation])
					'''

		#pickle.dump({"action_map":action_map, "room":room}, open("action_maps/lots50a_new_amap_"+floorPlan+"_"+task+".p", "wb" ) )
		#print(action_map.keys())
		#print("RAN OUTA STEPS, RESET!")
		event = controller.reset(scene=floorPlan)
		total_attempts.append(num_steps)
	controller.stop()
	print("counts:",total_attempts)

if __name__ == "__main__":
	fp = 6
	make_actionmap(floorPlan="FloorPlan"+str(fp),task="toast_bread",gridSize=0.25)

	'''
	generate = True
	if generate:
		for fp in range(1,30):
			make_actionmap(floorPlan="FloorPlan"+str(fp),gridSize=0.25)
	else:
		premade = pickle.load(open("action_maps/FloorPlan2_amap.p","rb"))
		room = premade["room"]
		action_map = premade["action_map"]
		controller = Controller(scene="FloorPlan2", gridSize=0.25,width=500,height=500)
		##### VIZ ALL IMAGES FROM POSES FOR TOGGLING A SPECIFIC STOVEKNOB
		viz_object_action_poses(room,[01.60,00.63],action_map['StoveKnob|+01.60|+00.92|+00.63']['ToggleObjectOn'])

		for pose in action_map['StoveKnob|+01.60|+00.92|+00.63']['ToggleObjectOn']:
			event = controller.step(action='TeleportFull', x=pose[0], y=pose[1], z=pose[2], rotation=dict(x=0.0, y=pose[3], z=0.0), horizon=30.0)
			input("next")
	'''
		