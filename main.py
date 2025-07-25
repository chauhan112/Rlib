#%%
from timeline.t2025.July.backendAPIForLocalTools.mainCode import get_app
app = get_app()
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)