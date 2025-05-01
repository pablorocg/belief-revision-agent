"""
Comprehensive Belief Revision Agent Example

This script demonstrates the belief revision agent's capabilities with a more comprehensive example.
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
    print("Comprehensive Belief Revision Agent Example")
    print_separator()
    
    # Create a parser for propositional logic formulas
    parser = FormulaParser()
    
    # Create a belief base
    belief_base = BeliefBase()
    
    # Example: Weather forecast
    print("Example: Weather forecast")
    print("Initial beliefs:")
    print("1. If it rains, the ground will be wet.")
    print("2. If the sprinkler is on, the ground will be wet.")
    print("3. It is not raining.")
    print_separator()
    
    # Define the formulas
    rain_wet = parser.parse("rain -> wet")  # If it rains, the ground will be wet
    sprinkler_wet = parser.parse("sprinkler -> wet")  # If the sprinkler is on, the ground will be wet
    not_rain = parser.parse("!rain")  # It is not raining
    
    # Add the formulas to the belief base with different priorities
    belief_base.add_belief(rain_wet, priority=3)
    belief_base.add_belief(sprinkler_wet, priority=2)
    belief_base.add_belief(not_rain, priority=1)
    
    # Print the belief base
    print("Initial Belief Base:")
    print(belief_base)
    print_separator()
    
    # Check if the belief base entails that the ground is wet
    entails_wet = belief_base.entails(parser.parse("wet"))
    print(f"Does the belief base entail 'wet'? {entails_wet}")
    print("(The ground is not necessarily wet because we don't know if the sprinkler is on.)")
    print_separator()
    
    # Now let's add a new belief: The ground is wet
    print("Adding new belief: 'wet'")
    belief_base.add_belief(parser.parse("wet"), priority=4)
    
    # Print the belief base
    print("Belief Base after adding 'wet':")
    print(belief_base)
    print_separator()
    
    # Check if the belief base entails that the sprinkler is on
    entails_sprinkler = belief_base.entails(parser.parse("sprinkler"))
    print(f"Does the belief base entail 'sprinkler'? {entails_sprinkler}")
    print("(The sprinkler is not necessarily on because the ground could be wet for other reasons.)")
    print_separator()
    
    # Now let's add a new belief: If the ground is wet, then either it is raining or the sprinkler is on
    print("Adding new belief: 'wet -> (rain | sprinkler)'")
    belief_base.add_belief(parser.parse("wet -> (rain | sprinkler)"), priority=5)
    
    # Print the belief base
    print("Belief Base after adding 'wet -> (rain | sprinkler)':")
    print(belief_base)
    print_separator()
    
    # Check if the belief base entails that the sprinkler is on
    entails_sprinkler = belief_base.entails(parser.parse("sprinkler"))
    print(f"Does the belief base entail 'sprinkler'? {entails_sprinkler}")
    print("(Now the sprinkler must be on because the ground is wet, it's not raining, and the only way the ground can be wet is if it's raining or the sprinkler is on.)")
    print_separator()
    
    # Now let's revise the belief base with a new belief: It is raining
    print("Revising belief base with 'rain'")
    belief_base.revise(parser.parse("rain"), priority=6)
    
    # Print the belief base after revision
    print("Belief Base after revision with 'rain':")
    print(belief_base)
    print_separator()
    
    # Check if the belief base still entails that the ground is wet
    entails_wet = belief_base.entails(parser.parse("wet"))
    print(f"Does the belief base entail 'wet'? {entails_wet}")
    print("(The ground is still wet because if it's raining, the ground is wet.)")
    
    # Check if the belief base still entails that the sprinkler is on
    entails_sprinkler = belief_base.entails(parser.parse("sprinkler"))
    print(f"Does the belief base entail 'sprinkler'? {entails_sprinkler}")
    print("(The sprinkler is no longer necessarily on because the ground being wet can now be explained by the rain.)")
    print_separator()
    
    # Now let's contract the belief base with 'wet'
    print("Contracting belief base with 'wet'")
    belief_base.contract(parser.parse("wet"))
    
    # Print the belief base after contraction
    print("Belief Base after contraction with 'wet':")
    print(belief_base)
    print_separator()
    
    # Check if the belief base still entails that the ground is wet
    entails_wet = belief_base.entails(parser.parse("wet"))
    print(f"Does the belief base entail 'wet'? {entails_wet}")
    print("(After contraction, the belief base should no longer entail that the ground is wet.)")
    print_separator()

if __name__ == "__main__":
    main()
