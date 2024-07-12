"""Import pandas and datasets to create datasets from training"""
import pandas as pd
from pandas import DataFrame
from datasets import Dataset

from pathlib import Path
from typing import Tuple


id2label = {0: 'non-protest', 1: 'protest'}
label2id = {'non-protest': 0, 'protest': 1}


def preprocess_positive(positive: Path, threshold: float) -> DataFrame:
    """Select tweets with prob2_combined above threshold. Extract only tweets' content"""
    df_positive = pd.read_csv(positive, sep='\t')
    positive_preprocessed = df_positive[df_positive['prob2_combined'] > threshold]['content'].to_frame()

    return positive_preprocessed


def preprocess_negative(negative: Path, size: int) -> DataFrame:
    """Negative set will have the same size and format as the positive set"""
    df_negative = pd.read_csv(negative, sep=',')
    df_negative_resized = df_negative.sample(n=size, random_state=42)
    negative_preprocessed = df_negative_resized["seged_weibo"]
    negative_preprocessed = negative_preprocessed.str.replace(' ', '', regex=False)

    return negative_preprocessed


def give_label(df_tweets: DataFrame, label: str) -> DataFrame:
    """Label a dataframe with following headers: tweets, label_id and label"""
    df_tweets.columns = ['tweets']
    df_tweets['label'] = label
    df_tweets['label_id'] = label2id[label]

    return df_tweets


def label_combine_and_shuffle(positive_preprocessed: DataFrame, negative_preprocessed: DataFrame) -> DataFrame:
    # Label
    positive_labeled = give_label(positive_preprocessed, label='protest')
    negative_labeled = give_label(negative_preprocessed, label='non-protest')

    # Combine
    combined_preprocessed = pd.concat([positive_labeled, negative_labeled], ignore_index=True)

    # Shuffle and provide index
    combined_shuffled = combined_preprocessed.sample(frac=1).reset_index(drop=True)
    combined_shuffled['idx'] = range(len(combined_shuffled))

    return combined_shuffled


def split_train_dev_test(dataset: Dataset, percentage: float) -> Tuple[Dataset, Dataset, Dataset]:
    # Train
    train_dev_test = dataset.train_test_split(train_size=percentage)
    train = train_dev_test['train']

    # Dev and test, will have the same size
    dev_test = train_dev_test['test'].train_test_split(train_size=0.5)
    dev = dev_test['train']
    test = dev_test['test']

    return train, dev, test


def main(positive, negative, output_folder, threshold, percentage):
    """1. Generate positive and negative sets,
    2. Combine and shuffle them,
    3. Split into test/dev/train,
    4. Output to .parquet"""
    # 1.
    positive_preprocessed = preprocess_positive(positive, threshold)
    size = len(positive_preprocessed)
    negative_preprocessed = preprocess_negative(negative, size)
    # 2.
    combined_shuffled = label_combine_and_shuffle(positive_preprocessed, negative_preprocessed)
    dataset = Dataset.from_pandas(combined_shuffled)
    # 3.
    train, dev, test = split_train_dev_test(dataset, percentage)
    # 4.
    train.to_parquet(f'{output_folder}/train.parquet', compression='snappy')
    dev.to_parquet(f'{output_folder}/dev.parquet', compression='snappy')
    test.to_parquet(f'{output_folder}/test.parquet', compression='snappy')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Clean raw data, generate dataset ready to train.')
    parser.add_argument('-p', '--positive', default='../data/raw/protest_posts.csv', type=Path, help='Path to positive set')
    parser.add_argument('-n', '--negative', default='../data/raw/WeiboSentiment2019.csv', type=Path, help='Path to negative set. Will have the same size as positive set.')
    parser.add_argument('-o', '--output_folder', default='../data/clean', type=Path, help='Folder to write output .parquet files.')
    parser.add_argument('-t', '--threshold', metavar='', default=0.6, type=float, help='Threshold for tweets above certain probabilities. Default set to 0.6.')
    parser.add_argument('-pct', '--percentage', metavar='', default=0.8, type=float, help='Percentage of training set. Default set to 0.8. Dev and test have equal size from the rest.')

    args = parser.parse_args()

    # Check arguments' value
    if not args.output_folder.is_dir():
        raise ValueError('Output folder should be a folder.')
    if not 0 < args.threshold < 1:
        raise ValueError('Threshold should be between 0 and 1')
    if not 0 < args.percentage < 1:
        raise ValueError('Percentage should be between 0 and 1')

    main(
        positive=args.positive,
        negative=args.negative,
        output_folder=args.output_folder,
        threshold=args.threshold,
        percentage=args.percentage,
    )