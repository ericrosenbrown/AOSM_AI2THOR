from viz_room import viz_room
from viz_room import viz_object_action_poses
from ai2thor.controller import Controller
from collections import defaultdict
import pickle

def dd():
	return defaultdict(list)

def make_actionmap(floorPlan='FloorPlan2',gridSize=0.25):
	##### INITIALIZE CONTROLLERs
	controller = Controller(scene=floorPlan, gridSize=gridSize,width=500,height=500)

	##### GET MAP
	event = controller.step(action='GetReachablePositions')
	room = event.metadata['actionReturn']

	#action_map['object_id']['action'] = [list of TeleportFull poses]
	action_map = defaultdict(dd)

	agent = event.metadata['agent']
	robot_position = [int(agent['position']['x']/gridSize),int(agent['position']['y']/gridSize),int(agent['position']['z']/gridSize)]

	#viz_room(room,robot_position,gridSize=gridSize)

	##### GO TO EACH FREE POSE AND TRY ACTIONS
	for xyz in room:
		x_raw = xyz['x']
		y_raw = xyz['y']
		z_raw = xyz['z']

		x = int(x_raw/gridSize)
		y = int(y_raw/gridSize)
		z = int(z_raw/gridSize)

		#for each position, try a bunch of different rotations
		for rotation in [0,90,180,270]:
			event = controller.step(action='TeleportFull', x=x_raw, y=y_raw, z=z_raw, rotation=dict(x=0.0, y=rotation, z=0.0), horizon=30.0)

			#go through all objects in the scene at this current event
			for o in event.metadata['objects']:
				#if object is visible and pickupable, then this location allows PickupObject
				if o['visible'] and o['pickupable'] and not o['obstructed']:
					action_map[o['objectId']]['PickupObject'].append([x_raw,y_raw,z_raw,rotation])
				#allows ToggleObjectOn
				if o['visible'] and o['toggleable'] and not o['obstructed']:
					action_map[o['objectId']]['ToggleObjectOn'].append([x_raw,y_raw,z_raw,rotation])
				#allows PutObject
				if o['visible'] and o['receptacle'] and not o['obstructed']:
					action_map[o['objectId']]['PutObject'].append([x_raw,y_raw,z_raw,rotation])
				#allows SliceObject
				if o['visible'] and o['sliceable'] and not o['obstructed']:
					action_map[o['objectId']]['SliceObject'].append([x_raw,y_raw,z_raw,rotation])



	pickle.dump({"action_map":action_map, "room":room}, open("action_maps/"+floorPlan+"_amap.p", "wb" ) )
	controller.stop()

if __name__ == "__main__":
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
		