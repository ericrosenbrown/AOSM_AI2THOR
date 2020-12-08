from ai2thor.controller import Controller
controller = Controller(scene='FloorPlan6', gridSize=0.25)

input("move ahead")
event = controller.step(action='MoveAhead', moveMagnitude=0.25 * 6)
input("rotate right")
event = controller.step(action='RotateRight')
input("moe ahead")
event = controller.step(action='MoveAhead', moveMagnitude=0.25 * 10)
input("rotate right")
event = controller.step(action='RotateRight')
input("rotate right")
even= controller.step(action='LookDown')
input("rotate right")

for o in event.metadata['objects']:
    if o['visible'] and o['pickupable'] and o['objectType'] == 'Knife':
        # pick up the knife
        event = controller.step(action='PickupObject',
                                objectId=o['objectId'],
                                raise_for_failure=True)
        knife_object_id = o['objectId']
        break

input("rotate right")
event = controller.step(action='RotateRight')
input("rotate right")
event = controller.step(action='MoveAhead', moveMagnitude=0.25 * 4)
input("rotate right")
event = controller.step(action='RotateLeft')
input("rotate right")

for o in event.metadata['objects']:
    if o['visible'] and o['sliceable'] and o['objectType'] == 'Bread':
        print("bread is visibile!")
        event = controller.step(action='SliceObject',
                                objectId=o['objectId'],
                                raise_for_failure=True)
        Bread_object_id = o['objectId']
        break

input("sliced?")
event = controller.step(action='DropHandObject')
input("dropped")
for o in event.metadata['objects']:
    if o['visible'] and o['pickupable'] and o['objectType'] == 'BreadSliced':
        # pick up the Bread
        event = controller.step(action='PickupObject',
                                objectId=o['objectId'],
                                raise_for_failure=True)
        breadslice_object_id = o['objectId']
        print("toast is",o['isCooked'])
        break

input("bread slice?")
event = controller.step(action='RotateLeft')
input("rotate right")
event = controller.step(action='MoveAhead', moveMagnitude=0.25 * 4)
input("rotate right")
event = controller.step(action='RotateLeft')
input("rotate right")

# put the object in the microwave
for o in event.metadata['objects']:
    if o['visible'] and o['objectType'] == 'Toaster':
        # pick up the Bread
        event = controller.step(action='ToggleObjectOn',
                                objectId=o['objectId'],
                                raise_for_failure=True)
        toaster_object_id = o['objectId']
        break
input("toaster on")

event = controller.step(
    action='PutObject',
    receptacleObjectId=toaster_object_id,
    objectId=breadslice_object_id,
    raise_for_failure=True)

input("bread in")
for o in event.metadata['objects']:
    if o['visible'] and o['pickupable'] and o['objectType'] == 'BreadSliced':
        # pick up the Bread
        event = controller.step(action='PickupObject',
                                objectId=o['objectId'],
                                raise_for_failure=True)
        breadslice_object_id = o['objectId']
        print("toast is",o['isCooked'])
        break
input("toast out")
