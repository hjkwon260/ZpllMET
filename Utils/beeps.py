from IPython.display import Audio
from IPython.core.display import display
import numpy as np

def beep():
    sr = 22050 # sample rate
    T = 0.3    # seconds
    t = np.linspace(0, T, int(T*sr), endpoint=False) # time variable
    x = 0.5*np.sin(2*np.pi*440*t) # pure sine wave at 440 Hz
    display(Audio(x, rate=sr, autoplay=True))
def beep_no():
    sr = 22050 # sample rate
    T = 0.3    # seconds
    t = np.linspace(0, T, int(T*sr), endpoint=False) # time variable
    x = 0.5*np.sin(2*np.pi*660*t)
    display(Audio(x, rate=sr, autoplay=True))    
def beep_ok():
    sr = 22050 # sample rate
    T = 0.3    # seconds
    t = np.linspace(0, T, int(T*sr), endpoint=False) # time variable
    x = 0.5*np.sin(2*np.pi*440*t)
    x1 = 0.5*np.sin(2*np.pi*300*t)
    display(Audio(x, rate=sr, autoplay=True))        
    display(Audio(x1, rate=sr, autoplay=True))  