import os
import json
from drs import drs
from tqdm import tqdm
from datasets import load_dataset

def get_language_nums(languages, lower_coeff, upper_coeff, sample_num):
    score_sum = sum(languages.values())
    languages = {k: v / score_sum for k, v in languages.items()}

    n = len(languages)

    lower_bounds = []
    upper_bounds = []

    for score in languages.values():
        lower_bounds.append(int(round(sample_num * score * lower_coeff)))
        upper_bounds.append(int(round(sample_num * score * upper_coeff)))

    nums = drs(n, sample_num, upper_bounds, lower_bounds)
    nums = [int(round(x)) for x in nums]
    languages = {k: v for k, v in zip(languages.keys(), nums)}
    return languages

if __name__ == '__main__':
    sample_num = 100000

    lower_coeff = 0.9
    upper_coeff = 1.1

    dataset_name = 'github-dataset/'

    if not os.path.exists(dataset_name):
        os.mkdir(dataset_name)

    skipped_language_names = ['FunC', 'TL']

    with open('languages.json', 'r') as f:
        languages = json.load(f)

    languages = get_language_nums(languages, lower_coeff, upper_coeff, sample_num)

    for language, num in languages.items():
        if language in skipped_language_names:
            continue

        language_name = f'{dataset_name}{language}/'
        print(language)

        if not os.path.exists(language_name):
            os.mkdir(language_name)

        ds = load_dataset('bigcode/the-stack', data_dir=f'data/{language.lower()}',
                          streaming=True, split='train')

        with tqdm(total=num) as tqdm_bar:
            for sample in iter(ds):
                content = sample['content']
                repo_name = sample['max_stars_repo_name'].replace('/', '\\')
                repo_path = sample['max_stars_repo_path']
                filename = repo_path.split('/')[-1]

                with open(f'{language_name}({repo_name})_{filename}', 'w') as f:
                    f.write(content)

                tqdm_bar.update(1)

                if tqdm_bar.n == num:
                    break

        print()

    print(f'All code samples are saved to {dataset_name}.')
