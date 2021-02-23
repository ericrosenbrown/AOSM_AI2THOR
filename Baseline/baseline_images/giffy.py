import imageio
import sys
import os

fname = sys.argv[1]

path, dirs, files = next(os.walk("./"+fname))
file_count = len(files)
print(files)
print(file_count)

images = []
filenames = [fname+"/"+str(i)+".png" for i in range(0,file_count)]
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave(fname+".gif", images,duration=0.5)
