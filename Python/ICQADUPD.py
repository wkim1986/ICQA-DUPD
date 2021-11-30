from skimage.io import imread


LEVELS = 256

def hist(img):
    w = img.shape[0]
    h = img.shape[1]

    H = [0] * LEVELS
    for x in range(w):
        for y in range(h):
            v = img[x, y]
            H[v] = H[v] + 1
            
    return H

def pdf(img):
    w = img.shape[0]
    h = img.shape[1]
    N = w * h
    return list(map(lambda h: h / N, hist(img)))


# ICQA-DUPD
# Image Contrast Quality Assessment based on the Degree of Uniformity in Probability Distribution
def _ICQADUPD(pdf, depth=0, _range=(0,256), alpha=1):
    # I = index, S = sum, R = ratio,
    # _S = start, _M = median, _E = end, _L = left, _R = right
    
    I_S = _range[0]
    I_M = _range[0] + ((_range[1] - _range[0]) // 2)
    I_E = _range[1]
    
    S_L = S_R = 0
    for i in range(I_S, I_M):
        S_L += pdf[i]
    for i in range(I_M, I_E):
        S_R += pdf[i]
        
    if S_L + S_R == 0:
        return 0
        
    S = S_L + S_R
    R_L = S_L / S
    R_R = S_R / S
    
    if R_L < R_R:
        value = R_L
    else:
        value = R_R
        
    coef = 0.5 ** depth
    
    score = 0
    if (depth != 8):
        score += _ICQADUPD(pdf, depth + 1, (I_S, I_M), R_L * alpha)
        score += _ICQADUPD(pdf, depth + 1, (I_M, I_E), R_R * alpha)
        
    score += coef * alpha * value
    
    if depth == 0:
        score += 0.00390625
        
    return score

def ICQADUPD(filepath):
    img = imread(filepath)
    return _ICQADUPD(pdf(img))


if __name__ == "__main__":
    result = ICQADUPD('../AVE256.jpg')
    print(f'ICQA-DUPD: {result}\n')
    