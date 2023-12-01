# Telegram ML Competition 2023, Round 2

This project is implemented for the [ML Competition 2023, Round 2](https://contest.com/docs/ML-Competition-2023-r2) which task is to create a library that detects a programming or markup language of a code snippet.

## How to Create Dataset

There are two different classification targets of this work: is the code snippet actually a source code sample or an user text sample, and if it is a code, what is the programming or markup language of it.

The make the code/text classification, the Telegram dataset samples are used. There are ~40k text samples and ~4k code samples.

To make the source code language classification, [the Stack dataset](https://huggingface.co/datasets/bigcode/the-stack) that consists of the GitHub source code samples is used. Although it is the 6 TB archive, ~100k source code samples are used in the dataset. Make sure you have your own access token to use the HuggingFace API.

To have the fair distribution of programming languages, [the TIOBE index](https://www.tiobe.com/tiobe-index/) is used here.

First of all, you need to install all the dependencies required to create a dataset:

```sh
pip install -r requirements.txt
```

Then, you should download the GitHub code samples:

```sh
python3 download_code_dataset.py
```

To detect programming languages of the Telegram source code samples, you can run the script based on the GuessLang library:

```sh
python3 detect_telegram_languages.py
```

To create the code/text dataset, run:

```sh
python3 create_text_dataset.py
```

To create the source code language dataset, run:

```sh
python3 create_code_dataset.py
```

## How to Train Model

The Facebook's [fastText](https://github.com/facebookresearch/fastText) library is used here. To build it, please follow the official instructions.

To train the code/text classification model, run this command:

```sh
./fasttext supervised -input text_train.txt -output text_model
```

To train the language classification model, run this one:

```sh
./fasttext supervised -input code_train.txt -output code_model
```

The inference speed of the models can be low. To accelerate it, you can use the quantization technique.

To quantize the code/text classification model, run:

```sh
./fasttext quantize -input text_train.txt -output text_model -qnorm -cutoff 10000 -retrain
```

To quantize the language classification model, run:

```sh
./fasttext quantize -input code_train.txt -output code_model -qnorm -cutoff 10000 -retrain
```

The quantization allows you to compress the model by 10x-1000x times so that it makes the model loading time acceptable.

## How to Build Library

To build the library, run:

```sh
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build .
```

To build the test script, run:

```sh
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build .
```

## How to Evaluate Model

To evaluate the model quality and performance, the average time, precision, recall and F1-score metrics are used.

To compare the programming and markup language results, [the confusion matrix](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ConfusionMatrixDisplay.html) is used as well.

To evaluate the code/text classification model, run:

```sh
python3 evaluate_text_model.py
```

To evaluate the language classification model, run:

```sh
python3 evaluate_language_model.py
```

Good luck!

## Results

This solution is among winners with the 4th place in [the leaderboard](https://contest.com/ml2023-r2).

|Name|Value|
|----|-----|
|Code Language Detection|71.9|
|Overall Detection|94.5|
|Average Time|16.8ms per sample|
|Final Score|30.6|
