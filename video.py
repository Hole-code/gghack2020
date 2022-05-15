import imageio

images = []
filenames = []
for i in range(0,173):
	filenames.append(r"r"+str(i)+".jpg")
for filename in filenames:
	print(filename)
	images.append(imageio.imread(filename))
imageio.mimsave('movie.gif', images)