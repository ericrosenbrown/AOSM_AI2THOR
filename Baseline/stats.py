from viz_room import viz_room
from viz_room import viz_object_action_poses
from ai2thor.controller import Controller
from collections import defaultdict
import pickle

import matplotlib.pyplot as plt

def dd():
	return defaultdict(list)

def num_actions_per_room():
	total_actions = []
	for i in range(1,30):
		'''
		##### INITIALIZE CONTROLLERs
		controller = Controller(scene="FloorPlan"+str(i), gridSize=0.25,width=500,height=500)

		##### GET MAP
		event = controller.step(action='GetReachablePositions')
		room = event.metadata['actionReturn']
		'''
		floor_plan_i = pickle.load(open("action_maps/FloorPlan"+str(i)+"_amap_room.p","rb"))

		room = floor_plan_i["room"]

		num_free_spaces = len(room)
		num_orientations = 4
		num_manip_actions = 6
		total = num_free_spaces*num_orientations*num_manip_actions

		total_actions.append(total)

	plt.hist(total_actions,bins=10)
	plt.show()

if __name__ == "__main__":
	num_actions_per_room()
