"""Quiz questions checked against the reference finance model."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Question:
    question: str
    options: tuple[str, str, str, str]
    correct: int
    explanation: str
    topic: str

QUIZ = [
    Question("If MYR/USD rises from 4.50 to 4.70, what happened to MYR?",
             ("MYR appreciated", "MYR depreciated", "USD depreciated", "No change"), 1,
             "USD 1 now costs more ringgit, so MYR depreciated.", "FX quotes"),
    Question("In the exact relative PPP model, a higher Malaysian inflation rate (all else equal) means…",
             ("Lower future MYR/USD", "Unchanged MYR/USD", "Higher future MYR/USD", "Higher real rate by definition"), 2,
             "Relative PPP multiplies the spot rate by (1+MY inflation)/(1+US inflation).", "PPP"),
    Question("Which variable pair determines the covered IRP-implied forward rate?",
             ("CPI and wage growth", "Nominal MY and US interest rates", "Only MY inflation", "A stock price and GDP"), 1,
             "Covered IRP prices an FX forward using spot and matched-term interest rates.", "IRP"),
    Question("With MY inflation 3% and MY nominal interest 4%, the exact Fisher real rate is…",
             ("Exactly 4%", "Exactly 3%", "(1.04/1.03)-1 ≈ 0.97%", "Exactly 7%"), 2,
             "The real rate = (1+nominal)/(1+expected inflation)-1 = 0.9709%.", "Fisher"),
    Question("What is the best description of an IRP-implied forward rate?",
             ("Guaranteed future spot", "Market's perfect forecast", "Theoretical no-arbitrage forward price", "Actual live bank quote"), 2,
             "Covered IRP is forward pricing under assumptions, not a guaranteed future spot forecast.", "IRP"),
    Question("When PPP and IFE expected rates differ in a student scenario, the sound conclusion is…",
             ("The software must be broken", "Input assumptions need not satisfy cross-model equilibrium", "Use the larger prediction as certain", "Inflation never matters"), 1,
             "PPP uses inflation; UIP/IFE uses interest with additional assumptions. Separate model outcomes can disagree.", "Integration"),
]


def assess(answer_indices: list[int]) -> tuple[int, list[dict]]:
    if len(answer_indices) != len(QUIZ):
        raise ValueError("The quiz requires one answer per question.")
    details = []
    for q, answer in zip(QUIZ, answer_indices):
        if answer not in range(4):
            raise ValueError("Quiz answer must be 0-3.")
        details.append({"topic": q.topic, "correct": answer == q.correct,
                        "expected": q.options[q.correct], "explanation": q.explanation})
    return sum(x["correct"] for x in details), details
