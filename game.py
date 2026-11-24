import json
import time
from pathlib import Path

from data import create_default_quizzes
from input_utils import read_number, read_text
from quiz import Quiz


class QuizGame:
    """퀴즈 목록과 메뉴 등 게임 전체를 관리합니다."""

    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.state_path = Path(__file__).resolve().parent / "state.json"
        self.save_enabled = True
        self.load_state()

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
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("새로운 최고 점수입니다!")
            self.save_state()

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
        if self.save_state():
            print("추가한 퀴즈를 저장했습니다.")

        print(f"퀴즈가 추가되었습니다! 현재 {len(self.quizzes)}개입니다.")

    def list_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")

    def show_score(self):
        if self.best_score is None:
            print("아직 퀴즈를 완료한 기록이 없습니다.")
            return

        print(f"\n최고 점수: {self.best_score}점")

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
        finally:
            if self.save_state():
                print("퀴즈와 점수를 저장했습니다.")

    def load_state(self):
        """저장 파일을 읽고 데이터를 검사합니다."""
        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("저장 데이터는 딕셔너리여야 합니다.")

            quizzes_data = data["quizzes"]
            best_score = data["best_score"]

            if not isinstance(quizzes_data, list):
                raise ValueError("퀴즈 목록 형식이 올바르지 않습니다.")

            quizzes = [Quiz.from_dict(item) for item in quizzes_data]

            if best_score is not None:
                if type(best_score) is not int or not 0 <= best_score <= 100:
                    raise ValueError("최고 점수는 0~100의 정수여야 합니다.")

            self.quizzes = quizzes
            self.best_score = best_score
            print(f"저장된 데이터를 불러왔습니다. 퀴즈 {len(quizzes)}개")

        except FileNotFoundError:
            print("저장 파일이 없어 기본 퀴즈로 시작합니다.")

        except (ValueError, KeyError, UnicodeError) as error:
            print(f"저장 파일이 손상되어 기본 퀴즈로 시작합니다: {error}")
            try:
                backup = self.state_path.with_name(
                    f"state.corrupt-{time.time_ns()}.json"
                )
                self.state_path.rename(backup)
                print(f"손상된 파일 보관: {backup.name}")
            except OSError as backup_error:
                self.save_enabled = False
                print(f"원본 보호를 위해 저장을 중단합니다: {backup_error}")

        except OSError as error:
            self.save_enabled = False
            print(f"파일을 읽을 수 없어 기본 퀴즈로 시작합니다: {error}")
            print("기존 파일 보호를 위해 이번 실행에서는 저장하지 않습니다.")

    def save_state(self):
        """임시 파일에 쓴 뒤 저장 파일을 교체합니다."""
        if not self.save_enabled:
            print("저장을 건너뜁니다. 파일 접근 상태를 확인해주세요.")
            return False

        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        temporary_path = self.state_path.with_suffix(".json.tmp")

        try:
            with temporary_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
                file.write("\n")

            temporary_path.replace(self.state_path)
            return True

        except OSError as error:
            print(f"저장하지 못했습니다: {error}")
            return False
