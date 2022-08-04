# %%
from threading import Thread
import base

# %%
if __name__ == "__main__":
    for th in range(4):
        Thread(target=base.main, args=([th])).start()