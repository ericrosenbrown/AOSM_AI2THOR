from ai2thor.controller import Controller
controller = Controller(scene='FloorPlan22', gridSize=0.25,width=500,height=500)

save_images = False
fname = "CookEgg_600"

if save_images:
    import pickle
    imgs = []

input("move ahead")
event = controller.step(action='RotateLeft')
input("rotate right")

if save_images:
    imgs.append(event.frame)
    pickle.dump(imgs,open(fname+".p","wb"))



for o in event.metadata['objects']:
    if o['visible'] and o['pickupable'] and o['objectType'] == 'Pan':
        # pick up the knife
        event = controller.step(action='PickupObject',
                                objectId=o['objectId'],
                                raise_for_failure=True)
        pan_object_id = o['objectId']
        break

if save_images:
    imgs.append(event.frame)
    pickle.dump(imgs,open(fname+".p","wb"))

input("rotate right")
event = controller.step(action='MoveAhead', moveMagnitude=0.25 * 1)
event = controller.step(action='RotateRight')
event = controller.step(action='MoveAhead', moveMagnitude=0.25 * 1)
event = controller.step(action='LookDown')
input("rotate right")

# turn stove on and put pan one
if save_images:
    imgs.append(event.frame)
    pickle.dump(imgs,open(fname+".p","wb"))


for o in event.metadata['objects']:
    if o['visible'] and o['objectType'] == 'StoveBurner':
        stove_object_id = o['objectId']
        event = controller.step(action='PutObject',
                                receptacleObjectId=stove_object_id,
                                objectId=pan_object_id)
        input("put pan down")

if save_images:
    imgs.append(event.frame)
    pickle.dump(imgs,open(fname+".p","wb"))

for o in event.metadata['objects']:
    if o['visible'] and o['objectType'] == 'StoveKnob':
        #print(o['toggleable'])
        #print(o['isToggled'])
        stoveknob_object_id = o['objectId']
        # turn on stove
        event = controller.step(action='ToggleObjectOn',
                                objectId=o['objectId'],
                                raise_for_failure=True)
input("turn stove on")
if save_images:
    imgs.append(event.frame)
    pickle.dump(imgs,open(fname+".p","wb"))



event = controller.step(action='RotateRight')
input("turn stove on")
event = controller.step(action='MoveAhead', moveMagnitude=0.25 * 4)
input("turn stove on")
event = controller.step(action='RotateRight')
input("turn stove on")
if save_images:
    imgs.append(event.frame)
    pickle.dump(imgs,open(fname+".p","wb"))

for o in event.metadata['objects']:
    if o['visible'] and o['pickupable'] and o['objectType'] == 'Egg':
        # pick up the knife
        event = controller.step(action='PickupObject',
                                objectId=o['objectId'],
                                raise_for_failure=True)
        egg_object_id = o['objectId']
        break
if save_images:
    imgs.append(event.frame)
    pickle.dump(imgs,open(fname+".p","wb"))

input("turn stove on")
event = controller.step(action='RotateRight')
input("turn stove on")
event = controller.step(action='MoveAhead', moveMagnitude=0.25 * 4)
input("turn stove on")
event = controller.step(action='RotateRight')
input("turn stove on")
if save_images:
    imgs.append(event.frame)
    pickle.dump(imgs,open(fname+".p","wb"))

event = controller.step(action='PutObject',
                                receptacleObjectId=pan_object_id,
                                objectId=egg_object_id,
                                raise_for_failure=True)
if save_images:
    imgs.append(event.frame)
    pickle.dump(imgs,open(fname+".p","wb"))

input("turn stove on")
event = controller.step(action='SliceObject',
                                objectId=egg_object_id,
                                raise_for_failure=True)
input("turn stove on")
if save_images:
    imgs.append(event.frame)
    pickle.dump(imgs,open(fname+".p","wb"))

