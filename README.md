The repository contains scripts of the project for calculating the cardiotaracal index by fluorography.

The development of the project included the following steps:

1) preparation of my custom dataset (GE medical equipment and ЗАО НАУЧПРИБОР were used), including analysis of source databases
(image_parsing), image conversion for neural network training, fluorography contouring using labelme tools and mask conversion (utility).

2) training a neural network with Unet architecture for image segmentation. Two types of binary masks were used: for the heart and for the lungs.
The following metric parameters were obtained:
Lungs: loss: -0.9016 - dice_coef: 0.9016 - binary_accuracy: 0.9835 - val_loss: -0.8969 - val_dice_coef: 0.8969 - val_binary_accuracy: 0.9850.
Heart: loss: 0.2262 - acc: 0.9202 - val_loss: 0.1864 - val_acc: 0.9254.

3) Calculation of the сaodiotaracal index and testing on public datasets (Montgomery, Shenzen). Examples of calculations, testing, and numerical data are given in DEMO HEART PREDICT and CARDIOINDEX CALCULATION.ipynb and EXPLANATION and EXAMPLE CARDIO INDEX CALCULATION DEF.ipynb.

