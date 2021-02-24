def random_policy(floors,task="toast_bread",gridSize=0.25):
	max_steps = 10000
	num_attempts = 10
	total_steps = {}
	for floor in floors:
		##### INITIALIZE CONTROLLERs
		controller = Controller(scene=floor, gridSize=gridSize,width=500,height=500)
		for attempt in range(num_attempts):
			for step in range(max_steps):

