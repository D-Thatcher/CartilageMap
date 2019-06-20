import sys
from PyQt4 import QtCore, QtGui
import nibabel as nib
import numpy as np
import cv2
from PIL import Image

# Create window
app = QtGui.QApplication(sys.argv)

# Create widget
label = QtGui.QLabel()

label.setGeometry(50, 50, 1000, 1000)




struct_path = r"\str.nii.gz"
cart_path = r"\cart.nii.gz"
t2_path = r"\t2.nii.gz"
s = nib.load(struct_path)
c = nib.load(cart_path)
t = nib.load(t2_path)
s_data = s.get_fdata()
c_data = c.get_fdata()
t_data = t.get_fdata()
t2cart = t_data * c_data

def get_red(m):
    h,w = m.shape
    nd = np.ndarray((h,w,3)).astype(np.uint8)
    nd[:,:,0] = m
    return nd

len_i,len_j,len_k = s_data.shape
i_s, j_s, k_s = np.where(t2cart != 0)
s_data = ((s_data - s_data.min()) / (s_data.ptp() / 255)).astype(np.uint8)
t2_cart = ((t2cart - t2cart.min()) / (t2cart.ptp() / 255)).astype(np.uint8)


im = s_data[:,250,:]
m = t2_cart[:, 250,:]

im = cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)
m_p = get_red(m)
m = m_p[:,:,0]
wh = np.where( m != 0)
k,l = wh

for k,l in zip(k,l):
    im[k,l,:] = 255*m_p[k,l,:]


base_photo = QtGui.QImage(im,len_k, len_i, QtGui.QImage.Format_RGB888)


hold_created = QtGui.QPixmap(base_photo)
label.setPixmap(hold_created)


# Draw window
label.show()
app.exec_()