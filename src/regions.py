from constants import X_BAULK_LINE, R_BAULK_D, screen_height

def get_region(position): 
    x, y = position
    if x > X_BAULK_LINE: # To the right of baulk line
        return 1
    elif (x - X_BAULK_LINE)**2 + (y - screen_height / 2)**2 > R_BAULK_D**2: # Outside Baulk D
        return 2
    else: # Inside Baulk D
        return 3