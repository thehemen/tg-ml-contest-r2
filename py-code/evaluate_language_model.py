import os
import time
import tqdm
import json
import subprocess
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from misc import load_github_dataset, load_telegram_dataset

if __name__ == '__main__':
    home_dir = os.getcwd()
    process_dir = '../libtglang-tester-r2/build/'

    github_dataset_name = 'github-dataset/'

    telegram_dataset_name = ['ml2023-r1-dataset/', 'ml2023-d1-dataset/']
    json_name = 'ml2023_languages.json'

    dataset = load_github_dataset(github_dataset_name, with_content=False)
    dataset.extend(load_telegram_dataset(telegram_dataset_name, with_content=False,
                                         json_name=json_name))

    labels = [x[0] for x in dataset]
    train_dataset, test_dataset = train_test_split(dataset, stratify=labels,
                                                   train_size=0.8, random_state=42)

    y_true = []
    y_pred = []

    with open('languages.json', 'r') as f:
        languages = json.load(f)

    languages = list(languages.keys())
    languages.insert(0, 'Other')

    elapsed_time = 0.0
    os.chdir(process_dir)

    for label, filename in tqdm.tqdm(test_dataset):
        y_true_now = languages.index(label[9:])
        y_true.append(y_true_now)
        t = time.perf_counter()
        result = subprocess.run(['./tglang-tester', f'{home_dir}/{filename}'], capture_output=True)
        elapsed_time += time.perf_counter() - t
        y_pred_now = int(result.stdout[:-1])
        y_pred.append(y_pred_now)

    os.chdir(home_dir)

    elapsed_time /= len(y_pred)
    precision = precision_score(y_true, y_pred, average='micro')
    recall = recall_score(y_true, y_pred, average='micro')
    f1 = f1_score(y_true, y_pred, average='micro')

    print(f'\nAverage Time: {elapsed_time:.6f}')
    print(f'Precision: {precision:.6f}')
    print(f'Recall: {recall:.6f}')
    print(f'F1-score: {f1:.6f}')

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=languages)
    disp.plot(xticks_rotation='vertical')
    plt.show()
