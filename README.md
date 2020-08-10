# CartilageMap
MR image viewer capable of overlaying anatomical maps

This project can be used as a quality assurance measure for clinicians to determine the precision and accuracy of anatomical mappings. In this example, this viewer is being used to assess a knee cartilage mapping.<br>

The viewer requires three compressed Nifty(.nii.gz) files to produce the map: An MRI sequence file (such as a T2), a structural image, and the anatomical map.<br>

The core operation is the overlaying of the product of the T2 image with the anatomical map onto the structural image. The product is colour mapped by pixel intensity prior to being overlaid for distinction.<br>

Project dependencies include: PyQt4, Matplotlib, Numpy, and OpenCV.

To install PyQt4, download the wheel at https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4  Now, using pip, run `pip install "PyQt4-4.11.4-cp36-cp##m-win_amd##.whl"` Where cp## refers to Python version ##.<br>

The remaining libraries can be installed using `pip install numpy matplotlib opencv-python`<br>

Run the `CartilageMap.py` file and a user-interface will open<br>


![alt text](https://github.com/D-Thatcher/CartilageMap/blob/master/assets/1.PNG)


Add your structural, anatomical map, and T2 image files and select Load.


![alt text](https://github.com/D-Thatcher/CartilageMap/blob/master/assets/3.PNG)


The image will load to its true size. You can zoom in or out using the +/- buttons in the top-left corner. And, you can scroll through the slices by first selecting a view, then moving the axis bar.


![alt text](https://github.com/D-Thatcher/CartilageMap/blob/master/assets/4.PNG)


Once your map is reached, you'll notice it will be mapped to a red colour scale.


![alt text](https://github.com/D-Thatcher/CartilageMap/blob/master/assets/5.PNG)


Select the cartilage distribution button to load a histogram of the map's pixel intensity for non-zero regions.


![alt text](https://github.com/D-Thatcher/CartilageMap/blob/master/assets/7.PNG)


Here is a view from another axial direction, with its corresponding distribution.


![alt text](https://github.com/D-Thatcher/CartilageMap/blob/master/assets/8.PNG)


Finally, it can be useful to open multiple anatomical maps at the same time. Since each overlaid map is the product of the T2 image and the anatomical map, you will need to `Add` one new T2 image for every new anatomical map.<br>
Although, it is also possible to reuse the T2 image, you will still need to add it, even if it is the same path. Note that this doesn't require any extra memory, as it is only the product and the structural image that is stored.


![alt text](https://github.com/D-Thatcher/CartilageMap/blob/master/assets/9.png)

