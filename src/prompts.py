EVALUATION_PROMPT = """###Task Description:
An instruction (might include an Input inside it), a response to evaluate, a reference answer that gets a score of 5, and a score rubric representing a evaluation criteria are given.
1. Write a detailed feedback that assess the quality of the response strictly based on the given methodology, not evaluating in general.
2. After writing a feedback, write a score that is an integer, equal or less than 5. You should refer to the score rubric.
3. The output format should look as follows: \"Feedback: {{write a feedback for criteria}} [RESULT] {{an integer equal or less than 5}}\"
4. Please do not generate any other opening, closing, and explanations. Be sure to include [RESULT] in your output.
5. Denote all problems with the answer in an enumerated list and add detractions of score based on score rubric list below.
6. Each problem results in detraction of at least 1 point from final score.
7. Some problems limit the maximum score of the response.
8. After writing down all problems, you need to write the final resulting score.


###Response to evaluate:
{response}

###Reference Answer (Score 5):
{reference_answer}

###Score Rubrics:
[Is the response correct, accurate, and factual based on the reference answer?]
1. If the response has incorrect or changed coordinates, you need to detract 3 points per error. The answer cannot get score more than 3.
2. If the response has missing instructions, you need to detract 3 points per error. The answer cannot get score more than 3.
3. If the response is tasking the agent to get less resources than the reference answer, you need to detract 2 points per error. The answer cannot get score more than 3.
4. If the response is tasking the agent to get more resources than the reference answer, you need to detract 1 point per error.

###Feedback:"""
