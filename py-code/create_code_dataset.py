from sklearn.model_selection import train_test_split
from misc import load_github_dataset, load_telegram_dataset, save_dataset

if __name__ == '__main__':
    github_dataset_name = 'github-dataset/'

    telegram_dataset_name = ['ml2023-r1-dataset/', 'ml2023-d1-dataset/']
    json_name = 'ml2023_languages.json'

    train_filename = '../../fastText/code_train.txt'
    test_filename = '../../fastText/code_test.txt'

    dataset = load_github_dataset(github_dataset_name)
    dataset.extend(load_telegram_dataset(telegram_dataset_name, json_name=json_name))

    labels = [x[0] for x in dataset]
    train_dataset, test_dataset = train_test_split(dataset, stratify=labels,
                                                   train_size=0.8, random_state=42)

    save_dataset(train_filename, train_dataset)
    save_dataset(test_filename, test_dataset)

    print(f'\nTrain set: {len(train_dataset)}.')
    print(f'Test set: {len(test_dataset)}.')
