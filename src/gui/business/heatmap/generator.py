import numpy as np
import cv2

def new_canvas(height, width) -> np.ndarray:
    """
    new_canvas creates and returns a two-dimensional numpy array filled with zeroes.
    """
    return np.zeros((height, width), dtype=np.float32)

def add_presence(canvas: np.ndarray, x1, y1, x2, y2):
    """
    add_presence takes a canvas and a rectangle as input and adds a constant value to every unit comprising the rectangle as presence.
    """
    height, width = canvas.shape

    # avoid going off-grid, it may not occur in practice though
    x1 = int(max(0, x1))
    y1 = int(max(0, y1))
    x2 = int(min(width, x2))
    y2 = int(min(height, y2))
    # verify valid rectangle, it may not occur in practice though
    if x2 > x1 and y2 > y1:
        canvas[y1:y2, x1:x2] += 1

def normalize_canvas(canvas: np.ndarray):
    """
    normalize_canvas normalizes values from [0, canvas.max()] to [0, 1], includes a minimum intensity threshold.
    """
    if canvas.max() == 0:
        return

    # ignore the 10% higher values as if they were abnormal results
    percentile = np.percentile(canvas, 90.0)
    # if ignoring the 10% higher values leaves us with zeroes, use the actual maximum (to avoid division by zero)
    if percentile == 0:
        canvas /= canvas.max()
    else:
        canvas /= percentile
    np.power(canvas, 0.6, out=canvas)
    # dividing by percentile may leave values bigger than 1
    np.clip(canvas, 0, 1, out=canvas)

    # every value bigger than 0 gets established as the maximum between itself or 0.1
    threshold = canvas > 0
    canvas[threshold] = np.maximum(canvas[threshold], 0.1)

def create_rgba_layer(canvas: np.ndarray, bgr_color) -> np.ndarray:
    """
    create_rgba_layer takes a canvas a returns an rgba colored image.
    """
    h, w = canvas.shape
    layer = np.zeros((h, w, 4), dtype=np.uint8)
    
    mask = canvas > 0
    # if there's no presence on the canvas
    if not mask.any():
        return layer

    # add color to layer
    for i, channel in enumerate(bgr_color):  # i=0: B, i=1: G, i=2: R
        layer[mask, i] = (channel * canvas[mask]).astype(np.uint8)

    # add alpha to layer
    alpha = 0.8 * canvas
    layer[:, :, 3] = (alpha * 255).astype(np.uint8)

    return layer

def add_gaussian_blur(layer: np.ndarray, kernel_size: tuple[int, int] = (49, 49), sigma = 8):
    """
    add_gaussian_blur applies Gaussian blur to the given heatmap layer to make it look nicer.
    """
    # add blur to rgb channels
    for c in range(3):
        layer[:, :, c] = cv2.GaussianBlur(layer[:, :, c], kernel_size, sigma)
    
    # add blur to alpha channels
    if layer.shape[2] == 4:
        layer[:, :, 3] = cv2.GaussianBlur(layer[:, :, 3], kernel_size, sigma)


def create_heatmap(heatmap_layers: dict[str, np.ndarray]) -> np.ndarray:
    """
    create_heatmap takes rgba heatmap layers as input and returns a colored image resulting from merging the layers.
    """
    h, w = list(heatmap_layers.values())[0].shape[:2]
    heatmap = np.zeros((h, w, 4), dtype=np.uint8)
        
    # merge all layers
    for layer_name, layer in heatmap_layers.items():
        # alpha blending
        # Author: an LLM
        alpha = layer[:, :, 3:4].astype(np.float32) / 255.0
        for c in range(3):
            heatmap[:, :, c] = np.where(
                alpha[:, :, 0] > 0,
                layer[:, :, c] * alpha[:, :, 0] + \
                heatmap[:, :, c] * (1 - alpha[:, :, 0]),
                heatmap[:, :, c]
            ).astype(np.uint8)
        heatmap[:, :, 3] = np.maximum(
            heatmap[:, :, 3], 
            layer[:, :, 3]
        )
    
    return heatmap

def resize_heatmap(heatmap: np.ndarray) -> np.ndarray:
    """
    resize_heatmap resizes a given heatmap to a 800x600 resolution.
    """
    return cv2.resize(heatmap, (800, 600), interpolation=cv2.INTER_LINEAR)
