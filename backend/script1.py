import pickle
from facerecog import analysis1

with open("facerecog1.pkl","wb") as f:
    # sc = inspect.getsource(analysis1)
    pickle.dump(analysis1,f)