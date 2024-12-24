from run_project import ProjectRunner
# from run_project import execute_query
import time
import json
from cosine_similarity import similarity



# @app.route("/execute_query", methods=['GET','POST'])
def execute_query(queries):
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    start_time = time.time()
    output_location = "project2_output.json"
    
    # Take inputs from terminal
    # queries = [
    #     "abnormal condition",
    #     "lung diseases",
    #     "diseases of the liver",
    #     "health in India"
        
    # ]
    # queries = [
    #     "Education India",
    #     "Education world",
    #     "health India",
    #     "food safety"
    # ]
    
    # queries = request.json["queries"]
    random_command = "self.indexer.get_index()"
    
    """ Running the queries against the pre-loaded index. """
    answer,doc_ids = runner.run_queries(queries, random_command)
    if answer:
        return answer,doc_ids
    else:
        answer,doc_ids = similarity(queries[0])
        if answer:
            return answer,doc_ids
        else:
            answer = "We currently don't have answer for it but we will work on it and come up with answer soon"
            return answer,000


runner = ProjectRunner()
runner.run_indexer()
if __name__ == '__main__':
    print(execute_query(["how are you ?"]))

