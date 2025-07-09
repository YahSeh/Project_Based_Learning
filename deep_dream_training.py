import numpy as np
from functools import partial
from PIL import Image
import tensorflow as tf
import urllib.request
import os
import zipfile
import matplotlib.pyplot as plt
import pathlib, shutil

tf.compat.v1.disable_eager_execution()

# ---------- helper utilities ----------
def resize(img, size):
    return np.float32(
        Image.fromarray(np.uint8(img)).resize(size[::-1], Image.LANCZOS)
    )

def showarray(a):
    a = np.clip(a, 0, 255).astype(np.uint8)
    plt.figure(figsize=(8, 8))
    plt.axis('off')
    plt.imshow(a)
    plt.show()

def calc_grad_tiled(img, grad_t, tile=512):
    h, w = img.shape[:2]
    sx = np.random.randint(tile)
    sy = np.random.randint(tile)
    img_shift = np.roll(np.roll(img, sx, 1), sy, 0)
    grad = np.zeros_like(img)
    for y in range(0, max(h - tile // 2, tile), tile):
        for x in range(0, max(w - tile // 2, tile), tile):
            sub = img_shift[y:y + tile, x:x + tile]
            g = sess.run(grad_t, {t_input: sub})
            grad[y:y + tile, x:x + tile] = g
    return np.roll(np.roll(grad, -sx, 1), -sy, 0)

# ---------- main ----------
def main():
    global sess, t_input

    # 1 – download Google’s pretrained network (Inception-5h)
    url = 'https://storage.googleapis.com/download.tensorflow.org/models/inception5h.zip'
    data_dir = './data'
    os.makedirs(data_dir, exist_ok=True)
    zip_path = os.path.join(data_dir, os.path.basename(url))
    if not os.path.exists(zip_path):
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(data_dir)

    model_fn = 'tensorflow_inception_graph.pb'

    # 2 – build TF graph
    graph = tf.Graph()
    with graph.as_default():
        sess = tf.compat.v1.InteractiveSession()
        with tf.io.gfile.GFile(os.path.join(data_dir, model_fn), 'rb') as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())

        t_input = tf.compat.v1.placeholder(np.float32, name='input')
        imagenet_mean = 117.0
        t_preprocessed = tf.expand_dims(t_input - imagenet_mean, 0)
        tf.import_graph_def(graph_def, {'input': t_preprocessed})

    # 3 – pick a layer/channel
    layer = 'mixed4d_3x3_bottleneck_pre_relu'
    channel = 139
    t_layer = graph.get_tensor_by_name(f'import/{layer}:0')

    # 4 – deep-dream function
    def render_deepdream(
            img0,
            t_obj=t_layer[..., channel],
            n_iter=10, step=1.5,
            n_octave=4, octave_scale=1.4):

        with graph.as_default():
            t_score = tf.reduce_mean(t_obj)
            t_grad = tf.gradients(t_score, t_input)[0]

        # split image into octaves
        img = img0.copy()
        octaves = []
        for _ in range(n_octave - 1):
            hw = img.shape[:2]
            lo = resize(img, np.int32(np.float32(hw) / octave_scale))
            hi = img - resize(lo, hw)
            img = lo
            octaves.append(hi)

        # iterate over octaves
        for octave in range(n_octave):
            if octave > 0:
                hi = octaves[-octave]
                img = resize(img, hi.shape[:2]) + hi
            for _ in range(n_iter):
                g = calc_grad_tiled(img, t_grad)
                img += g * (step / (np.abs(g).mean() + 1e-7))
            showarray(img)

    # 5 – prompt user for an image URL
    img_url = input(
        "Enter an image URL "
        "(e.g., https://upload.wikimedia.org/wikipedia/commons/3/33/Pilatus1.jpg): "
    ).strip()

    try:
        image_path = 'input.jpg'
        with urllib.request.urlopen(img_url) as r, open(image_path, 'wb') as f:
            shutil.copyfileobj(r, f)
        img0 = np.float32(Image.open(image_path))
    except Exception as e:
        print(f"Failed to load image from URL: {e}")
        return

    # 6 – run DeepDream
    render_deepdream(img0)

if __name__ == '__main__':
    main()