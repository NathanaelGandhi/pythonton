# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 13:30:44 2021

@author: siris
"""
import SimpleITK as sitk
import numpy as np
import tqdm


def get_te(f):
    # 1. Read image in file 'f' and extract echo time (te) from the metadata
    # Read the DICOM series from the 4D DICOM file
    reader = sitk.ImageSeriesReader()
    dicom_series = reader.GetGDCMSeriesFileNames(f)
    reader.SetFileNames(dicom_series)
    image = reader.Execute()

    # Access the DICOM tags to extract the Echo Time (TE)
    dicom_info = image.GetMetaData("0008|0008")  # DICOM Tag for Image Type
    tags = dicom_info.split("\\")
    
    # Find the index of the TE tag in the DICOM tags
    te_index = tags.index("TE")
    
    # Extract the TE value
    te = float(tags[te_index + 1])
    
    
    return te


def mono_exponential_decay(x, a, b):
    # this function can be used as is :)
    y = a * np.exp(-b * x)
    return y


def calculate_t2map(dicom_filepaths):

    ### IM REALLY NOT SURE ABOUT THIS

    # 1. Get a list of the echo times (defined as te below) in the 4D image series
    te = []
    for slicepath in dicom_filepaths:
        te.append(get_te(slicepath))

    # 2. Read the 4D image series into a 4D Numpy array (defined as s below)
    # HINT: Use a for loop to collect 3D image arrays at each echo time
    slices = []
    dicom_image = sitk.ReadImage(dicom_filepaths)
    # Get the pixel array (image data)
    pixel_array = sitk.GetArrayFromImage(dicom_image)

    # Handle 4D (volume) image
    # You may want to specify a specific time frame if necessary
    # For example, if you want the first time frame: pixel_array[0, slice_num]
    # Here, slice_num is the slice you want to extract
    for time_idx in range(np.size(te)):
        slices.append(pixel_array[time_idx, :])


    # 3. Perform T2 fitting for each voxel
    dim = np.shape(s)  # HINT: Note the array dimensions are te, z, r, c
    t2map = np.zeros(shape=dim[1:])
    xdata = np.array(te[1:])  # ms # we will ignore the first echo in the fit
    start_T2 = np.mean(te)  # ms
    # For each image slice,
    for sl in tqdm(range(dim[1]), desc='Calculating T2 map...'):
        t2_slice = np.zeros(dim[2] * dim[3])
        s_z = np.zeros(shape=(dim[0], dim[2] * dim[3]))
        for k in range(dim[0]):
            s_z[k, :] = np.reshape(s[k, sl, :, :], (1, dim[2] * dim[3]))

        for n in range(dim[2] * dim[3]):
            ydata = np.array(s_z[1:, n])
            if ydata[0] != 0:
                try:
                    p0_init = [np.max(ydata), 1/start_T2]
                    
                    # Perform fitting of the signal intensities in the voxel
                    # HINT: Use scipy.optimize.curve_fit to fit ydata to the mono-exponential decay function
                    # and extract fitted parameter 'b'. Calculate the T2 value from 'b' and assign to
                    # the t2map array
                    
                    
                except RuntimeError:
                    pass
        out = np.reshape(t2_slice, (dim[2], dim[3]))
        t2map[sl, :, :] = out

    return t2map


def show_maps(ref_img, ref_img_title, calc_img, calc_img_title):
    # 1. Create subplots to show the two T2 maps next to each other
    # HINT: Make sure you specify a reasonable intensity range


    # 2. Create a single colorbar with reasonable range of T2 values

    # 3. Show the figure and save it
