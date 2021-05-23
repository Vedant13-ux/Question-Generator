from summarizer import Summarizer


def get_summary(text, min_length, max_length, ratio):
    model = Summarizer()
    result = model(text, min_length= min_length, max_length = max_length , ratio = ratio)
    summarized_text = ''.join(result)
    return summarized_text

