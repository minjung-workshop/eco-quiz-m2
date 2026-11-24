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
