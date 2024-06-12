from utilz2.core.u1_essentials import *

host_name = socket.gethostname()
home_path = os.path.expanduser("~")
#username = getpass.getuser()
username=home_path.split('/')[-1]
sleep = time.sleep
sys = os.sys
gg = glob.glob


import numpy as np

rnd = np.random.random
rndint = np.random.randint
rndn = np.random.randn
rndchoice = np.random.choice
na = np.array
degrees = np.degrees
arange = np.arange
shape = np.shape
randint = np.random.randint
randn = np.random.randn
zeros = np.zeros
ones = np.ones
reshape = np.reshape
mod = np.mod
array = np.array
sqrt = np.sqrt
sin = np.sin
cos = np.cos
std = np.std
pi = np.pi


if __name__ == '__main__':
    eg(__file__)
    print('home_path =',home_path)
    print('username =',username)
    print('host_name =',host_name)
    print()

#EOF
