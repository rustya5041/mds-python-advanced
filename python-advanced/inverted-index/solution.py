import argparse
import json

class InvertedIndex:
    """
    This class allows to perform inverted_index search on the document based on the query
    """
    def __init__(self, word_to_docs_mapping: dict):
        """
        Class constructor, takes a dict as an input.
        """
        self.word_to_docs_mapping = word_to_docs_mapping

    def query(self, words: list) -> set:
        """
        This method takes an iterable and chooses common articles for all words in the query.
        :param words: list of words
        :returns: empty set when the KeyError occurs, set of common articles otherwise
        """
        try:
            for word in words:
                return set.intersection(*[self.word_to_docs_mapping[word] for word in words])
        except KeyError:
            return set()

    def dump(self, filepath: str):
        """
        This method saves inverted index to the disk.
        :param filepath: str, path to the file where inverted index will be saved
        """
        art_ids = {art_id: list(value) for art_id, value in self.word_to_docs_mapping.items()}
        with open(filepath, 'w', encoding='utf8') as file_path:
            json.dump(art_ids, file_path)

    @classmethod
    def load(cls, filepath: str) -> "InvertedIndex":
        """
        This method loads inverted index from the disk.
        :param filepath: str, path to the file where inverted index is saved
        :returns: InvertedIndex object
        """
        with open (filepath, 'r', encoding='utf8') as file_path:
            mapping_to_revert = json.load(file_path)
            reverted_set = {word: set(index) for word, index in mapping_to_revert.items()}
            return cls(reverted_set)

def load_document(filepath: str) -> dict:
    """
    This method loads a document from the filepath and returns a {article_id : article_content} dict
    :param filepath: str, path to the file where document is saved
    :returns: dict with words as keys and articles as values
    """
    docs = {}
    with open(filepath, 'r', encoding= 'utf8') as f_p:
        for line in f_p:
            article_id, article_content = line.split('\t', 1)
            docs[article_id] = article_content.strip()
    return docs

def build_inverted_index(articles: dict) -> "InvertedIndex":
    """
    This function builds the inverted index for the document.
    :param articles: dict with words as keys and articles as values
    :returns: InvertedIndex object
    """
    word_to_docs_mapping = {}

    for article_id, article in articles.items():
        for word in article.split():
            word_to_docs_mapping.setdefault(word, set()).add(article_id)            
    return InvertedIndex(word_to_docs_mapping)

def build(args):
    """
    This function builds the inverted index for the passed document based on the argument from the command line.
    :param args: arguments from the command line
    """
    inverted_index = build_inverted_index(load_document(args.dataset))
    inverted_index.dump(args.index)

def query(args):
    """
    This function queries the inverted index for the passed document based on the argument from the command line.
    :param args: arguments from the command line
    """
    inverted_index = InvertedIndex.load(args.index)

    with open(args.query_file, 'r', encoding='utf8') as fp:
        for line in fp:
            words = line.strip().split()
            print(','.join(sorted(inverted_index.query(words), key=int)))

def main():
    """
    This function parses arguments from the command line and calls the appropriate function.
    """
    parser = argparse.ArgumentParser()   
    subparsers = parser.add_subparsers(dest='command')

    build_parser = subparsers.add_parser('build')
    build_parser.add_argument('--dataset', required=True)
    build_parser.add_argument('--index', required=True)
    build_parser.set_defaults(func=build)

    query_parser = subparsers.add_parser('query')
    query_parser.add_argument('--index', required=True)
    query_parser.add_argument('--query_file', required=True)
    query_parser.set_defaults(func=query)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()