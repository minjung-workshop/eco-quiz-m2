from data import create_default_quizzes
from input_utils import read_number, read_text
from quiz import Quiz


class QuizGame:
    """퀴즈 목록과 메뉴 등 게임 전체를 관리합니다."""

    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None

    def show_menu(self):
        print("\n===== 우리 동네 생태 퀴즈 =====")
        print(f"등록된 퀴즈: {len(self.quizzes)}개")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")

    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return

        total = len(self.quizzes)
        correct_count = 0
        print(f"\n퀴즈를 시작합니다! 총 {total}문제입니다.")

        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"\n----- 문제 {number}/{total} -----")
            quiz.display()
            user_answer = read_number("정답 번호 (1~4): ", 1, 4)

            if quiz.check_answer(user_answer):
                print("정답입니다!")
                correct_count += 1
            else:
                answer_text = quiz.choices[quiz.answer - 1]
                print(f"오답입니다. 정답: {quiz.answer}번, {answer_text}")

        score = round(correct_count / total * 100)
        print(f"\n결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
        return score

    def add_quiz(self):
        print("\n새로운 생태 퀴즈를 추가합니다.")
        question = read_text("문제: ")

        choices = []
        for number in range(1, 5):
            choice = read_text(f"선택지 {number}: ")
            choices.append(choice)

        answer = read_number("정답 번호 (1~4): ", 1, 4)
        quiz = Quiz(question, choices, answer)
        self.quizzes.append(quiz)

        print(f"퀴즈가 추가되었습니다! 현재 {len(self.quizzes)}개입니다.")

    def list_quizzes(self):
        print("퀴즈 목록은 다음 단계에서 구현합니다.")

    def show_score(self):
        print("점수 확인은 다음 단계에서 구현합니다.")

    def run(self):
        try:
            while True:
                self.show_menu()
                choice = read_number("선택: ", 1, 5)

                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_score()
                else:
                    print("생태 퀴즈를 종료합니다.")
                    break

        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되어 안전하게 종료합니다.")
