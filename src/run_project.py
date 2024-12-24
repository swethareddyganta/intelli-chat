from tqdm import tqdm
from preprocessor import Preprocessor
from indexer import Indexer
from collections import OrderedDict
from linkedlist import LinkedList
import inspect as inspector
import sys
import argparse
import json
import time
import random

class ProjectRunner:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.indexer = Indexer()
        self.index = self.indexer.get_index()


    def _merge(self, list1, list2):
        """Helper function to merge two posting lists"""
        result = []
        comparisons = 0
        i = j = 0
         
        while i < len(list1) and j < len(list2):
            comparisons += 1
            if list1[i] == list2[j]:
                result.append(list1[i])
                i += 1
                j += 1
            elif list1[i] < list2[j]:
                i += 1
            else:
                j += 1

        return result, comparisons

    def _daat_and(self,query, sort_by_tfidf = False):
        """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
            Use appropriate parameters & return types.
            To be implemented."""
        results = {}
        # print(f'the query given is {query}')
        postings = []
        for term in query:
            if term in self.index:
                postings.append((term, self.index[term].traverse_list()))
            else:
                postings.append((term, []))

        # Sort postings by length for optimization
        postings.sort(key=lambda x: len(x[1]))
        print(f'postings are {postings}')
        # print('corssed the line')
        # Merge postings lists
        if not postings or not postings[0][1]:  # If shortest list is empty
            result = []
            comparisons = 0
        else:
            result = postings[0][1]
            comparisons = 0

            for i in range(1, len(postings)):
                if not result:  # If intermediate result is empty
                    break
                # print(postings[0][1],postings[1][1])
                result, curr_comparisons = self._merge( result,postings[i][1])
                comparisons += curr_comparisons

            if sort_by_tfidf:
                print('using scores to sort')
                scored_results = {}
                for doc_id in result:
                    total_score = 0
                    for term in query:
                        head = self.index[term].start_node
                        while head:
                            if head.value == doc_id:
                                total_score += head.score
                                break
                            head = head.next
                    scored_results[doc_id] = total_score
                scored_results = sorted(scored_results.items(),key = lambda x:-x[1])
                print(f'The sorted score are {scored_results}')
                result = [res[0] for res in scored_results]          

        return result,comparisons
    def _daat_skip(self,query,sort_by_tfidf = False):
        
        def merge(skip1,skip2):
            new_result = LinkedList()
            comparisons = 0
            while skip1 and skip2:
                # print(f'The first node is {skip1.value}')
                # print(f'The second node is {skip2.value}')
                # print(f'Comaprisions :{comparisons}\n')
                comparisons += 1
                if skip1.value == skip2.value:
                    new_result.insert_at_end(skip1.value)
                    skip1 = skip1.next
                    skip2 = skip2.next
                elif skip1.value < skip2.value:
                    if skip1.skip and skip1.skip.value <= skip2.value:
                        while skip1.skip and skip1.skip.value <= skip2.value:
                            skip1 = skip1.skip
                            
                    else:
                        skip1 = skip1.next
                    # comparisons += 1
                else:
                    if skip2.skip and skip2.skip.value <= skip1.value:
                        while skip2.skip and skip2.skip.value <= skip1.value:
                            skip2 = skip2.skip
                            
                    else:
                        skip2 = skip2.next 
            return new_result,comparisons
        
        postings = []
        comparisons = 0
        for term in query:
            if term in self.index:
                print(f'the term is {term} and postings is {self.index[term]}')
                postings.append(self.index[term])
            else:
                postings.append([])
        print('entering crossing postings')
        print(f'these are the postings{postings}')
        result_link = postings[0]
        for i in range(1,len(postings)):
            if postings[i] == []:
                return [],0
            result_link,new_comp = merge(result_link.start_node,postings[i].start_node)
            comparisons += new_comp
            result_link.add_skip_connections()
        result = result_link.traverse_list()
        if sort_by_tfidf:
            # print('using scores to sort')
            scored_results = {}
            for doc_id in result:
                total_score = 0
                for term in query:
                    head = self.index[term].start_node
                    while head:
                        if head.value == doc_id:
                            total_score += head.score
                            break
                        head = head.next
                scored_results[doc_id] = total_score
            scored_results = sorted(scored_results.items(),key = lambda x:-x[1])
            # print(f'The sorted score are {scored_results}')
            result = [res[0] for res in scored_results]          
        return result,comparisons




    def _get_postings(self,term,use_skips = False):
        """ Function to get the postings list of a term from the index.
            Use appropriate parameters & return types.
            To be implemented."""
       
       
        postings = []
        if use_skips == False:
            if term in self.index:
                postings_list = self.index[term].traverse_list()
                postings.append(postings_list)
            return postings
        
        if use_skips == True:
            # print('entered to skip tranversal')
            if term in self.index:
                postings_list = self.index[term].traverse_skips()
                postings.append(postings_list)
            return postings


    def _output_formatter(self, op):
        """ This formats the result in the required format.
            Do NOT change."""
        if op is None or len(op) == 0:
            return [], 0
        op_no_score = [int(i) for i in op]
        results_cnt = len(op_no_score)
        return op_no_score, results_cnt

    def run_indexer(self):
        """ This function reads & indexes the corpus. After creating the inverted index,
            it sorts the index by the terms, add skip pointers, and calculates the tf-idf scores.
            Already implemented, but you can modify the orchestration, as you seem fit."""
        corpus = "final_scraped.json"
        with open(corpus, 'r', encoding='utf-8') as fp:
            self.data = json.load(fp)
            for document in tqdm(self.data['health']):
                doc_id = document['revision_id']
                document = document['summary']
                tokenized_document = self.preprocessor.tokenizer(document)
                self.indexer.generate_inverted_index(doc_id, tokenized_document)
        self.indexer.sort_terms()
        self.indexer.add_skip_connections()
        self.indexer.calculate_tf_idf()

    def sanity_checker(self, command):
        """ DO NOT MODIFY THIS. THIS IS USED BY THE GRADER. """

        index = self.indexer.get_index()
        kw = random.choice(list(index.keys()))
        return {"index_type": str(type(index)),
                "indexer_type": str(type(self.indexer)),
                "post_mem": str(index[kw]),
                "post_type": str(type(index[kw])),
                "node_mem": str(index[kw].start_node),
                "node_type": str(type(index[kw].start_node)),
                "node_value": str(index[kw].start_node.value)}
                # "command_result": eval(command) if "." in command else ""}

    def run_queries(self, query_list, random_command):
        """ DO NOT CHANGE THE output_dict definition"""
        output_dict = {
                       'daatAnd': {},
                       'daatAndSkip': {},
                       'daatAndSkipTfIdf': {},
                       'daatAndTfIdf': {},
                       'postingsList': {},
                       'postingsListSkip': {},
                       'sanity': self.sanity_checker(random_command)}

        for query in tqdm(query_list):
            """ Run each query against the index. You should do the following for each query:
                1. Pre-process & tokenize the query.
                2. For each query token, get the postings list & postings list with skip pointers.
                3. Get the DAAT AND query results & number of comparisons with & without skip pointers.
                4. Get the DAAT AND query results & number of comparisons with & without skip pointers, 
                    along with sorting by tf-idf scores."""
            input_term_arr = self.preprocessor.tokenizer(query)
            
            and_op_no_skip_sorted, and_comparisons_no_skip_sorted = self._daat_and(
                input_term_arr,sort_by_tfidf = True)
            
            and_op_no_score_no_skip_sorted, and_results_cnt_no_skip_sorted = self._output_formatter(and_op_no_skip_sorted)

            

            output_dict['daatAndTfIdf'][query.strip()] = {}
            output_dict['daatAndTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_docs'] = and_results_cnt_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['results'] = and_op_no_score_no_skip_sorted
        answer = []
        if  and_op_no_score_no_skip_sorted:     
            keys = self.data.keys()
            for key in keys:           
                for doc in self.data[key]:
                    if doc['revision_id'] == and_op_no_score_no_skip_sorted[0]:
                        answer.append(doc['summary'])
                    if len(and_op_no_score_no_skip_sorted)>1:   
                        if doc['revision_id'] == and_op_no_score_no_skip_sorted[1]:
                            answer.append(doc['summary'])

        return answer,and_op_no_score_no_skip_sorted[:2]

