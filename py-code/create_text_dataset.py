from sklearn.model_selection import train_test_split
from misc import load_telegram_dataset, save_dataset

if __name__ == '__main__':
	dataset_names = ['ml2023-r1-dataset/', 'ml2023-d1-dataset/']

	train_filename = '../../fastText/text_train.txt'
	test_filename = '../../fastText/text_test.txt'

	dataset = load_telegram_dataset(dataset_names)

	labels = [x[0] for x in dataset]
	train_dataset, test_dataset = train_test_split(dataset, stratify=labels,
		                                           train_size=0.8, random_state=42)

	save_dataset(train_filename, train_dataset)
	save_dataset(test_filename, test_dataset)

	print(f'Train set: {len(train_dataset)}.')
	print(f'Test set: {len(test_dataset)}.')
