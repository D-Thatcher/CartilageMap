import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import CartMapUI
from PyQt4 import QtCore, QtGui
import sys
import nibabel as nib
import numpy as np
import cv2
import matplotlib.pyplot as plt


# If you make changes to the GUI with a program like QT Designer,
# replace 'self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)'
# with 'self.scrollArea.setWidget(self.label)' after converting the .ui file to .py

#Assumes the cart map and the structural image data are correctly lined up
class CartMap(QtGui.QMainWindow, CartMapUI.Ui_MainWindow):

    def __init__(self):
        #Standard method calls
        super(self.__class__, self).__init__()
        self.setupUi(self)

        #onclick
        self.loadButton.clicked.connect(lambda: self.set_label())
        self.addStructFile.clicked.connect(lambda: self.add_struct_path())
        self.addCartFile.clicked.connect(lambda: self.add_cart_path())
        self.addT2File.clicked.connect(lambda: self.add_t2_path())
        self.cartDistribution.clicked.connect(lambda: self.show_distribution())

        self.viewOne.clicked.connect(lambda: self.change_view(1))
        self.viewTwo.clicked.connect(lambda: self.change_view(2))
        self.viewThree.clicked.connect(lambda: self.change_view(3))
        self.zoomIn.clicked.connect(lambda: self.zoom_in(True))
        self.zoomOut.clicked.connect(lambda: self.zoom_in(False))
        self._load_bar(self.axis1)
        self._load_bar(self.axis2)
        self._load_bar(self.axis3)


        #member variables
        self.struct_path = ""
        self.cart_paths = []
        self.t2_paths = []

        self.change_view(1)
        self.axis1.setEnabled(False)
        [v.setEnabled(False) for v in [self.viewOne, self.viewTwo, self.viewThree]]
        self.label.setStyleSheet("background-color:#000000;")

        self.histogram = []

        self.axis1_loc = 0
        self.axis2_loc = 0
        self.axis3_loc = 0
        self.zoom_factor = 1

        self.t2cart = None
        self.s_shape = None

        self.s_data = None
        self.t2cart_masked = None


    def zoom_in(self,expand):
        if expand:
            self.zoom_factor = self.clamp(self.zoom_factor + 0.2, 0.2, 10)
        else:
            self.zoom_factor = self.clamp(self.zoom_factor - 0.2, 0.2, 10)
        self.__update_image_location()


    # Adds weight to, removes weight from, enables, and disables UI elements
    def update_view(self):
        all_buttons = (self.viewOne,self.viewTwo,self.viewThree)
        all_labels_2 = (self.label_11, self.label_12, self.label_13)
        view_label_2 = all_labels_2[self.view_axis-1]
        view_button = all_buttons[self.view_axis-1]
        all_stuff = all_buttons + all_labels_2
        for stuff in all_stuff:
            boo = (stuff == view_button or stuff == view_label_2)
            curr_font = stuff.font()
            curr_font.setBold(boo)
            stuff.setFont(curr_font)
        all_axis = (self.axis1,self.axis2,self.axis3)
        view_axis = all_axis[self.view_axis - 1]
        for x in all_axis:
            x.setEnabled(x == view_axis)

    def change_view(self,n):
        self.view_axis = n
        self.update_view()

    def _load_bar(self,bar):
        bar.setMinimum(0)
        bar.setMaximum(10)
        bar.setValue(0)
        bar.setTickPosition(0)
        bar.setTickInterval(1)
        bar.valueChanged.connect(lambda: self.update_bars(True,True))

    def update_bar_max(self,max_val,bar):
        bar.setMaximum(max_val-1)

    def __update_image_location(self):
        im = self.get_ith_view_image()
        bar_max = self.s_data.shape[self.view_axis - 1]
        h,w,chan = im.shape
        axis_to_update = (self.axis1,self.axis2,self.axis3)[self.view_axis - 1]
        self.update_bar_max(bar_max,axis_to_update)
        base_photo = QtGui.QImage(im, w, h, QtGui.QImage.Format_RGB888)
        hold_created = QtGui.QPixmap(base_photo)
        self.label.setPixmap(hold_created)

    def update_static_location(self):
        self.currentAxis1.setText(str(self.axis1_loc))
        self.currentAxis2.setText(str(self.axis2_loc))
        self.currentAxis3.setText(str(self.axis3_loc))


    def update_bars(self,update_params,update_other):
        if update_params:
            self.axis1_loc = int(float(self.axis1.value()))
            self.axis2_loc = int(float(self.axis2.value()))
            self.axis3_loc = int(float(self.axis3.value()))
            self.update_static_location()
            self.__update_image_location()
        else:
            self.axis1.setValue(self.axis1_loc)
            self.axis2.setValue(self.axis2_loc)
            self.axis3.setValue(self.axis3_loc)
            self.update_static_location()
            if update_other: self.update_edit(False,False)

    def clamp(self, n, minn, maxn):
        if n < minn:
            return minn
        elif n > maxn:
            return maxn
        else:
            return n

    def reset_paths(self):
        self.struct_path = ""
        self.cart_path = ""
        self.t2_path = ""
        self.t2Combo.clear()
        self.cartCombo.clear()
        self.structEdit.setText(self.struct_path)

    def add_struct_path(self):
        self.struct_path = str(self.open_dialog("Select a Structural Image"))
        self.structEdit.setText(self.struct_path)

    def add_cart_path(self):
        to_add = str(self.open_dialog("Select a Cartilage Map Image"))
        self.cartCombo.addItem(to_add)
        if to_add:
            self.cart_paths.append(to_add)

    def add_t2_path(self):
        to_add = str(self.open_dialog("Select a T2 Image"))
        self.t2Combo.addItem(to_add)
        if to_add:
            self.t2_paths.append(to_add)

    def set_label(self):
        len_c = len(self.cart_paths)
        len_t = len(self.t2_paths)
        if self.struct_path and len_c > 0 and len_t > 0:

            s = nib.load(self.struct_path)
            try:
                self.s_data = s.get_fdata()
            except MemoryError:
                msg = QtGui.QMessageBox()
                msg.setText("Accessible memory was exhausted.")
                msg.show()
            self.s_data = ((self.s_data - self.s_data.min()) / (self.s_data.ptp() / 255)).astype(
                np.uint8)
            self.s_shape = self.s_data.shape

            c = nib.load(self.cart_paths[0])
            t = nib.load(self.t2_paths[0])

            try:
                self.t2cart = t.get_fdata() * c.get_fdata()
            except MemoryError:
                msg = QtGui.QMessageBox()
                msg.setText("Accessible memory was exhausted.")
                msg.show()
                
            self.t2cart = np.nan_to_num(self.t2cart)

            if len_c > 1 and len_t > 1:

                for cart_path, t2_path in zip(self.cart_paths[1:],self.t2_paths[1:]):
                    c = nib.load(cart_path)
                    t = nib.load(t2_path)
                    try:
                        self.t2cart = self.t2cart + t.get_fdata()*c.get_fdata()
                    except MemoryError:
                        msg = QtGui.QMessageBox()
                        msg.setText("Accessible memory was exhausted.")
                        msg.show()

            self.axis1.setEnabled(True)
            [v.setEnabled(True) for v in [self.viewOne, self.viewTwo, self.viewThree]]
            self.__update_image_location()

    def get_ith_view_image(self):
        if self.view_axis == 1:
            im = self.s_data[self.axis1_loc, :, :]
            m = self.t2cart[self.axis1_loc, :, :]
        elif self.view_axis  == 2:
            im = self.s_data[:, self.axis2_loc, :]
            m = self.t2cart[:, self.axis2_loc, :]
        else:
            im = self.s_data[:, :, self.axis3_loc]
            m = self.t2cart[:, :, self.axis3_loc]
        im = cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)

        wh = np.where(m != 0)
        m_p = self.get_red(m)

        k, r = wh
        box = []
        for w, j in zip(k, r):
            im[w, j, :] = m_p[w, j, :]
            box.append(m[w, j])
        self.histogram = box
        if self.zoom_factor != 1:
            im = cv2.resize(im, (0, 0), fx=self.zoom_factor, fy=self.zoom_factor)
        return im

    def show_distribution(self):
        num = plt.get_fignums()
        if num:
            msg = QtGui.QMessageBox(self)
            msg.setText("Close the open histogram before opening a new one")
            msg.show()
        else:
            plt.hist(self.histogram,bins = 'auto')
            plt.title("Cartilage Distribution (for non-zero regions)")
            plt.xlabel("Intensity")
            plt.ylabel("Number of Pixels")
            plt.show()


    def get_red(self,m):
        h, w = m.shape
        nd = np.ndarray((h, w, 3)).astype(np.uint8)
        m_max = m.max()
        m_min = m.min()
        MIN = 100 #Purely experimental
        MAX = 255
        #linearly map the max and min to MAX and MIN
        ratio = 1
        y_int = 0
        if m_max > m_min:
            ratio = (MAX - MIN) / float(m_max - m_min)
            y_int = MAX - ratio*m_max
            m = ratio*m + y_int
        m = m.astype(np.uint8)
        nd[:, :, 0] = m
        return nd


    def open_dialog(self, dialog_title):
        file_path = QtGui.QFileDialog.getOpenFileName(self,dialog_title)
        if file_path:
            if len(file_path) > 3 and file_path[-3:] == '.gz':
                return file_path
            else:
                self.unsupported_file_type()
                return ""
        return ""

    def unsupported_file_type(self):
        msg = QtGui.QMessageBox(self)
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText("This file type is not supported. Try a .nii.gz type file. If your file is .gz, but you know it contains image data, rename it and add .nii.gz to the end.")
        msg.setWindowTitle(":(")
        msg.show()

def main():
    app = QtGui.QApplication(sys.argv)
    form = CartMap()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
