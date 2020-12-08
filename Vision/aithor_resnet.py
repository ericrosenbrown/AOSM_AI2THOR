import torch
import pickle
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
#model = torch.hub.load('pytorch/vision:v0.6.0', 'resnet18', pretrained=True)
# or any of these variants
# model = torch.hub.load('pytorch/vision:v0.6.0', 'resnet34', pretrained=True)
model = torch.hub.load('pytorch/vision:v0.6.0', 'resnet50', pretrained=True)
# model = torch.hub.load('pytorch/vision:v0.6.0', 'resnet101', pretrained=True)
# model = torch.hub.load('pytorch/vision:v0.6.0', 'resnet152', pretrained=True)
model.eval()

lw_model = torch.nn.Sequential(*list(model.children())[:-2])
#lw_model = torch.nn.Sequential(*list(model.children())[:-1])

lw_model.eval()

# Download an example image from the pytorch website
imgs = pickle.load(open("CookEgg_2.p","rb"))

# sample execution (requires torchvision)
from PIL import Image
from torchvision import transforms

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

image_input_tensor = [Image.fromarray(new_img) for new_img in imgs]
input_tensor = [preprocess(new_img) for new_img in image_input_tensor]
input_batch = torch.stack(input_tensor)# create a mini-batch as expected by the model

num = 0
for iit in image_input_tensor:
    iit.save('egg_'+str(num)+'.png')
    num+=1
######image_input_tensor[0].show()

# move the input and model to GPU for speed if available
if torch.cuda.is_available():
    input_batch = input_batch.to('cuda')
    model.to('cuda')
    lw_model.to('cuda')

with torch.no_grad():
    almost_output = lw_model(input_batch)
    #if you use second to last layer [-1]
    #almost_output = almost_output.squeeze(-1).squeeze(-1)
    #if you use third to last layer [-2]
    almost_output = almost_output.reshape(10,100352)
    output = model(input_batch)

# Tensor of shape 1000, with confidence scores over Imagenet's 1000 classes
#print(output[0])
# The output has unnormalized scores. To get probabilities, you can run a softmax on it.
#print(torch.nn.functional.softmax(output[0], dim=0))
looking_at = 0
predicted_k_indexes = torch.topk(output[looking_at],k=10)
prk_0 = predicted_k_indexes[0]
prk_1 = predicted_k_indexes[1]
for f,s in zip(prk_0,prk_1):
    print(f,s)


pca = PCA(n_components=2)
pca.fit(almost_output)

print(pca.explained_variance_ratio_)

X_pca = pca.transform(almost_output)
categories = [0,0,1,1,1,2,2,1,1,1]
colormap = np.array(["r","g","b"])
plt.scatter(X_pca[:,0],X_pca[:,1],c=colormap[categories])
plt.show()
