import numpy as np
from scipy.signal import convolve2d

def h_gradient(img):
    kernel = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])
    return convolve2d(img, kernel, mode='same')  # pad to same size

def v_gradient(img):
    kernel = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ])
    return convolve2d(img, kernel, mode='same')  # pad to same size

def compute_energy(img, mode='L1'):
    if mode == 'L1':
        return np.abs(h_gradient(img)) + np.abs(v_gradient(img))
    elif mode == 'HoG':
        pass
    
def rgb2gray(img):
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    return (0.2989 * r + 0.5870 * g + 0.1140 * b).astype(np.uint8)

def seam_carve(color_img):

    I = rgb2gray(color_img)  # convert color image to grayscale (h * w)

    h, w = I.shape

    E = compute_energy(I)  # compute pixel energy (h * w)
    M = np.copy(E)  # compute cumulative energy (vertical) (h * w)
    B = np.zeros_like(M)  # backtrack path

    # Start DP

    for i in range(1, h):  # base case is M(0, j)
        for j in range(w):
            p1 = M[i-1, j-1] if j > 0 else np.inf
            p2 = M[i-1, j]
            p3 = M[i-1, j+1] if j+1 < w else np.inf

            e = {p1 : -1, p2: 0, p3: 1}
            p = min(e.keys())

            M[i, j] += p  # add pixel energy from previous row
            B[i, j] = e[p]

    end_idx = np.argmin(M[-1, :])  # minimum index of last row. Backtrack from (h-1, end_idx)

    j = end_idx
    for i in range(h - 1, -1, -1):
        color_img[i, j:-1, :] = color_img[i, j+1:, :]  # remove pixel at (i, j)
        #color_img[i, j, :] = 255
        j += B[i, j]
    
    return color_img[:, :-1, :]