"""실행: python3 benchmark.py — 실제 state.json은 변경하지 않습니다."""

import io
import platform
import tempfile
import tracemalloc
from contextlib import redirect_stdout
from pathlib import Path
from time import perf_counter

from data import create_default_quizzes
from game import QuizGame
from quiz import Quiz


def main():
    original_path = Path(__file__).resolve().parent / "state.json"
    original = original_path.read_bytes() if original_path.exists() else None

    print("Python:", platform.python_version())
    print("측정 대상: 합성 퀴즈 1,000개")
    print("시간은 단일 실행 측정값이며 환경에 따라 달라집니다.")

    with tempfile.TemporaryDirectory() as folder:
        with redirect_stdout(io.StringIO()):
            game = QuizGame()

        game.state_path = Path(folder) / "state.json"
        game.save_enabled = True
        base = create_default_quizzes()

        tracemalloc.start()
        start = perf_counter()
        game.quizzes = [
            Quiz(
                f"[측정용 {number}] {base[number % len(base)].question}",
                base[number % len(base)].choices,
                base[number % len(base)].answer,
            )
            for number in range(1000)
        ]
        creation_ms = (perf_counter() - start) * 1000
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"객체 1,000개 생성: {creation_ms:.3f} ms")
        print(f"생성 후 추적 메모리: {current / 1024:.1f} KiB")
        print(f"생성 중 최대 추적 메모리: {peak / 1024:.1f} KiB")

        start = perf_counter()
        assert game.save_state()
        print(f"JSON 저장: {(perf_counter() - start) * 1000:.3f} ms")
        print(f"JSON 파일 크기: {game.state_path.stat().st_size:,} bytes")

        game.quizzes = []
        tracemalloc.start()
        start = perf_counter()
        with redirect_stdout(io.StringIO()):
            game.load_state()
        loading_ms = (perf_counter() - start) * 1000
        _, loading_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        assert len(game.quizzes) == 1000

        print(f"JSON 불러오기·검증·객체 복원: {loading_ms:.3f} ms")
        print(f"불러오기 중 최대 추적 메모리: {loading_peak / 1024:.1f} KiB")

        start = perf_counter()
        for _ in range(1000):
            matches = [
                quiz for quiz in game.quizzes
                if "[측정용 999]" in quiz.question
            ]
        search_ms = (perf_counter() - start) * 1000 / 1000
        assert len(matches) == 1
        print(f"선형 검색 1회 평균: {search_ms:.4f} ms (1,000회 반복)")

    after = original_path.read_bytes() if original_path.exists() else None
    assert after == original
    print("PASS: 실제 state.json 원본 유지")
    print("성능 측정 완료")


if __name__ == "__main__":
    main()
