# AI-Powered Fashion Recommendation System

## Project Overview

This project is an AI-based fashion recommendation system that provides personalized clothing recommendations based on a user's uploaded photo and preferences. The system analyzes the user's visual features using the ResNet50 deep learning model for feature extraction, recommends suitable outfits, and generates a virtual try-on preview to help users visualize the selected clothing before making a decision.

## Problem Statement

Choosing suitable clothing for different occasions can be difficult, especially when shopping online. Users often struggle to determine which outfits match their appearance, body type, and personal preferences. This project aims to solve this problem by providing intelligent outfit recommendations and a virtual try-on experience.

## Target Users

- Online shoppers
- Fashion enthusiasts
- Students and professionals
- Anyone looking for personalized outfit recommendations



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