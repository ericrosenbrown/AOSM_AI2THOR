from ai2thor.controller import Controller
from viz_room import slam_viz_room, slam_viz_hidden_room
import numpy as np

def get_reachable_room(room,robot_position,gridSize=0.25):
	robox = int(robot_position[0]/gridSize)
	roboz = int(robot_position[1]/gridSize)

	box = 5

	reachable_spots = []
	for xd in range(-1*box,box):
		for zd in range(-1*box,box):
			reachable_spots.append([robox+xd,roboz+zd])

	'''
	for xyz in room:
		x = int(xyz['x']/gridSize)
		z = int(xyz['z']/gridSize)

		if np.linalg.norm(np.array([x,z])-np.array([robox,roboz])) <= thresh:
			reachable_spots.append([x,z])
	'''
	return(reachable_spots)



if __name__ == "__main__":
	i = 6
	gridSize = 0.25
	controller = Controller(scene="FloorPlan"+str(i), gridSize=gridSize,width=500,height=500,renderObjectImage=True,renderClassImage=True,renderDepthImage=True)

	event = controller.step(action='GetReachablePositions')
	room = event.metadata['actionReturn']

	agent = event.metadata['agent']
	robot_position = [agent['position']['x'],agent['position']['z']]

	rspots = get_reachable_room(room,robot_position)

	slam_viz_room(room,robot_position,gridSize)
	slam_viz_hidden_room(room,rspots,robot_position,gridSize)
	input("Wee!")

	event = controller.step(
				action="MoveAhead",
				moveMagnitude=gridSize*6)

	agent = event.metadata['agent']
	robot_position = [agent['position']['x'],agent['position']['z']]

	rspots += get_reachable_room(room,robot_position)

	slam_viz_hidden_room(room,rspots,robot_position,gridSize)
	input("Wee!")

	event = controller.step(
				action="RotateRight",
				degrees=90)

	event = controller.step(
				action="MoveAhead",
				moveMagnitude=gridSize*5)

	agent = event.metadata['agent']
	robot_position = [agent['position']['x'],agent['position']['z']]

	rspots += get_reachable_room(room,robot_position)

	slam_viz_hidden_room(room,rspots,robot_position,gridSize)
	input("Wee!")

	event = controller.step(
				action="MoveAhead",
				moveMagnitude=gridSize*5)

	agent = event.metadata['agent']
	robot_position = [agent['position']['x'],agent['position']['z']]

	rspots += get_reachable_room(room,robot_position)

	slam_viz_hidden_room(room,rspots,robot_position,gridSize)
	input("Wee!")

	event = controller.step(
				action="MoveAhead",
				moveMagnitude=gridSize*2)
	event = controller.step(
				action="RotateRight",
				degrees=90)

	agent = event.metadata['agent']
	robot_position = [agent['position']['x'],agent['position']['z']]

	rspots += get_reachable_room(room,robot_position)

	slam_viz_hidden_room(room,rspots,robot_position,gridSize)
	input("Wee!")

	event = controller.step(
				action="MoveAhead",
				moveMagnitude=gridSize*5)

	agent = event.metadata['agent']
	robot_position = [agent['position']['x'],agent['position']['z']]

	rspots += get_reachable_room(room,robot_position)

	slam_viz_hidden_room(room,rspots,robot_position,gridSize)
	input("Wee!")

	event = controller.step(
				action="MoveAhead",
				moveMagnitude=gridSize*4)
	event = controller.step(
				action="RotateRight",
				degrees=90)

	agent = event.metadata['agent']
	robot_position = [agent['position']['x'],agent['position']['z']]

	rspots += get_reachable_room(room,robot_position)

	slam_viz_hidden_room(room,rspots,robot_position,gridSize)
	input("Wee!")

	event = controller.step(
				action="MoveAhead",
				moveMagnitude=gridSize*5)

	agent = event.metadata['agent']
	robot_position = [agent['position']['x'],agent['position']['z']]

	rspots += get_reachable_room(room,robot_position)

	slam_viz_hidden_room(room,rspots,robot_position,gridSize)
	input("Wee!")

