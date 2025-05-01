"""
Belief Revision Agent Example

This script demonstrates how to use the belief revision agent with a simple example.
"""

from belief_revision_agent import (
    Atom, Negation, Conjunction, Disjunction, Implication, Biconditional,
    BeliefBase, FormulaParser
)

def main():
    """Main function to demonstrate the belief revision agent."""
    print("Belief Revision Agent Example")
    print("-" * 50)
    
    # Create a parser for propositional logic formulas
    parser = FormulaParser()
    
    # Create a belief base
    belief_base = BeliefBase()
    
    # Example: Birds fly, penguins are birds, penguins don't fly
    print("Example: Birds fly, penguins are birds, penguins don't fly")
    print("-" * 50)
    
    # Define the formulas
    bird_fly = parser.parse("bird -> fly")  # Birds fly
    penguin_bird = parser.parse("penguin -> bird")  # Penguins are birds
    penguin_not_fly = parser.parse("penguin -> !fly")  # Penguins don't fly
    
    # Add the formulas to the belief base with different priorities
    belief_base.add_belief(bird_fly, priority=1)  # Lowest priority
    belief_base.add_belief(penguin_bird, priority=2)
    belief_base.add_belief(penguin_not_fly, priority=3)  # Highest priority
    
    # Print the belief base
    print("Initial Belief Base:")
    print(belief_base)
    print("-" * 50)
    
    # Check if the belief base entails that birds fly
    entails_bird_fly = belief_base.entails(parser.parse("bird -> fly"))
    print(f"Does the belief base entail 'bird -> fly'? {entails_bird_fly}")
    
    # Check if the belief base entails that penguins fly
    entails_penguin_fly = belief_base.entails(parser.parse("penguin -> fly"))
    print(f"Does the belief base entail 'penguin -> fly'? {entails_penguin_fly}")
    
    # Check if the belief base entails that penguins don't fly
    entails_penguin_not_fly = belief_base.entails(parser.parse("penguin -> !fly"))
    print(f"Does the belief base entail 'penguin -> !fly'? {entails_penguin_not_fly}")
    print("-" * 50)
    
    # Now let's add a new belief: Tweety is a penguin
    print("Adding new belief: 'tweety -> penguin'")
    belief_base.add_belief(parser.parse("tweety -> penguin"), priority=4)
    
    # Check if the belief base entails that Tweety is a bird
    entails_tweety_bird = belief_base.entails(parser.parse("tweety -> bird"))
    print(f"Does the belief base entail 'tweety -> bird'? {entails_tweety_bird}")
    
    # Check if the belief base entails that Tweety flies
    entails_tweety_fly = belief_base.entails(parser.parse("tweety -> fly"))
    print(f"Does the belief base entail 'tweety -> fly'? {entails_tweety_fly}")
    
    # Check if the belief base entails that Tweety doesn't fly
    entails_tweety_not_fly = belief_base.entails(parser.parse("tweety -> !fly"))
    print(f"Does the belief base entail 'tweety -> !fly'? {entails_tweety_not_fly}")
    print("-" * 50)
    
    # Now let's revise the belief base with a new belief: Tweety flies
    print("Revising belief base with 'tweety -> fly'")
    belief_base.revise(parser.parse("tweety -> fly"), priority=5)
    
    # Print the belief base after revision
    print("Belief Base after revision:")
    print(belief_base)
    print("-" * 50)
    
    # Check if the belief base still entails that Tweety is a penguin
    entails_tweety_penguin = belief_base.entails(parser.parse("tweety -> penguin"))
    print(f"Does the belief base entail 'tweety -> penguin'? {entails_tweety_penguin}")
    
    # Check if the belief base still entails that Tweety is a bird
    entails_tweety_bird = belief_base.entails(parser.parse("tweety -> bird"))
    print(f"Does the belief base entail 'tweety -> bird'? {entails_tweety_bird}")
    
    # Check if the belief base entails that Tweety flies
    entails_tweety_fly = belief_base.entails(parser.parse("tweety -> fly"))
    print(f"Does the belief base entail 'tweety -> fly'? {entails_tweety_fly}")
    print("-" * 50)

if __name__ == "__main__":
    main()
