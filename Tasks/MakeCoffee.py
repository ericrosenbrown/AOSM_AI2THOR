from ai2thor.controller import Controller
controller = Controller(scene='FloorPlan9', gridSize=0.25)

input("move ahead")
event = controller.step(action='MoveAhead', moveMagnitude=0.25 * 2)
input("move ahead")
event = controller.step(action='RotateRight')
input("move ahead")
event = controller.step(action='MoveAhead', moveMagnitude=0.25 * 5)
input("move ahead")
event = controller.step(action='RotateRight')
input("move ahead")

# put the object in the microwave
for o in event.metadata['objects']:
    if o['visible'] and o['objectType'] == 'CoffeeMachine':
        coffeemaker_object_id = o['objectId']
        # pick up the Bread
        event = controller.step(action='ToggleObjectOn',
                                objectId=o['objectId'],
                                raise_for_failure=True)
        break
input("toaster on")

for o in event.metadata['objects']:
    if o['visible'] and o['pickupable'] and o['objectType'] == 'Mug':
        # pick up the Bread
        event = controller.step(action='PickupObject',
                                objectId=o['objectId'],
                                raise_for_failure=True)
        mug_object_id = o['objectId']
        break
input("toast out")
