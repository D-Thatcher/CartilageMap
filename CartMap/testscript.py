import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import CartMapUI
from PyQt4 import QtCore, QtGui
import sys
import nibabel as nib
import numpy as np


struct_path = r"\str.nii.gz"
cart_path = r"\cart.nii.gz"
t2_path = r"\t2.nii.gz"
s = nib.load(struct_path)
c = nib.load(cart_path)
t = nib.load(t2_path)
s_data = s.get_fdata()
s_data = ((s_data - s_data.min()) / (s_data.ptp() / 255)).astype(np.uint8)
c_data = c.get_fdata()
h = np.where(c_data != 0)
t_data = t.get_fdata()
t2cart = t_data * c_data
t2cart_masked = np.ma.masked_equal(t2cart, 0)
structure_image = s_data[0,:,:]
cart_image = t2cart_masked[0, :, :]