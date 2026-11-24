class Quiz:
    """문제 하나의 데이터와 동작을 관리합니다."""

    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = list(choices)
        self.answer = answer

    def display(self):
        """문제와 번호가 붙은 선택지를 출력합니다."""
        print(f"\n{self.question}")

        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def check_answer(self, user_answer):
        """사용자 답이 정답이면 True를 반환합니다."""
        return user_answer == self.answer

    def to_dict(self):
        """퀴즈 객체를 저장 가능한 딕셔너리로 변환합니다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """딕셔너리를 검사하고 퀴즈 객체로 복원합니다."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈는 딕셔너리여야 합니다.")

        question = data.get("question")
        choices = data.get("choices")
        answer = data.get("answer")

        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제 내용이 올바르지 않습니다.")

        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 4개여야 합니다.")

        if not all(isinstance(item, str) and item.strip() for item in choices):
            raise ValueError("선택지에 빈 내용이나 잘못된 값이 있습니다.")

        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답 번호는 1~4의 정수여야 합니다.")

        return cls(question, choices, answer)
