import imageio
import sys
import os

fname = sys.argv[1]
img_type = sys.argv[2]

fpath = fname+"/"+img_type

path, dirs, files = next(os.walk("./"+fpath))
file_count = len(files)
print(files)
print(file_count)

images = []
filenames = [fpath+"/"+str(i)+".png" for i in range(0,file_count)]
print(fname+"/"+img_type+"/"+str(0)+".png")
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave(fname+"_"+img_type+".gif", images,duration=0.5)
