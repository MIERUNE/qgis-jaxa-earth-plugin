# ----------------------------------------------------------------------------------------
# Load module
# ----------------------------------------------------------------------------------------
import numpy as np


# ----------------------------------------------------------------------------------------
# apply_palette
# ----------------------------------------------------------------------------------------
def apply_palette(img_in, color_map_in):
    # Change dimension (3d to 2d)
    img_tmp = img_in.reshape(img_in.shape[0:2]).astype(np.uint8)

    # If colormap is 16bit, reduce it to 8 bit
    if max(color_map_in) > 255:
        color_map = [i >> 8 for i in color_map_in]
    else:
        color_map = list(color_map_in)

    # Build 256-entry RGB LUT (pad with zeros, matching PIL putpalette behavior)
    palette = np.zeros((256, 3), dtype=np.uint8)
    flat = np.asarray(color_map, dtype=np.uint8)
    n = min(flat.size, palette.size)
    palette.reshape(-1)[:n] = flat[:n]

    # Apply LUT
    img_out3 = palette[img_tmp]

    # Add alpha channel
    alpha = np.zeros(img_out3.shape[0:2], dtype=np.uint8)
    alpha[np.sum(img_out3, axis=2) > 0] = 255
    img_out = np.dstack([img_out3, alpha])

    # Output
    return img_out


# ----------------------------------------------------------------------------------------
# conv_cmap
# ----------------------------------------------------------------------------------------
def conv_cmap(cmap_in):
    cmap_out = list(np.array(cmap_in).reshape([3, -1]).T.flatten())
    return cmap_out
