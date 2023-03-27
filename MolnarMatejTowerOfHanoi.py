import sys
from enum import Enum
import time
from memory_profiler import profile


class HEAP(Enum):
    ONE = 0
    TWO = 1
    THREE = 2


class HanoiGame:
    __num_of_movements = 0

    def __init__(self, number_of_disks: int):
        self.number_of_disks = number_of_disks
        heap_one = []
        heap_two = []
        heap_three = []

        for i in reversed(range(number_of_disks)):
            heap_one.append(i + 1)

        self.state = [heap_one, heap_two, heap_three]

    def move(self, from_heap: HEAP, to_heap: HEAP):
        try:
            take = self.state[from_heap.value][-1]
        except IndexError:
            print("FROM HEAP EMPTY")
            return

        look = sys.maxsize
        if len(self.state[to_heap.value]) > 0:
            look = self.state[to_heap.value][-1]

        if take < look:
            self.state[to_heap.value].append(self.state[from_heap.value].pop())
        else:
            print("UNSUPPORTED OPERATION")

        self.__num_of_movements = self.__num_of_movements + 1

    def print_state(self):
        print(self.state)

    def is_game_over(self):
        return self.number_of_disks == len(self.state[HEAP.THREE.value])

    def number_of_movements(self):
        return self.__num_of_movements


def manual_solve(game: HanoiGame):
    while not game.is_game_over():
        print("Trenutno stanje:")
        game.print_state()
        from_heap = int(input("Unesite broj gdje želite pomaknuti disk(1,2 ili 3):  ")) - 1
        to_heap = int(input("Unesite broj gdje želite pomaknuti disk(1,2 ili 3):")) - 1
        game.move(HEAP(from_heap), HEAP(to_heap))

    print("Bravo, riješili ste igricu u ", game.number_of_movements(), "poteza!")


def auto_solve(game: HanoiGame):
    solve_hanoi(game, game.number_of_disks, HEAP.ONE, HEAP.THREE, HEAP.TWO)
    print("Igrica je riješena u ", game.number_of_movements(), "poteza.")
    game.print_state()


def solve_hanoi(game: HanoiGame, n: int, from_heap: HEAP, to_heap: HEAP, aux_heap: HEAP):
    if n == 1:
        game.move(from_heap, to_heap)
    else:
        solve_hanoi(game, n - 1, from_heap, aux_heap, to_heap)
        game.move(from_heap, to_heap)
        solve_hanoi(game, n - 1, aux_heap, to_heap, from_heap)

@profile
def main():
    while True:
        print("Dobro dosli u Tower of Hanoi game!")
        num_disks = int(input("Unesite broj diskova (ili 0 za izlaz iz programa): "))

        if num_disks == 0:
            print("Dovidenja!")
            break

        game = HanoiGame(num_disks)

        while True:
            choice = input("Unesite 'm' za ručno rješavanje, 'a' za automatsko rješavanje ili 'q' za izlaz iz programa: ")

            if choice == 'm':
                manual_solve(game)
                break
            elif choice == 'a':
                auto_solve(game)
                break
            elif choice == 'q':
                print("Dovidenja!")
                sys.exit(0)

if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print("Execution time:", end_time - start_time, "seconds")
