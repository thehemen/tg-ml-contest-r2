import os
import time
import tqdm
import subprocess
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from misc import load_telegram_dataset

if __name__ == '__main__':
    home_dir = os.getcwd()
    process_dir = '../libtglang-tester-r2/build/'

    dataset_names = ['ml2023-r1-dataset/', 'ml2023-d1-dataset/']
    dataset = load_telegram_dataset(dataset_names, with_content=False)

    labels = [x[0] for x in dataset]
    train_dataset, test_dataset = train_test_split(dataset, stratify=labels,
                                                   train_size=0.8, random_state=42)

    y_true = []
    y_pred = []

    elapsed_time = 0.0
    os.chdir(process_dir)

    for label, filename in tqdm.tqdm(test_dataset):
        y_true_now = 1 if label == '__label__CODE' else 0
        y_true.append(y_true_now)
        t = time.perf_counter()
        result = subprocess.run(['./tglang-tester', f'{home_dir}/{filename}'], capture_output=True)
        elapsed_time += time.perf_counter() - t
        y_pred_now = 1 if int(result.stdout[:-1]) else 0
        y_pred.append(y_pred_now)

    os.chdir(home_dir)

    elapsed_time /= len(y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    print(f'\nAverage Time: {elapsed_time:.6f}')
    print(f'Precision: {precision:.6f}')
    print(f'Recall: {recall:.6f}')
    print(f'F1-score: {f1:.6f}')

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Text', 'Code'])
    disp.plot()
    plt.show()
