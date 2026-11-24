from data import create_default_quizzes
from input_utils import read_number


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
        print("퀴즈 풀기는 다음 단계에서 구현합니다.")

    def add_quiz(self):
        print("퀴즈 추가는 다음 단계에서 구현합니다.")

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
