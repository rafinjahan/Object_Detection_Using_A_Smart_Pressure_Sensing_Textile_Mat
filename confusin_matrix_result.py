import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold, cross_val_score, cross_val_predict
from sklearn.metrics import classification_report, confusion_matrix, matthews_corrcoef, cohen_kappa_score
import matplotlib.pyplot as plt
import seaborn as sns
import os

script_folder = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_folder, 'tablecloth_dataset_flattened.csv')
df = pd.read_csv(csv_path, sep=';')
if len(df.columns) == 1:
    df = pd.read_csv(csv_path, sep=',')

df['raw_label'] = df['state'].astype(str) + " " + df['item'].astype(str)
label_mapping = {
    'empty plate': 'Empty Plate',
    'full plate': 'Full Plate',
    'empty bowl': 'Empty Bowl',
    'full bowl': 'Full Bowl',
    'empty muumi_cup_arabia': 'Empty Cup',
    'full muumi_cup_arabia': 'Full Cup',
    'full coke_0.33l': 'Full 0.33L Can',
    'full coke_1.5l': 'Full 1.5L Bottle'
}
df['label'] = df['raw_label'].map(label_mapping).fillna(df['raw_label'])
df = df.sort_values(by=['label', 'time']).reset_index(drop=True)
df['time_diff'] = df.groupby('label')['time'].diff().fillna(999)
df['new_placement'] = (df['time_diff'] > 2.0).astype(int)
df['placement_id'] = df['label'] + '_' + df['new_placement'].cumsum().astype(str)

X = df.loc[:, 'p0':'p15']
y = df['label']
groups = df['placement_id']

rf = RandomForestClassifier(random_state=42)
gkf = GroupKFold(n_splits=5)

cv_scores = cross_val_score(rf, X, y, groups=groups, cv=gkf, scoring='accuracy')
y_pred = cross_val_predict(rf, X, y, groups=groups, cv=gkf)

mcc   = matthews_corrcoef(y, y_pred)
kappa = cohen_kappa_score(y, y_pred)

print("RESULTS")
print(f"Grouped 5-Fold CV Accuracy {cv_scores.mean()*100:.2f}% +/- {cv_scores.std()*100:.2f}%")
print(f"MCC {mcc:.4f}")
print(f"Cohen Kappa {kappa:.4f}")
print()
print("Classification Report")
print(classification_report(y, y_pred))

cm = confusion_matrix(y, y_pred, labels=sorted(y.unique()))
classes = sorted(y.unique())

plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
plt.title("Confusion Matrix Grouped 5-Fold CV", fontsize=14)
plt.xlabel("Predicted Label", fontsize=12)
plt.ylabel("True Label", fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

image_path = os.path.join(script_folder, 'confusion_matrix_grouped_cv.png')
plt.savefig(image_path, dpi=300)
print(f"Confusion matrix saved to {image_path}")