"""
Resolution Algorithm for Propositional Logic

This module implements the resolution algorithm for checking logical entailment
in propositional logic.
"""

from belief_revision_agent import Literal, Clause, CNF


def resolve(clause1, clause2):
    """
    Attempt to resolve two clauses.
    Returns a list of all possible resolvents (could be empty if no resolution is possible).
    """
    resolvents = []
    
    # Try to find complementary literals
    for lit1 in clause1.literals:
        for lit2 in clause2.literals:
            if lit1.name == lit2.name and lit1.negated != lit2.negated:
                # Found complementary literals, create a resolvent
                resolvent_literals = set()
                
                # Add all literals from clause1 except lit1
                for l in clause1.literals:
                    if l != lit1:
                        resolvent_literals.add(l)
                
                # Add all literals from clause2 except lit2
                for l in clause2.literals:
                    if l != lit2:
                        resolvent_literals.add(l)
                
                # Create the resolvent clause
                resolvent = Clause(resolvent_literals)
                
                # Skip tautologies
                if not resolvent.is_tautology():
                    resolvents.append(resolvent)
    
    return resolvents


def resolution(clauses):
    """
    Apply the resolution algorithm to check if a set of clauses is unsatisfiable.
    Returns True if the clauses are unsatisfiable (meaning the original formula is entailed).
    """
    # Make a copy of the clauses to avoid modifying the original set
    clauses = set(clauses)
    
    # Keep track of new clauses added in each iteration
    new_clauses = set(clauses)
    
    while True:
        # Pairs of clauses to resolve
        pairs = [(c1, c2) for c1 in clauses for c2 in new_clauses if c1 != c2]
        new_clauses = set()
        
        for c1, c2 in pairs:
            resolvents = resolve(c1, c2)
            
            # Check if we derived the empty clause (contradiction)
            for resolvent in resolvents:
                if resolvent.is_empty():
                    return True  # Unsatisfiable
                
                # Add the resolvent if it's not already in the set of clauses
                if resolvent not in clauses:
                    new_clauses.add(resolvent)
        
        # If no new clauses were added, we're done
        if not new_clauses or new_clauses.issubset(clauses):
            return False  # Satisfiable
        
        # Add the new clauses to the set of all clauses
        clauses.update(new_clauses)
