#binary mask for MRI convertion

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

def convert_TIF_to_JPG(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".tif"):
                frame1 = plt.gca()
                frame1.axes.xaxis.set_ticklabels([])
                frame1.axes.yaxis.set_ticklabels([])
                plt.imshow(mpimg.imread(input_dir + file))
                fig1 = plt.gcf()
                #plt.show()
                plt.draw()
                fig1.savefig(output_dir+file+'.jpg')
        else:
            pass

dir1=('/home/alex/Рабочий стол/mask/')
dir2=('/home/alex/Рабочий стол/tif/')

convert_TIF_to_JPG(dir1,dir2)