import SimpleITK as sitk

###############################################################################
def image_from_series(dicom_dir):

    print("Reading Dicom directory:", dicom_dir)
    reader = sitk.ImageSeriesReader()

    dicom_names = reader.GetGDCMSeriesFileNames(dicom_dir)
    reader.SetFileNames(dicom_names)

    image = reader.Execute()

    size = image.GetSize()
    print("Image size:", size[0], size[1], size[2])

    return image
###############################################################################
