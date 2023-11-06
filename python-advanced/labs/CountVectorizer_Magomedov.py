class CountVectorizer:
    "CountVectorizer class"
    def __init__(self, ngram_size):
        """
        Constructor for CountVectorizer

        :param ngram_size: size of tokens

        :returns: None
        """
        self.ngram_size = ngram_size

    def tokenise(string : str, ngram_size : int):
        """
        Generator method. This method tokenises a string into a list of tokens. Since there's a need to tokenize inputs both in 'fit' and 'transform' methods, additional method reduces repetativity

        :param string: string to be tokenised
        :param ngram_size: size of tokens

        :yields: a generator to slice strings
        """
        for i in range(len(string) - ngram_size + 1):
            yield string[i:i + ngram_size]

    def fit(self, corpus):
        """
        This method encodes sorted tokens into indexes and returns a respective dict

        :param corpus: list of strings

        :returns: token_to_index, a dictionary with tokens as keys, indexes as values
        """
        self.token_to_index = {}
        for string in corpus:
            for token in CountVectorizer.tokenise(string, self.ngram_size):
                if token not in self.token_to_index:
                    self.token_to_index[token] = len(self.token_to_index)        
        self.token_to_index = {token: index for index, token in enumerate(sorted(self.token_to_index.keys()))}  #sorting by key in lexicographic order
        return self.token_to_index


    def transform(self, corpus):
        """
        This method encodes corpus into a list of lists with counts of tokens in each string/line/etc

        :param corpus: list of strings

        :returns: index_to_count, a list of lists with counts of tokens in each string
        """
        self.index_to_count = []
        for string in corpus:
            str_dict = {token:0 for token in self.token_to_index.keys()}
            for token in CountVectorizer.tokenise(string, self.ngram_size):
                if token in self.token_to_index:
                    str_dict[token] += 1  # incrementing the index's vector value
            self.index_to_count.append([str_dict[token] for token in sorted(str_dict.keys())])
        return self.index_to_count
        
    def fit_transform(self, corpus):
        """
        This method simultaneously calls fit and transform on the corpus.

        :param corpus: list of strings

        :returns: index_to_count, a list of lists with counts of tokens in each string
        """
        self.fit(corpus)
        return self.transform(corpus)
