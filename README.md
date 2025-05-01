# Belief Revision Agent

This project implements a belief revision agent based on the AGM postulates. The agent can represent a belief base, check logical entailment using resolution, contract beliefs, and expand beliefs.

## Table of Contents

- [Overview](#overview)
- [Files](#files)
- [Installation](#installation)
- [Usage](#usage)
  - [Interactive Mode](#interactive-mode)
  - [Example Scripts](#example-scripts)
  - [Formula Syntax](#formula-syntax)
- [Implementation Details](#implementation-details)
  - [Belief Base](#belief-base)
  - [Contraction](#contraction)
  - [Expansion](#expansion)
  - [Revision](#revision)
  - [Resolution](#resolution)
- [AGM Postulates](#agm-postulates)
- [Requirements](#requirements)

## Overview

The belief revision agent is implemented in Python and consists of the following components:

1. **Propositional Logic Representation**: Classes for representing propositional logic formulas, including atoms, negation, conjunction, disjunction, implication, and biconditional.
2. **CNF Conversion**: Methods for converting propositional formulas to Conjunctive Normal Form (CNF).
3. **Resolution Algorithm**: Implementation of the resolution algorithm for checking logical entailment.
4. **Belief Base**: A class for representing a belief base consisting of propositional formulas with priorities.
5. **Belief Revision Operations**: Implementation of contraction, expansion, and revision operations based on the AGM postulates.
6. **Formula Parser**: A parser for propositional logic formulas that allows users to input formulas in a more user-friendly way.

## Files

- `belief_revision_agent.py`: Contains the main implementation of the belief revision agent, including classes for propositional logic formulas, the belief base, and the formula parser.
- `resolution.py`: Implements the resolution algorithm for checking logical entailment.
- `main.py`: Provides an interactive interface for using the belief revision agent.
- `example.py`: A simple example demonstrating the belief revision agent with the classic "birds fly, penguins are birds, penguins don't fly" scenario.
- `comprehensive_example.py`: A more comprehensive example demonstrating the belief revision agent's capabilities with a weather scenario.

## Installation

No special installation is required beyond having Python 3.6 or higher. Simply clone or download the repository to your local machine.

## Usage

### Interactive Mode

The `main.py` script provides an interactive mode that allows you to interact with the belief revision agent through a command-line interface. To start the interactive mode, run:

```bash
python main.py
```

Once in interactive mode, you can use the following commands:

- `add <formula> <priority>`: Add a formula to the belief base with the specified priority
- `remove <formula>`: Remove a formula from the belief base
- `entails <formula>`: Check if the belief base entails a formula
- `contract <formula>`: Contract the belief base with a formula
- `expand <formula> <priority>`: Expand the belief base with a formula
- `revise <formula> <priority>`: Revise the belief base with a formula
- `show`: Show the current belief base
- `clear`: Clear the belief base
- `q`: Quit
- `h`: Help

Example commands:
```
add a -> b 1
add b -> c 2
add a 3
entails c
revise !a 4
show
```

### Example Scripts

The repository includes two example scripts that demonstrate how to use the belief revision agent:

1. **Simple Example** (`example.py`): Demonstrates the belief revision agent with the classic "birds fly, penguins are birds, penguins don't fly" scenario.

   Run it with:
   ```bash
   python example.py
   ```

2. **Comprehensive Example** (`comprehensive_example.py`): Demonstrates the belief revision agent's capabilities with a weather scenario, showing how beliefs can be added, checked for entailment, revised, and contracted.

   Run it with:
   ```bash
   python comprehensive_example.py
   ```

### Programmatic Usage

You can also use the belief revision agent programmatically in your own Python scripts:

```python
from belief_revision_agent import (
    Atom, Negation, Conjunction, Disjunction, Implication, Biconditional,
    BeliefBase, FormulaParser
)

# Create a parser for propositional logic formulas
parser = FormulaParser()

# Create a belief base
belief_base = BeliefBase()

# Add beliefs to the belief base
belief_base.add_belief(parser.parse("a -> b"), priority=1)
belief_base.add_belief(parser.parse("b -> c"), priority=2)
belief_base.add_belief(parser.parse("a"), priority=3)

# Check if the belief base entails a formula
entails = belief_base.entails(parser.parse("c"))
print(f"Does the belief base entail c? {entails}")

# Contract the belief base with a formula
belief_base.contract(parser.parse("c"))

# Expand the belief base with a formula
belief_base.expand(parser.parse("d"), priority=4)

# Revise the belief base with a formula
belief_base.revise(parser.parse("!a"), priority=5)
```

### Formula Syntax

The formula parser supports the following syntax:

- **Atoms**: Single letters or words (a, b, p, q, rain, etc.)
- **Negation**: !a, ~a, -a, ¬a
- **Conjunction**: a & b, a && b, a and b, a ∧ b
- **Disjunction**: a | b, a || b, a or b, a ∨ b
- **Implication**: a -> b, a => b, a implies b, a → b
- **Biconditional**: a <-> b, a <=> b, a iff b, a ↔ b
- **Parentheses for grouping**: (a & b) | c

Example formulas:
- `p & (q | !r) -> s`
- `rain -> wet`
- `penguin -> bird`
- `penguin -> !fly`
- `wet <-> (rain | sprinkler)`

## Implementation Details

### Belief Base

The belief base is represented as a dictionary mapping formulas to their priorities. Higher priority values indicate more important beliefs. When conflicts arise during belief revision, higher priority beliefs are preferred over lower priority beliefs.

### Contraction

The contraction operation uses partial meet contraction based on priorities. It finds all maximal subsets of the belief base that do not entail the formula, and then selects the "best" subset based on priorities.

The implementation follows these steps:
1. Check if the formula is already not entailed (Vacuity)
2. Find all maximal subsets that do not entail the formula
3. Select the "best" subset based on priorities
4. Update the belief base with the selected subset

### Expansion

The expansion operation simply adds the formula to the belief base with the given priority. If the formula already exists in the belief base, its priority is updated.

### Revision

The revision operation follows the Levi identity: first contract with the negation of the formula, then expand with the formula. This ensures that the belief base remains consistent after revision.

The implementation follows these steps:
1. Contract with the negation of the formula
2. Expand with the formula

### Resolution

The resolution algorithm is used to check logical entailment. It converts all formulas to CNF, adds the negation of the query formula, and then applies the resolution rule until either the empty clause is derived (indicating that the query is entailed) or no new clauses can be derived (indicating that the query is not entailed).

The implementation follows these steps:
1. Convert all beliefs to CNF
2. Combine all clauses from the beliefs
3. Add the negation of the query formula
4. Apply resolution until either the empty clause is derived or no new clauses can be derived

## AGM Postulates

The belief revision operations implemented in this project follow the AGM postulates:

1. **Closure**: The result of a revision is a belief base.
2. **Success**: If the formula is not a tautology, it is not entailed by the contracted belief base.
3. **Inclusion**: The contracted belief base is a subset of the original.
4. **Vacuity**: If the formula is not entailed by the original belief base, the contracted belief base is the same.
5. **Extensionality**: If two formulas are logically equivalent, contracting by either gives the same result.
6. **Recovery**: The original belief base can be recovered by adding back the formula.

## Requirements

- Python 3.6 or higher
