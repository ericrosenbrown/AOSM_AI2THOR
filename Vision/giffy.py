import imageio
images = []
filenames = ["egg_"+str(i)+".png" for i in range(10,15)]
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('giff2.gif', images,duration=1)
