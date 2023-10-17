import numpy as np
import io
import base64
import pydicom
import cv2
import matplotlib.pyplot as plt


class Dicom_pred:
    def __init__(self, dicom_file):
        dicom_file = dicom_file.open("r")
        self.ds = pydicom.dcmread(dicom_file, force=True)

    @staticmethod
    def make_rgb(img):
        if len(img.shape) == 3:
            return img
        img3 = np.empty(img.shape + (3,))
        img3[:, :, :] = img[:, :, np.newaxis]
        return img3    

    def pred_ultrasound(self):
        arr = self.ds.pixel_array[120:730, 70:950] / 255
        print(arr.shape)
        dst = cv2.resize(arr, (224, 224))
        if dst.shape == (224, 224):
            img = self.make_rgb(dst)

            dicom_img = plt.imshow(img)
            #fig = dicom_img.get_figure()
            #plot_file = io.BytesIO()
            #fig.savefig(plot_file)
            #pabd_base_64 = base64.b64encode(plot_file.getvalue()).decode()
            okmessage = "Good_Image"


            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            graphic = base64.b64encode(image_png)
            graphic = graphic.decode('utf-8')
            return (graphic, okmessage)
        else:
            okmessage = "bad_Image"
            return (dicom_img, okmessage)
