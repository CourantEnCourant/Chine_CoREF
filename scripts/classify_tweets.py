"""imports DL libraries"""
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from tqdm import tqdm

label2id = {'涉案': 7, '都市': 10, '革命': 12, '农村': 4, '传奇': 0, '其它': 2,
            '传记': 1, '青少': 11, '军旅': 3, '武打': 6, '科幻': 9, '神话': 8, '宫廷': 5}
id2label = {7: '涉案', 10: '都市', 12: '革命', 4: '农村', 0: '传奇', 2: '其它',
            1: '传记', 11: '青少', 3: '军旅', 6: '武打', 9: '科幻', 8: '神话', 5: '宫廷'}


def predict_agriculture(input_txt, output_csv) -> None:
    """Classify texts"""
    # Load text
    with open(input_txt, 'r', encoding='utf-8') as f:
        texts = f.readlines()
    print(f'{len(texts)} texts to classify.')

    # Check device
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f'Using {device}.')

    # Load model
    checkpoint = "../src/pred_genre"
    tokenizer = BertTokenizer.from_pretrained(checkpoint, problem_type="single_label_classification")
    model = BertForSequenceClassification.from_pretrained(checkpoint).to(device)

    # Classify
    texts_classified = []
    idx = 1
    for text in tqdm(texts):
        inputs = tokenizer(text, truncation=True, max_length=512, return_tensors='pt')
        inputs = inputs.to(device)
        outputs = model(**inputs)
        label_id = torch.argmax(outputs.logits, dim=1).to('cpu').numpy()[0]
        label = id2label[label_id]
        if label == '农村':
            text_classified = (str(idx), str(text), str(label))
            texts_classified.append(text_classified)
            idx += 1

    # Output to csv
    with open(output_csv, 'w', encoding='utf-8') as f:
        headers = 'idx,text,label'
        f.write(headers + '\n')
        for text_classified in texts_classified:
            text = ','.join(text_classified)
            f.write(text + '\n')


if __name__ == '__main__':
    predict_agriculture(input_txt='../data/raw/tweets.txt',
                        output_csv='../data/raw/tweets_agriculture.csv')
