from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

FastTextSocialNetworkModel.MODEL_PATH = 'fasttext-social-network-model.bin'

tokenizer = RegexTokenizer()
tokens = tokenizer.split('всё очень плохо')  # [('всё', None), ('очень', None), ('плохо', None)]

model = FastTextSocialNetworkModel(tokenizer=tokenizer)


def analyse_string(s):
    result = model.predict([s], k=2)[0]
    return result


# проверка, что всё работает

messages = [
    'привет',
    'я люблю тебя!!'
]

results = model.predict(messages, k=2)

for message, sentiment in zip(messages, results):
    # привет -> {'speech': 1.0000100135803223, 'skip': 0.0020607432816177607}
    # люблю тебя!! -> {'positive': 0.9886782765388489, 'skip': 0.005394937004894018}
    print(message, '->', sentiment)
