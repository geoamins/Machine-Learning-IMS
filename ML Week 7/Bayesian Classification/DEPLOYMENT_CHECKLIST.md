# 🚀 Streamlit Cloud Deployment Checklist

## Quick Checklist

- [ ] Code is pushed to GitHub repository
- [ ] `streamlit_app.py` is in: `ML Week 7/Bayesian Classification/`
- [ ] `Book1.csv` is in: `ML Week 7/Bayesian Classification/`
- [ ] `requirements.txt` is in: `ML Week 7/Bayesian Classification/`
- [ ] All files are committed to Git

## Deployment Steps

1. **Go to:** https://share.streamlit.io/
2. **Sign in** with GitHub
3. **Click:** "New app"
4. **Select:** Your repository
5. **Select:** Branch (main/master)
6. **Main file path:** `ML Week 7/Bayesian Classification/streamlit_app.py`
7. **Click:** "Deploy!"

## Important Notes

✅ The app will automatically find `Book1.csv` in the same directory  
✅ Streamlit Cloud will install dependencies from `requirements.txt`  
✅ Changes auto-deploy when you push to GitHub  
✅ Your app URL will be: `https://your-username-streamlit-app-xxxxx.streamlit.app`

## Files Required

```
ML Week 7/Bayesian Classification/
├── streamlit_app.py      ← Main app file
├── Book1.csv             ← Data file (must be here!)
└── requirements.txt      ← Dependencies
```

## Need Help?

See `README_STREAMLIT_CLOUD.md` for detailed instructions.

