
## Data Preprocessing

### 1. Install dependencies

```bash
pip install -r data_processing/requirements.txt
```

### 2. Place the raw dataset

```
dataset/raw/
```

### 3. Run preprocessing

```bash
python data_processing/run_pipeline.py
```

### Output

```
dataset/processed/
├── images/
└── processed_styles.csv
```