from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig

# see ``examples/summarization/bart/run_eval.py`` for a longer example
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
with open('long_article.txt', 'r') as file:
    ARTICLE_TO_SUMMARIZE = file.read().replace('\n', '')
inputs = tokenizer.batch_encode_plus([ARTICLE_TO_SUMMARIZE], max_length=1024, return_tensors='pt')
# Generate Summary
summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=300, early_stopping=True)
print([tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids])