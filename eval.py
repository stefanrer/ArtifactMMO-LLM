import pathlib
import json
from tqdm import tqdm

import pandas as pd

import os
import dotenv
import threading
from queue import Queue

import src.prompts as prompts
import src.utils as utils

dotenv.load_dotenv(".env")


def judge(item, q):
    judge_model = f"{os.environ.get('JUDGE_MODEL')}"
    judge_api_link = f"{os.environ.get('JUDGE_API_LINK')}"
    token = f"{os.environ.get('TOKEN')}"

    with sem:
        eval = utils.send_question(
            prompt=prompts.EVALUATION_PROMPT.format(
                response=item["generated_answer"],
                reference_answer=item["true_answer"],
            ),
            model=judge_model,
            api_link=judge_api_link,
            token=token,
            temperature=0.1,
            max_tokens=512,
        )

    try:
        feedback, score = [i.strip() for i in eval.split("[RESULT]")]
        print(f"Score: {score}\nFeedback: {feedback}")
        item["feedback"] = feedback
        item["score"] = score

        with q_lock:
            q.put(item)
    except Exception:
        return


def extract_answers(task, answers):
    return '\n'.join(answers[task])


if __name__ == "__main__":
    eval_files = ["data/test_model.json"]
    tasks = ["craft_copper_dagger", "kill_yellow_slime"]

    perfect_answers = json.loads(pathlib.Path('data/perfect_answers.json').read_text())

    for idx, eval_file in enumerate(eval_files):
        data = json.loads(pathlib.Path(eval_file).read_text())

        outputs = []

        for task in tasks:
            gt = extract_answers(task, perfect_answers)
            answer = extract_answers(task, data)

            result = {
                "true_answer": gt,
                "generated_answer": answer,
            }

            outputs.append(result)

        pathlib.Path(f"eval/eval_ans_{idx}.json").write_text(json.dumps(outputs, indent=2))

        with open(f"eval/eval_ans_{idx}.json", "w") as f:
            json.dump(outputs, f, indent=2)

        flattened_data = json.loads(pathlib.Path(f"eval/eval_ans_{idx}.json").read_text())

        sem = threading.Semaphore(1)

        q_lock = threading.Lock()

        threads = []
        q = Queue()
        for item in tqdm(flattened_data):
            thread = threading.Thread(target=judge, args=(item, q))
            thread.start()
            threads.append(thread)

        [_.join() for _ in threads]

        res = []
        while not q.empty():
            res.append(q.get())

        with open(f"eval/eval_res_{idx}.json", "w") as f:
            json.dump(res, f, indent=2)


    for idx, eval_file in enumerate(eval_files):
        df = pd.read_json(f"eval/eval_res_{idx}.json")

        print(f"Eval file: {eval_file}\n")
        print(f"Model: {json.loads(pathlib.Path(eval_file).read_text())['model_info']}")
        print(f"Judge model: {os.environ.get('JUDGE_MODEL')}\n")

        print(df.score.value_counts(), end="\n\n")

        print("Mean score: " + str(df.score[df.score != 0].mean()))
        print("Median score: " + str(df.score[df.score != 0].median()))
        print("Percentage: " + str(df.score[df.score != 0].mean() / 5 * 100))

        print("\n\n")
