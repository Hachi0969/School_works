import random
import string

# ==============================
# Problem Configuration
# ==============================

# Target password we want to crack
TARGET = "Hi+My-Name-harry"

# Length of chromosome (fixed)
PASSWORD_LENGTH = len(TARGET)

# Allowed character set (A-Z, a-z, 0-9, +, -)
CHAR_SET = string.ascii_letters + string.digits + "+-"


# ==============================
# Create Chromosome and Population
# ==============================

def create_chromosome():
    """
    Create a random chromosome (candidate password).
    Each gene is randomly selected from CHAR_SET.
    """
    return ''.join(random.choice(CHAR_SET) for _ in range(PASSWORD_LENGTH))


def create_population(size):
    """
    Generate initial population of given size.
    """
    return [create_chromosome() for _ in range(size)]


# ==============================
# Fitness Function (with caching)
# ==============================

def calculate_fitness(population):
    """
    Calculate fitness for each chromosome once per generation.
    Fitness = number of matching characters at correct position.
    Store results in a dictionary (fitness cache).
    """
    fitness_cache = {}

    for chromosome in population:
        score = 0
        for i in range(PASSWORD_LENGTH):
            if chromosome[i] == TARGET[i]:
                score += 1
        fitness_cache[chromosome] = score

    return fitness_cache


# ==============================
# Roulette Wheel Selection
# ==============================

def select_parent(population, fitness_cache):
    """
    Select one parent using Roulette Wheel Selection.
    Probability of selection is proportional to fitness.
    """
    total_fitness = sum(fitness_cache.values())

    # If all fitness values are zero, choose randomly
    if total_fitness == 0:
        return random.choice(population)

    pick = random.uniform(0, total_fitness)
    current = 0

    for individual in population:
        current += fitness_cache[individual]
        if current >= pick:
            return individual


# ==============================
# Crossover (Single Point)
# ==============================

def crossover(parent1, parent2):
    """
    Perform single-point crossover.
    Randomly choose a cut position and swap tails.
    """
    cut = random.randint(1, PASSWORD_LENGTH - 1)

    child1 = parent1[:cut] + parent2[cut:]
    child2 = parent2[:cut] + parent1[cut:]

    return child1, child2


# ==============================
# Mutation (Improved Version)
# ==============================

def mutate(chromosome, mutation_rate=0.01):
    """
    Mutation: each gene has a small probability to change.
    Improved by modifying a list instead of string concatenation.
    """
    chromosome = list(chromosome)  # Convert string to list for easy modification

    for i in range(PASSWORD_LENGTH):
        if random.random() < mutation_rate:
            chromosome[i] = random.choice(CHAR_SET)

    return ''.join(chromosome)  # Convert back to string


# ==============================
# Main Genetic Algorithm Process
# ==============================

if __name__ == "__main__":

    POP_SIZE = 100
    MAX_GENERATIONS = 1000

    # Step 1: Initialize population
    population = create_population(POP_SIZE)

    # Step 2: Evolution process
    for generation in range(1, MAX_GENERATIONS + 1):

        # Step 3: Calculate fitness once (fitness caching)
        fitness_cache = calculate_fitness(population)

        # Step 4: Sort population by fitness (highest first)
        population = sorted(
            population,
            key=lambda x: fitness_cache[x],
            reverse=True
        )

        best = population[0]
        best_fitness = fitness_cache[best]

        # Show first 5 generations and final generation
        if generation <= 5 or best_fitness == PASSWORD_LENGTH:
            print(f"Generation {generation}:")
            print("Best:", best)
            print("Fitness:", best_fitness)
            print("-" * 40)

        # Step 5: Stop if password is cracked
        if best_fitness == PASSWORD_LENGTH:
            print("Password cracked successfully!")
            break

        # Step 6: Create new generation
        new_population = []

        while len(new_population) < POP_SIZE:

            # Select parents using roulette wheel
            parent1 = select_parent(population, fitness_cache)
            parent2 = select_parent(population, fitness_cache)

            # Apply crossover
            child1, child2 = crossover(parent1, parent2)

            # Apply mutation
            child1 = mutate(child1)
            child2 = mutate(child2)

            new_population.append(child1)
            new_population.append(child2)

        # Replace old population
        population = new_population[:POP_SIZE]