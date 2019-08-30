import io
import os
import base64
import logging
import tempfile
import requests
import cv2
import numpy as np
import pandas as pd
from imageio import imread
from PIL import Image
from matplotlib import pyplot as plt


logger = logging.getLogger()
represent_colors = pd.read_csv("data/represent_colors.csv")


def imread_web(url: str) -> "np.ndarray":
    res = requests.get(url)
    img = None

    with tempfile.NamedTemporaryFile(dir='./') as fp:
        fp.write(res.content)
        fp.file.seek(0)
        img = cv2.imread(fp.name)
    return img


def get_rgb_average(mat) -> list:

    plt.imshow(mat)
    plt.show()

    # averaging
    r = int(mat[:, :, 0].mean())
    g = int(mat[:, :, 1].mean())
    b = int(mat[:, :, 2].mean())

    # show average img
    plt.imshow(
       np.array([r, g, b] * 2500).reshape(50, 50, 3)
    )
    return [r, g, b]


def get_rgb_average_by_url(url: str) -> list:
    mat = cv2.imread(f"data/image/{os.path.basename(url)}")
    mat = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
    return get_rgb_average(mat)


def get_rgb_kmeans(mat, K=3, imshow=False) -> list:

    colors = mat.reshape(-1, 3)  # extract colors
    colors = colors.astype(np.float32)
    print("colors shape", colors.shape)
    criteria = cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 10, 1.0

    _, label, center = cv2.kmeans(
        colors, K, None, criteria, attempts=10, flags=cv2.KMEANS_RANDOM_CENTERS)

    _, counts = np.unique(label, axis=0, return_counts=True)

    if imshow:
        fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(10, 3))
        fig.subplots_adjust(wspace=0.5)
        bar_color = [(r / 255, g / 255, b / 255) for b, g, r in center]
        bar_text = [f"({r}, {g}, {b})" for b, g, r in center.astype(np.uint8)]
        ax1.imshow(cv2.cvtColor(mat, cv2.COLOR_BGR2RGB))
        ax1.set_axis_off()
        ax2.barh(np.arange(K), counts, color=bar_color, tick_label=bar_text)
        plt.show()

    return [[int(r), int(g), int(b)] for b, g, r in center][np.argmax(counts)]


def get_rgb_kmeans_by_url(url: str, K=3, imshow=False) -> list:

    if "?p=" in url:
        url = url[:url.find("?p=")]

    mat = cv2.imread(f"data/image/{os.path.basename(url)}")

    if mat is None:
        print(f"{os.path.basename(url)} not found!")
        return

    return get_rgb_kmeans(mat, K=K, imshow=imshow)


def search(color: list, represent_colors,
    n_result=30, show=False, **kwargs) -> list:

    """search image with RGB code"""

    assert len(color) == 3, f"invalid length of RGB value, 3 != {len(color)}"
    r, g, b = color

    A = represent_colors.iloc[:, 1:].values.astype(float)
    B = np.array([r, g, b] * len(represent_colors)).reshape(len(represent_colors), 3)

    norms = np.linalg.norm(x=(A-B), axis=1, keepdims=True)
    norms_sort = norms.argsort(axis=0)

    result_urls = \
        represent_colors.iloc[[n[0] for n in norms_sort], :]["url"].values[:n_result]

    if show:
        [get_rgb_kmeans(url, imshow=True) for url in result_urls]
    return result_urls


def _hex_to_rgb(code: str) -> list:
    # assert code is None or code == "", f"invalid input for _hex_to_rgb(): {code}"
    code = code.lstrip('#')
    print(f"input hex: {code}")
    lv = len(code)
    
    return list(int(code[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def search_by_hex(code: str, represent_colors, n_result=30, **kwargs) -> list:
    print(f"Searched: {code}")
    return search(_hex_to_rgb(code), represent_colors, n_result=n_result, **kwargs)


def decode_binary_base64(code: str) -> "np.ndarray":
    img_binary = base64.b64decode(code)
    print("loaded image binary", img_binary)
    jpg = np.frombuffer(img_binary, dtype=np.uint8)
    print("transformed to jpg", jpg)
    img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)
    print("transformed to cv2 img", img)
    return img


def binary_to_array(image_bytes: str):
    decoded = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
    npimg = np.array(decoded)
    # mat = cv2.cvtColor(npimg, cv2.COLOR_BGR2RGB)
    return npimg


if __name__ == "__main__":
    pass
