# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click",
#     "numpy",
# ]
# ///
import click
import numpy as np

@click.command()
@click.option('--count', '-n', default=10, show_default=True, help='Number of random numbers to generate.')
@click.option('--min', 'min_', default=0, show_default=True, help='Minimum value (inclusive for int, lower bound for float).')
@click.option('--max', 'max_', default=100, show_default=True, help='Maximum value (exclusive for int, upper bound for float).')
@click.option('--dtype', type=click.Choice(['int', 'float']), default='int', show_default=True, help='Type of random numbers to generate.')
def main(count, min_, max_, dtype):
    """Generate random numbers using numpy."""
    if dtype == 'int':
        numbers = np.random.randint(min_, max_, size=count)
    else:
        numbers = np.random.uniform(min_, max_, size=count)
    for num in numbers:
        print(num)

if __name__ == '__main__':
    main() 