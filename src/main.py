import click

from src.input.nvidia_input import NvidiaInput
from src.model.basic_tour import BasicTour
from src.model.nvidia_solution import NvidiaSolution
from src.algorithm.solver import Solver

@click.command()
@click.argument("input_file")
@click.argument("output_file")
def main(input_file, output_file):
    # currently assumes nvidia input format
    # later we might add support for other formats
    input = NvidiaInput.from_file(input_file)
    solver = Solver(input, BasicTour)
    solver.solve()
    solution = solver.get_solution()
    nvidia_solution = NvidiaSolution(solution, input_file)
    nvidia_solution.write(output_file)
    

if __name__ == "__main__":
    main()
