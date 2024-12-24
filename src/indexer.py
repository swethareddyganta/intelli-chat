from collections import OrderedDict
from linkedlist import LinkedList
class Indexer:
    def __init__(self):
        """Initialize the inverted index and document statistics"""
        self.inverted_index = OrderedDict({})
        self.doc_lengths = {}  # used to calc Term freq
        self.term_frequencies = {}  # Used to calc Term freq
        self.total_docs = 0

    def get_index(self):
        """Return the inverted index"""
        return self.inverted_index

    def generate_inverted_index(self, doc_id, tokenized_document):
        """Add tokenized document to the index"""
        
        self.doc_lengths[doc_id] = len(tokenized_document) # length of each doc
        self.total_docs += 1 # count the total no of documents

        
        term_freq = {}
        for t in tokenized_document:
            self.add_to_index(t, doc_id) # add term to the document
            term_freq[t] = term_freq.get(t, 0) + 1 # increase the count if the term exists in the document
        self.term_frequencies[doc_id] = term_freq
            

    def add_to_index(self, term_, doc_id_):
        """Add term and document id to the index"""
        
        if term_ not in self.inverted_index:
            self.inverted_index[term_] = LinkedList()
            self.inverted_index[term_].insert_at_end(doc_id_)
            return

        # Get the posting list for the term
        postings = self.inverted_index[term_]

        current = postings.start_node
        while current is not None:
            if current.value == doc_id_:
                return
            current = current.next

        
        postings.insert_at_end(doc_id_)

    def sort_terms(self):
        """Sort the index by terms"""
        sorted_index = OrderedDict({})
        for k in sorted(self.inverted_index.keys()):
            sorted_index[k] = self.inverted_index[k]
        self.inverted_index = sorted_index

    def add_skip_connections(self):
        """Add skip pointers to all posting lists"""
        for term in self.inverted_index:
            self.inverted_index[term].add_skip_connections()

    def calculate_tf_idf(self):
        """Calculate tf-idf scores for all documents in the index"""
        for term, postings in self.inverted_index.items():
            # Update IDF for the term
            postings.rare_term(self.total_docs)
            #update the total documents and update the IDF Value
            current = postings.start_node
            while current is not None:
                count_term = self.term_frequencies[current.value].get(term, 0)# freq of doc in current term
                tf = count_term / self.doc_lengths[current.value] # divided by total length of the document
                current.score = tf * postings.idf
                current = current.next
