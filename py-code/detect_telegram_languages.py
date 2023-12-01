import json
import guesslang
from tqdm import tqdm
from misc import load_telegram_dataset

if __name__ == '__main__':
    guess = guesslang.Guess()

    language_dict = {
        'C#': 'C-Sharp',
        'Objective-C': 'Objective-C++'
    }

    dataset_names = ['ml2023-r1-dataset/', 'ml2023-d1-dataset/']
    json_name = 'ml2023_languages.json'

    dataset = load_telegram_dataset(dataset_names, with_content=False)

    with open('languages.json', 'r') as f:
        language_stats = json.load(f)

    languages = {}

    for label, filename in tqdm(dataset):
        if label == '__label__OTHER':
            continue

        with open(filename, 'r') as f:
            text = f.read()
            language_name = guess.language_name(text)

            if language_name in language_dict.keys():
                language_name = language_dict[language_name]

            if language_name not in language_stats.keys():
                continue

            languages[filename] = language_name

    with open(json_name, 'w') as f:
        json.dump(languages, f)

    print(f'Telegram source code languages are saved to {json_name}.')
