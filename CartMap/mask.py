import matplotlib.pyplot as plt
import matplotlib
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

# Define paths to files
structniifile = r"C:\Users\Dan\Desktop\NIFTY_READ\Test\str.nii.gz"
#t2niifile     = r"C:\Users\Dan\Desktop\NIFTY_READ\Test\t2.nii.gz"
#cartniifile   = r"C:\Users\Dan\Desktop\NIFTY_READ\Test\cart.nii.gz"
t2niifile     = r"C:\Users\Dan\Desktop\NIFTY_READ\OtherTest\other_t2.nii.gz"
cartniifile   = r"C:\Users\Dan\Desktop\NIFTY_READ\OtherTest\other_cart.nii.gz"

# Load images
structnii = nib.load(structniifile)
cartnii   = nib.load(cartniifile)
t2nii     = nib.load(t2niifile)

# Access 3D image data
structdata = structnii.get_data()
cartdata = cartnii.get_data()
t2data = t2nii.get_data()


# Create a matrix with T2 values where
# cartmask equals 1, zero values outside cartilage
t2cart = t2data * cartdata

# Slice you want to visualize
sl = 250

# Convert T2 cartilage data array into masked array
# so that zero-value voxels are transparent when visualized
t2cart_masked = np.ma.masked_equal(t2cart,0)

# Create matplotlib figure
f,ax = plt.subplots()


# Add structural 2D image to figure
#ax.matshow(structdata[:,240,:])
#ax.matshow(t2cart_masked[:,240,:],cmap='cool')
a = t2cart[:,250,:]
a = np.nan_to_num(a)
wh = np.where(a != 0)
k,l = wh
box= []

for i,j in zip(k,l):
    box.append(a[i,j])

l = np.array(box)
plt.hist(box,bins = 'auto')
plt.show()
# Add cartilage mask overlay




# Draw plot
#plt.show()