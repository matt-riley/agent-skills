# Agentic Evaluation Patterns

Annotated examples of the three core evaluation strategies. Use these as a starting point — adapt to your agent's language, framework, and output contract.

## The evaluation loop

```
Generate → Evaluate → Critique → Refine → Output
    ↑                              │
    └──────────────────────────────┘
```

The loop exits when the output meets the score threshold or the iteration budget is exhausted. Always set both.

## Best practices

| Practice | Rationale |
| --- | --- |
| Clear criteria up front | Criteria added mid-loop make scores incomparable across iterations |
| Iteration limit (3–5) | Prevents infinite loops; most quality gains come in the first 2–3 passes |
| Convergence check | Exit early if the score is not improving; oscillating loops waste budget |
| Log full trajectory | Evaluation loops are opaque without a history of scores and critiques |
| Structured output | JSON evaluation results are reliable to parse; free-text critique is not |

---

## Pattern 1: Basic reflection

Agent evaluates its own output through self-critique. Use when a single LLM can both generate and judge.

```python
def reflect_and_refine(task: str, criteria: list[str], max_iterations: int = 3) -> str:
    output = llm(f"Complete this task:\n{task}")
    prev_score = None

    for i in range(max_iterations):
        critique = json.loads(llm(f"""
        Evaluate this output against criteria: {criteria}
        Output: {output}
        Return JSON: {{"scores": {{"criterion": {{"status": "PASS|FAIL", "feedback": "..."}}}}}}
        """))

        all_pass = all(c["status"] == "PASS" for c in critique["scores"].values())
        if all_pass:
            break

        failed = {k: v["feedback"] for k, v in critique["scores"].items() if v["status"] == "FAIL"}
        output = llm(f"Improve to address: {failed}\nOriginal: {output}")

    return output
```

**Key decisions:** Use `PASS`/`FAIL` per criterion rather than a single aggregate score — it makes the refine step more actionable.

---

## Pattern 2: Evaluator-optimizer

Separate generation and evaluation into distinct components. Use when you want to swap the evaluator independently, compare evaluator strategies, or scale generation and evaluation separately.

```python
class EvaluatorOptimizer:
    def __init__(self, score_threshold: float = 0.8, max_iterations: int = 3):
        self.score_threshold = score_threshold
        self.max_iterations = max_iterations

    def generate(self, task: str) -> str:
        return llm(f"Complete: {task}")

    def evaluate(self, output: str, task: str) -> dict:
        return json.loads(llm(f"""
        Evaluate output for task: {task}
        Output: {output}
        Return JSON: {{"overall_score": 0-1, "dimensions": {{"accuracy": ..., "clarity": ...}}, "critique": "..."}}
        """))

    def optimize(self, output: str, feedback: dict) -> str:
        return llm(f"Improve based on feedback: {feedback['critique']}\nOutput: {output}")

    def run(self, task: str) -> str:
        output = self.generate(task)
        prev_score = None
        history = []

        for _ in range(self.max_iterations):
            evaluation = self.evaluate(output, task)
            history.append({"output": output, "score": evaluation["overall_score"]})

            if evaluation["overall_score"] >= self.score_threshold:
                break
            if prev_score is not None and evaluation["overall_score"] <= prev_score:
                break  # convergence check: score not improving

            prev_score = evaluation["overall_score"]
            output = self.optimize(output, evaluation)

        return output
```

**Key decisions:** The convergence check (`score <= prev_score`) prevents wasted iterations when the loop has plateaued.

---

## Pattern 3: LLM-as-judge

Use a separate LLM instance to compare and rank outputs. Use when you want human-preference-style scoring or when the primary LLM has a self-serving bias as its own judge.

```python
def llm_judge(output_a: str, output_b: str, criteria: str) -> dict:
    return json.loads(llm(f"""
    Compare outputs A and B for: {criteria}
    Output A: {output_a}
    Output B: {output_b}
    Return JSON: {{"winner": "A|B|tie", "rationale": "...", "scores": {{"A": 0-1, "B": 0-1}}}}
    """))
```

To use in an iteration loop, generate multiple candidates and pass the winner forward as the base for the next iteration.

---

## Pattern 4: Rubric-based scoring

Score outputs against weighted dimensions. Use when you need a numeric quality signal for multiple criteria with different importance weights.

```python
RUBRIC = {
    "accuracy":     {"weight": 0.4},
    "clarity":      {"weight": 0.3},
    "completeness": {"weight": 0.3},
}

def evaluate_with_rubric(output: str, rubric: dict) -> float:
    raw = json.loads(llm(f"""
    Rate 1–5 for each dimension: {list(rubric.keys())}
    Output: {output}
    Return JSON: {{"dimension_name": score, ...}}
    """))
    return sum(raw[d] * rubric[d]["weight"] for d in rubric) / 5.0
```

**Key decisions:** Normalize the final score to 0–1 so it is comparable to `score_threshold` in Pattern 2. Define the rubric before any generation begins.
