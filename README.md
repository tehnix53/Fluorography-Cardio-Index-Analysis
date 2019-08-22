# Dataset_Preparation

1) A script for preparing a dataset for binary classification from the X-rayOffice software database used on low-dose fluorographs of FMC-NPO Vzglyad Orel. The source files are stored on the workstation in the VXR_KADR directory. The database files are located in the VXR_BASE directory. For the script to work, you need to create two .XLSX files from the database files with the .DB extension with a list of study numbers and description tags 1 or 2, corresponding to the "Normal" or "Pathology" class. At the output, the script gives three directories TRAIN, VAL, TEST with files marked up into two types of PNG classes (converted from DICOM), which can be used to train CNN through datagen.flow_from_directory.

2) Conversion of binary masks (from a competition to recognize signs of multiple sclerosis on an MRI of the brain) into graphic files.
