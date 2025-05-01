"""
Belief Revision Agent Demo

This script demonstrates how to use the belief revision agent.
"""

from belief_revision_agent import (
    Atom, Negation, Conjunction, Disjunction, Implication, Biconditional,
    BeliefBase, FormulaParser
)

def print_separator():
    """Print a separator line."""
    print("\n" + "=" * 50 + "\n")

def main():
    """Main function to demonstrate the belief revision agent."""
    print("Belief Revision Agent Demo")
    print_separator()
    
    # Create a parser for propositional logic formulas
    parser = FormulaParser()
    
    # Create a belief base
    belief_base = BeliefBase()
    
    # Example from the slides: Robert does well in the exam if and only if he is prepared or lucky
    print("Example from the slides:")
    print("Robert does well in the exam if and only if he is prepared or lucky.")
    print("Robert does not do well in the exam.")
    print("Query: Robert is not prepared.")
    print_separator()
    
    # Define the atoms
    r = Atom("r")  # Robert does well in the exam
    p = Atom("p")  # Robert is prepared
    s = Atom("s")  # Robert is lucky
    
    # Define the formulas
    # r ↔ (p ∨ s)
    formula1 = Biconditional(r, Disjunction(p, s))
    # ¬r
    formula2 = Negation(r)
    # Query: ¬p
    query = Negation(p)
    
    # Add the formulas to the belief base
    belief_base.add_belief(formula1, priority=2)
    belief_base.add_belief(formula2, priority=1)
    
    # Print the belief base
    print("Initial Belief Base:")
    print(belief_base)
    print_separator()
    
    # Check if the belief base entails the query
    entails = belief_base.entails(query)
    print(f"Does the belief base entail {query}? {entails}")
    print_separator()
    
    # Demonstrate contraction
    print("Contracting the belief base with ¬p:")
    belief_base.contract(query)
    print("Belief Base after contraction:")
    print(belief_base)
    print_separator()
    
    # Demonstrate expansion
    print("Expanding the belief base with ¬p:")
    belief_base.expand(query, priority=3)
    print("Belief Base after expansion:")
    print(belief_base)
    print_separator()
    
    # Demonstrate revision
    print("Revising the belief base with p:")
    belief_base.revise(p, priority=4)
    print("Belief Base after revision:")
    print(belief_base)
    print_separator()
    
    # Demonstrate the parser
    print("Using the parser to create formulas:")
    formula_str = "r <-> (p | s)"
    formula = parser.parse(formula_str)
    print(f"Parsed formula: {formula}")
    print(f"Original string: {formula_str}")
    print_separator()
    
    # Create a new belief base using the parser
    print("Creating a new belief base using the parser:")
    new_belief_base = BeliefBase()
    
    # Debug the parser
    print("Parsing 'a -> b'...")
    formula1 = parser.parse("a -> b")
    print(f"Parsed formula1: {formula1}")
    
    print("Parsing 'b -> c'...")
    formula2 = parser.parse("b -> c")
    print(f"Parsed formula2: {formula2}")
    
    print("Parsing 'a'...")
    formula3 = parser.parse("a")
    print(f"Parsed formula3: {formula3}")
    
    # Add the formulas to the belief base
    new_belief_base.add_belief(formula1, priority=1)
    new_belief_base.add_belief(formula2, priority=2)
    new_belief_base.add_belief(formula3, priority=3)
    print(new_belief_base)
    print_separator()
    
    # Check if the new belief base entails c
    query = parser.parse("c")
    entails = new_belief_base.entails(query)
    print(f"Does the new belief base entail {query}? {entails}")
    print_separator()
    
    # Interactive mode
    print("Interactive Mode")
    print("Enter 'q' to quit.")
    
    interactive_belief_base = BeliefBase()
    
    while True:
        command = input("\nEnter command: ").strip()
        
        if command.lower() == 'q':
            break
        elif command.lower() == 'show':
            print("\nCurrent Belief Base:")
            print(interactive_belief_base)
        elif command.lower() == 'clear':
            interactive_belief_base = BeliefBase()
            print("\nBelief base cleared.")
        elif command.lower().startswith('add '):
            try:
                parts = command[4:].strip().split(' ')
                if len(parts) >= 2:
                    formula_str = ' '.join(parts[:-1])
                    priority = int(parts[-1])
                    formula = parser.parse(formula_str)
                    interactive_belief_base.add_belief(formula, priority)
                    print(f"\nAdded formula: {formula} with priority {priority}")
                else:
                    print("\nInvalid command. Use 'add <formula> <priority>'")
            except Exception as e:
                print(f"\nError: {e}")
        elif command.lower().startswith('remove '):
            try:
                formula_str = command[7:].strip()
                formula = parser.parse(formula_str)
                interactive_belief_base.remove_belief(formula)
                print(f"\nRemoved formula: {formula}")
            except Exception as e:
                print(f"\nError: {e}")
        elif command.lower().startswith('entails '):
            try:
                formula_str = command[8:].strip()
                formula = parser.parse(formula_str)
                entails = interactive_belief_base.entails(formula)
                print(f"\nDoes the belief base entail {formula}? {entails}")
            except Exception as e:
                print(f"\nError: {e}")
        elif command.lower().startswith('contract '):
            try:
                formula_str = command[9:].strip()
                formula = parser.parse(formula_str)
                interactive_belief_base.contract(formula)
                print(f"\nContracted with formula: {formula}")
            except Exception as e:
                print(f"\nError: {e}")
        elif command.lower().startswith('expand '):
            try:
                parts = command[7:].strip().split(' ')
                if len(parts) >= 2:
                    formula_str = ' '.join(parts[:-1])
                    priority = int(parts[-1])
                    formula = parser.parse(formula_str)
                    interactive_belief_base.expand(formula, priority)
                    print(f"\nExpanded with formula: {formula} with priority {priority}")
                else:
                    print("\nInvalid command. Use 'expand <formula> <priority>'")
            except Exception as e:
                print(f"\nError: {e}")
        elif command.lower().startswith('revise '):
            try:
                parts = command[7:].strip().split(' ')
                if len(parts) >= 2:
                    formula_str = ' '.join(parts[:-1])
                    priority = int(parts[-1])
                    formula = parser.parse(formula_str)
                    interactive_belief_base.revise(formula, priority)
                    print(f"\nRevised with formula: {formula} with priority {priority}")
                else:
                    print("\nInvalid command. Use 'revise <formula> <priority>'")
            except Exception as e:
                print(f"\nError: {e}")
        else:
            print("\nUnknown command. Available commands:")
            print("  add <formula> <priority>, remove <formula>, entails <formula>")
            print("  contract <formula>, expand <formula> <priority>, revise <formula> <priority>")
            print("  show, clear, q")

if __name__ == "__main__":
    main()
