import numpy as np
import cv2
import matplotlib.pyplot as plt

from service.ProfileProjection import crop
from service.Preprocessing import bordering_image

# new_model = tf.keras.models.load_model('ClassificationModel/nomorktp')
new_model = cv2.ml.KNearest_create()
isInitiate = 0


def initiate():
    with np.load('ClassificationModel/KNN/knn_data.npz') as data:
        train = data['train']
        train_labels = data['train_labels']
        new_model.train(train, cv2.ml.ROW_SAMPLE, train_labels)
    isInitiate = 1


def do_classification(data):
    if isInitiate == 0:
        initiate()

    gambar = data.copy()
    crop_gambar = crop(gambar, 1)

    using_data = []
    fig, axes = plt.subplots(1, 4, figsize=(8, 4), sharex=True, sharey=True)
    ax = axes.ravel()

    classification_image = cv2.resize(doFilling(crop_gambar), (40, 50), interpolation=cv2.INTER_AREA)
    classification_image_temp = bordering_image(classification_image)

    ax[1].imshow(doFilling(data), cmap=plt.cm.gray)
    ax[1].set_title('with filling')
    ax[1].axis('off')

    ax[3].imshow(classification_image, cmap=plt.cm.gray)
    ax[3].set_title('class image')
    ax[3].axis('off')

    ax[2].imshow(data, cmap=plt.cm.gray)
    ax[2].set_title('before filling')
    ax[2].axis('off')

    ax[0].imshow(classification_image_temp, cmap=plt.cm.gray)
    ax[0].set_title('skeletonize')
    ax[0].axis('off')

    fig.tight_layout()
    plt.show()

    using_data.append(classification_image_temp.flatten())
    new_data = np.array(using_data, dtype=np.float32)
    # tf.keras.utils.normalize(new_data, axis=0)

    # predictions = new_model.predict(new_data)
    # return np.argmax(predictions)
    ret, result, neighbours, dist = new_model.findNearest(new_data, k=1)

    return result


def doFilling(image):
    # image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)))
    # return image