import joblib
def prediction(data):
    model=joblib.load('model.pkl')
    ans=model.predict([data])
    return ans[0]