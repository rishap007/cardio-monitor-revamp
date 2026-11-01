# Cardio Monitor

A small Flask app that demonstrates a heart disease risk classifier using the included `heart.csv` dataset. The prediction is an educational demonstration, not a medical diagnosis.

## Run locally (macOS/Linux)

From this folder, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python modelbuild.py
python app.py
```

Open <http://127.0.0.1:5000> in your browser. Keep the virtual environment active when running the app. To stop it, press `Ctrl+C` in the terminal.

On Windows PowerShell, activate the environment with `.venv\\Scripts\\Activate.ps1` instead of the `source` command.

## Model

`modelbuild.py` trains a scikit-learn pipeline from the local CSV and writes `heartmodel.pkl`. The pipeline keeps feature scaling and classification together, so the app applies the same preprocessing used during training. Re-run the model build command after changing `heart.csv` or when setting up a fresh environment.

The included CSV uses remapped category codes, and its target labels are inverted relative to the app's result wording. The training and prediction code explicitly converts them so the app's positive output means the disease-present class.

The script prints holdout metrics for the current dataset and split. Those results describe this small sample only; they do not establish clinical performance.

## Project files

- `app.py`: Flask routes and result visualizations
- `prediction.py`: form validation and model inference
- `modelbuild.py`: local model training
- `heart.csv`: included training data
- `templates/` and `static/`: web interface and assets

The app does not store submitted form data. The older MongoDB helpers in `database.py` are not used by the local web app.
