import re
import glob
import json
from tqdm import tqdm

signs = [
    ['//', '/\*', '\*/'],  # C++
    ['# ', '"""', '"""'],  # Python
    ['--', '<!--', '-->'],  # HTML
    ['--', '--[', ']]'],  # Lua
    [';;', '"""', '"""']  # FunC
]

def replace_text(text, signs, pattern):
    for sign in signs:
        text = re.sub(re.compile(f'{sign}.*?{sign}', re.DOTALL), pattern, text)

    return text

def replace_comments(text, signs):
    for one, first, second in signs:
        text = re.sub(re.compile(f'{first}.*?{second}', re.DOTALL), ' comment ', text)
        text = re.sub(re.compile(f'{one}.*?(\n|$)'), ' comment ', text)

    return text

def split_text(text):
    return re.findall(r"\w+|[^\w\s]", text, re.UNICODE)

def tokenize(source_code):
    clean_code = replace_text(replace_comments(source_code, signs), '\'"', ' text ')
    text = ' '.join(split_text(clean_code))
    return text

def load_telegram_dataset(dataset_names, with_content=True, json_name=''):
    dataset = []

    if json_name:
        with open(json_name, 'r') as f:
            languages = json.load(f)

    for dataset_name in dataset_names:
        for filename in glob.iglob(dataset_name + '/**/*/*', recursive=True):
            if json_name:
                if filename in languages.keys():
                    class_name = languages[filename]
                else:
                    continue
            else:
                class_name = filename.split('/')[2].split('.')[0].split('-')[1]

            label = f'__label__{class_name}'

            if not with_content:
                dataset.append(tuple((label, filename)))
            else:
                with open(filename, 'r') as f:
                    text = tokenize(f.read())
                    dataset.append(tuple((label, text)))

    return dataset

def load_github_dataset(dataset_name, with_content=True):
    dataset = []

    for filename in tqdm(glob.iglob(dataset_name + '/**/*/*', recursive=True)):
        class_name = filename.split('/')[1]
        label = f'__label__{class_name}'

        if not with_content:
            dataset.append(tuple((label, filename)))
        else:
            with open(filename, 'r') as f:
                text = tokenize(f.read())
                dataset.append(tuple((label, text)))

    return dataset

def save_dataset(filename, dataset):
    with open(filename, 'w') as f:
        for label, text in dataset:
            f.write(f'{label} {text}\n')
