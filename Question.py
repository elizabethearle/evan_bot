from dataclasses import dataclass, field


@dataclass
class Question:
    question: str
    correct_answer: str
    type: str
    category: str
    difficulty: str
    incorrect_answers: list = field(default_factory=lambda: [])
