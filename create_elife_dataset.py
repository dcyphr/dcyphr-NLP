import requests
import os
import Levenshtein


def calculate_nb_chars(original_sentence, simple_sentence):
    """Calculate and return the character length ratio between an original
    sentence and a simplified sentence"""
    return round(len(simple_sentence) / len(original_sentence), 1)


def get_levenshtein_similarity(complex_sentence, simple_sentence):
    """ Return the similarity between complex_sentence and simple_sentence """
    return round(Levenshtein.ratio(complex_sentence, simple_sentence), 1)


def get_digest_original(article_id):

    url = "https://prod--gateway.elifesciences.org/articles/{}".format(
        article_id)
    r = requests.get(url).json()

    try:
        contents = r['digest']['content']
    except:
        return 1

    digest = ""
    for content in contents:
        try:
            digest = digest + content['text']
        except:
            pass

    abstract = r['abstract']['content'][0]['text']

    for section in r['body']:
        if 'discussion' in section['title'].lower():
            discussion = section['content'][0]['text']

    abstract_discussion = abstract + discussion
    return (digest, abstract_discussion)


def main():
    source_file = "elife/source.txt"
    target_file = "elife/target.txt"
    total_url = "https://prod--gateway.elifesciences.org/articles?per-page=100"
    r = requests.get(total_url).json()
    items = r['items']

    if os.path.isfile(source_file):
        os.remove(source_file)
    if os.path.isfile(target_file):
        os.remove(target_file)
    source = open(source_file, 'a')
    target = open(target_file, 'a')

    for item in items:

        digest_original = get_digest_original(item['id'])

        if digest_original == 1:
            continue
        else:
            original = digest_original[1]
            digest = digest_original[0]

        source.write('\n')
        source.write(
            "<NbChars_" + str(calculate_nb_chars(original, digest)) + ">")
        source.write(
            "<LevSim_" + str(get_levenshtein_similarity(original, digest)) + ">")
        source.write(
            "<" + "Discussion" + ">")
        source.write(original)

        target.write('\n')
        target.write(digest)


if __name__ == '__main__':
    main()
