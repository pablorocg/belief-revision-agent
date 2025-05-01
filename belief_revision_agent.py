"""
Belief Revision Agent

This module implements a belief revision agent based on the AGM postulates.
It includes functionality for:
- Representing a belief base
- Checking logical entailment using resolution
- Contracting beliefs
- Expanding beliefs
"""

class Literal:
    """
    Represents a literal in propositional logic (a variable or its negation).
    """
    def __init__(self, name, negated=False):
        self.name = name
        self.negated = negated
        
    def negate(self):
        """Returns a new literal with the opposite negation status."""
        return Literal(self.name, not self.negated)
    
    def __eq__(self, other):
        if not isinstance(other, Literal):
            return False
        return self.name == other.name and self.negated == other.negated
    
    def __hash__(self):
        return hash((self.name, self.negated))
    
    def __str__(self):
        return f"¬{self.name}" if self.negated else self.name
    
    def __repr__(self):
        return str(self)


class Clause:
    """
    Represents a clause (disjunction of literals) in propositional logic.
    """
    def __init__(self, literals=None):
        self.literals = set(literals) if literals else set()
        
    def add_literal(self, literal):
        """Add a literal to the clause."""
        self.literals.add(literal)
        
    def is_empty(self):
        """Check if the clause is empty (contradiction)."""
        return len(self.literals) == 0
    
    def is_tautology(self):
        """Check if the clause is a tautology (always true)."""
        for literal in self.literals:
            if literal.negate() in self.literals:
                return True
        return False
    
    def __eq__(self, other):
        if not isinstance(other, Clause):
            return False
        return self.literals == other.literals
    
    def __hash__(self):
        return hash(frozenset(self.literals))
    
    def __str__(self):
        if not self.literals:
            return "⊥"  # Empty clause (contradiction)
        return " ∨ ".join(str(lit) for lit in self.literals)
    
    def __repr__(self):
        return str(self)


class Formula:
    """
    Base class for propositional formulas.
    """
    def to_cnf(self):
        """Convert the formula to Conjunctive Normal Form (CNF)."""
        raise NotImplementedError("Subclasses must implement to_cnf()")
    
    def __eq__(self, other):
        raise NotImplementedError("Subclasses must implement __eq__()")
    
    def __hash__(self):
        raise NotImplementedError("Subclasses must implement __hash__()")


class Atom(Formula):
    """
    Represents an atomic proposition.
    """
    def __init__(self, name):
        self.name = name
        
    def to_cnf(self):
        """Convert the atom to CNF."""
        literal = Literal(self.name)
        return CNF([Clause([literal])])
    
    def __eq__(self, other):
        if not isinstance(other, Atom):
            return False
        return self.name == other.name
    
    def __hash__(self):
        return hash(("atom", self.name))
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)


class Negation(Formula):
    """
    Represents the negation of a formula.
    """
    def __init__(self, formula):
        self.formula = formula
        
    def to_cnf(self):
        """Convert the negation to CNF."""
        # Handle special cases for efficient conversion
        if isinstance(self.formula, Atom):
            literal = Literal(self.formula.name, True)
            return CNF([Clause([literal])])
        elif isinstance(self.formula, Negation):
            # Double negation elimination
            return self.formula.formula.to_cnf()
        
        # For complex formulas, we need to apply De Morgan's laws and other transformations
        # This is a simplified implementation
        if isinstance(self.formula, Conjunction):
            # ¬(A ∧ B) ≡ ¬A ∨ ¬B
            return Disjunction(Negation(self.formula.left), Negation(self.formula.right)).to_cnf()
        elif isinstance(self.formula, Disjunction):
            # ¬(A ∨ B) ≡ ¬A ∧ ¬B
            return Conjunction(Negation(self.formula.left), Negation(self.formula.right)).to_cnf()
        elif isinstance(self.formula, Implication):
            # ¬(A → B) ≡ A ∧ ¬B
            return Conjunction(self.formula.antecedent, Negation(self.formula.consequent)).to_cnf()
        elif isinstance(self.formula, Biconditional):
            # ¬(A ↔ B) ≡ (A ∧ ¬B) ∨ (¬A ∧ B)
            left = Conjunction(self.formula.left, Negation(self.formula.right))
            right = Conjunction(Negation(self.formula.left), self.formula.right)
            return Disjunction(left, right).to_cnf()
        
        # Default case (should not reach here if all formula types are handled)
        raise ValueError(f"Cannot convert negation of {type(self.formula)} to CNF")
    
    def __eq__(self, other):
        if not isinstance(other, Negation):
            return False
        return self.formula == other.formula
    
    def __hash__(self):
        return hash(("neg", hash(self.formula)))
    
    def __str__(self):
        return f"¬({self.formula})"
    
    def __repr__(self):
        return str(self)


class Conjunction(Formula):
    """
    Represents a conjunction of two formulas.
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def to_cnf(self):
        """Convert the conjunction to CNF."""
        left_cnf = self.left.to_cnf()
        right_cnf = self.right.to_cnf()
        
        # Combine the clauses from both sides
        return CNF(left_cnf.clauses.union(right_cnf.clauses))
    
    def __eq__(self, other):
        if not isinstance(other, Conjunction):
            return False
        return (self.left == other.left and self.right == other.right) or \
               (self.left == other.right and self.right == other.left)
    
    def __hash__(self):
        # Ensure commutativity in hash
        return hash(("conj", frozenset([hash(self.left), hash(self.right)])))
    
    def __str__(self):
        return f"({self.left} ∧ {self.right})"
    
    def __repr__(self):
        return str(self)


class Disjunction(Formula):
    """
    Represents a disjunction of two formulas.
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def to_cnf(self):
        """Convert the disjunction to CNF."""
        left_cnf = self.left.to_cnf()
        right_cnf = self.right.to_cnf()
        
        # Apply distributive law: (A ∨ B) ∧ (C ∨ D) ≡ (A ∨ C) ∧ (A ∨ D) ∧ (B ∨ C) ∧ (B ∨ D)
        new_clauses = set()
        for left_clause in left_cnf.clauses:
            for right_clause in right_cnf.clauses:
                # Create a new clause with literals from both sides
                new_clause = Clause(left_clause.literals.union(right_clause.literals))
                if not new_clause.is_tautology():  # Skip tautologies
                    new_clauses.add(new_clause)
        
        return CNF(new_clauses)
    
    def __eq__(self, other):
        if not isinstance(other, Disjunction):
            return False
        return (self.left == other.left and self.right == other.right) or \
               (self.left == other.right and self.right == other.left)
    
    def __hash__(self):
        # Ensure commutativity in hash
        return hash(("disj", frozenset([hash(self.left), hash(self.right)])))
    
    def __str__(self):
        return f"({self.left} ∨ {self.right})"
    
    def __repr__(self):
        return str(self)


class Implication(Formula):
    """
    Represents an implication between two formulas.
    """
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent
        
    def to_cnf(self):
        """Convert the implication to CNF."""
        # A → B ≡ ¬A ∨ B
        return Disjunction(Negation(self.antecedent), self.consequent).to_cnf()
    
    def __eq__(self, other):
        if not isinstance(other, Implication):
            return False
        return self.antecedent == other.antecedent and self.consequent == other.consequent
    
    def __hash__(self):
        return hash(("impl", hash(self.antecedent), hash(self.consequent)))
    
    def __str__(self):
        return f"({self.antecedent} → {self.consequent})"
    
    def __repr__(self):
        return str(self)


class Biconditional(Formula):
    """
    Represents a biconditional between two formulas.
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def to_cnf(self):
        """Convert the biconditional to CNF."""
        # A ↔ B ≡ (A → B) ∧ (B → A) ≡ (¬A ∨ B) ∧ (¬B ∨ A)
        left_to_right = Implication(self.left, self.right)
        right_to_left = Implication(self.right, self.left)
        return Conjunction(left_to_right, right_to_left).to_cnf()
    
    def __eq__(self, other):
        if not isinstance(other, Biconditional):
            return False
        return (self.left == other.left and self.right == other.right) or \
               (self.left == other.right and self.right == other.left)
    
    def __hash__(self):
        # Ensure commutativity in hash
        return hash(("bicon", frozenset([hash(self.left), hash(self.right)])))
    
    def __str__(self):
        return f"({self.left} ↔ {self.right})"
    
    def __repr__(self):
        return str(self)


class CNF:
    """
    Represents a formula in Conjunctive Normal Form (CNF).
    """
    def __init__(self, clauses=None):
        self.clauses = set(clauses) if clauses else set()
        
    def add_clause(self, clause):
        """Add a clause to the CNF formula."""
        if not clause.is_tautology():  # Skip tautologies
            self.clauses.add(clause)
        
    def is_satisfiable(self):
        """Check if the CNF formula is satisfiable using resolution."""
        # Implementation of resolution algorithm will be added later
        pass
    
    def __str__(self):
        if not self.clauses:
            return "⊤"  # Empty CNF (tautology)
        return " ∧ ".join(f"({clause})" for clause in self.clauses)
    
    def __repr__(self):
        return str(self)


class BeliefBase:
    """
    Represents a belief base consisting of propositional formulas with priorities.
    """
    def __init__(self):
        # Dictionary mapping formulas to their priorities (higher number = higher priority)
        self.beliefs = {}
        
    def add_belief(self, formula, priority=1):
        """Add a belief to the belief base with a given priority."""
        self.beliefs[formula] = priority
        
    def remove_belief(self, formula):
        """Remove a belief from the belief base."""
        if formula in self.beliefs:
            del self.beliefs[formula]
            
    def get_beliefs(self):
        """Get all beliefs in the belief base."""
        return list(self.beliefs.keys())
    
    def get_priority(self, formula):
        """Get the priority of a belief."""
        return self.beliefs.get(formula, 0)
    
    def entails(self, formula):
        """Check if the belief base entails a formula using resolution."""
        # Convert all beliefs to CNF
        belief_cnfs = [belief.to_cnf() for belief in self.beliefs]
        
        # Combine all clauses from the beliefs
        all_clauses = set()
        for cnf in belief_cnfs:
            all_clauses.update(cnf.clauses)
        
        # Add the negation of the formula to check for contradiction
        negated_formula = Negation(formula).to_cnf()
        all_clauses.update(negated_formula.clauses)
        
        # Apply resolution
        return self._resolution(all_clauses)
    
    def _resolution(self, clauses):
        """
        Apply the resolution algorithm to check if a set of clauses is unsatisfiable.
        Returns True if the clauses are unsatisfiable (meaning the original formula is entailed).
        """
        from resolution import resolution
        return resolution(clauses)
    
    def contract(self, formula):
        """
        Contract the belief base by removing the formula and any beliefs that entail it.
        Uses partial meet contraction based on priorities.
        
        The contraction operation follows the AGM postulates:
        1. Closure: The result is a belief base
        2. Success: If the formula is not a tautology, it is not entailed by the contracted belief base
        3. Inclusion: The contracted belief base is a subset of the original
        4. Vacuity: If the formula is not entailed by the original belief base, the contracted belief base is the same
        5. Extensionality: If two formulas are logically equivalent, contracting by either gives the same result
        6. Recovery: The original belief base can be recovered by adding back the formula
        """
        # Check if the formula is already not entailed (Vacuity)
        if not self.entails(formula):
            return
        
        # Find all maximal subsets that do not entail the formula
        maximal_subsets = self._find_maximal_non_entailing_subsets(formula)
        
        # If no such subsets exist, keep the belief base unchanged
        if not maximal_subsets:
            return
        
        # Perform partial meet contraction: select the "best" subsets based on priorities
        selected_subset = self._select_best_subset(maximal_subsets)
        
        # Update the belief base
        self.beliefs = selected_subset
    
    def _find_maximal_non_entailing_subsets(self, formula):
        """
        Find all maximal subsets of the belief base that do not entail the formula.
        """
        # Start with all possible subsets
        all_beliefs = list(self.beliefs.items())
        n = len(all_beliefs)
        
        # Generate all possible subsets
        subsets = []
        for i in range(2**n):
            subset = {}
            for j in range(n):
                if (i >> j) & 1:
                    subset[all_beliefs[j][0]] = all_beliefs[j][1]
            subsets.append(subset)
        
        # Filter out subsets that entail the formula
        non_entailing_subsets = []
        for subset in subsets:
            # Create a temporary belief base with the subset
            temp_bb = BeliefBase()
            temp_bb.beliefs = subset
            
            # Check if it entails the formula
            if not temp_bb.entails(formula):
                non_entailing_subsets.append(subset)
        
        # Find maximal subsets
        maximal_subsets = []
        for subset1 in non_entailing_subsets:
            is_maximal = True
            for subset2 in non_entailing_subsets:
                # If subset1 is a proper subset of subset2, it's not maximal
                if subset1 != subset2 and set(subset1.keys()).issubset(set(subset2.keys())):
                    is_maximal = False
                    break
            if is_maximal:
                maximal_subsets.append(subset1)
        
        return maximal_subsets
    
    def _select_best_subset(self, subsets):
        """
        Select the "best" subset based on priorities.
        The best subset is the one that retains the highest priority beliefs.
        """
        if not subsets:
            return {}
        
        # Calculate a score for each subset based on the priorities of the beliefs it contains
        subset_scores = []
        for subset in subsets:
            score = sum(priority for _, priority in subset.items())
            subset_scores.append((subset, score))
        
        # Sort by score in descending order
        subset_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return the subset with the highest score
        return subset_scores[0][0]
    
    def expand(self, formula, priority=1):
        """
        Expand the belief base by adding the formula.
        """
        self.add_belief(formula, priority)
    
    def revise(self, formula, priority=1):
        """
        Revise the belief base by first contracting with the negation of the formula,
        then expanding with the formula.
        """
        # Contract with the negation of the formula
        self.contract(Negation(formula))
        
        # Expand with the formula
        self.expand(formula, priority)
    
    def __str__(self):
        return "\n".join(f"{formula} (priority: {priority})" for formula, priority in self.beliefs.items())
    
    def __repr__(self):
        return str(self)


# Parser for propositional logic formulas
class FormulaParser:
    """
    Parser for propositional logic formulas.
    """
    def __init__(self):
        self.tokens = []
        self.current = 0
    
    def parse(self, formula_str):
        """
        Parse a string representation of a formula into a Formula object.
        
        Supported syntax:
        - Atoms: single letters or words (a, b, p, q, rain, etc.)
        - Negation: !a, ~a, -a, ¬a
        - Conjunction: a & b, a && b, a and b, a ∧ b
        - Disjunction: a | b, a || b, a or b, a ∨ b
        - Implication: a -> b, a => b, a implies b, a → b
        - Biconditional: a <-> b, a <=> b, a iff b, a ↔ b
        - Parentheses for grouping: (a & b) | c
        
        Example: "p & (q | !r) -> s"
        """
        # Tokenize the input
        self.tokenize(formula_str)
        self.current = 0
        
        # Parse the formula
        return self.parse_biconditional()
    
    def tokenize(self, formula_str):
        """
        Convert the input string into a list of tokens.
        """
        # Preprocess the formula string to handle special operators
        # Replace -> with a special token
        formula_str = formula_str.replace("->", " IMPLIES ")
        # Replace <-> with a special token
        formula_str = formula_str.replace("<->", " BICONDITIONAL ")
        # Replace => with a special token
        formula_str = formula_str.replace("=>", " IMPLIES ")
        # Replace <=> with a special token
        formula_str = formula_str.replace("<=>", " BICONDITIONAL ")
        
        i = 0
        tokens = []
        
        while i < len(formula_str):
            char = formula_str[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
            
            # Handle parentheses
            if char in '()':
                tokens.append(char)
                i += 1
                continue
            
            # Handle operators
            if char in '!~¬-':
                tokens.append('!')  # Normalize negation
                i += 1
                continue
            
            if char == '&':
                if i + 1 < len(formula_str) and formula_str[i + 1] == '&':
                    i += 2
                else:
                    i += 1
                tokens.append('&')
                continue
            
            if char == '|':
                if i + 1 < len(formula_str) and formula_str[i + 1] == '|':
                    i += 2
                else:
                    i += 1
                tokens.append('|')
                continue
            
            # Handle special tokens
            if i + 7 < len(formula_str) and formula_str[i:i+7] == "IMPLIES":
                tokens.append('->')
                i += 7
                continue
            
            if i + 13 < len(formula_str) and formula_str[i:i+13] == "BICONDITIONAL":
                tokens.append('<->')
                i += 13
                continue
            
            # Handle words (atoms)
            if char.isalnum() or char == '_':
                start = i
                while i < len(formula_str) and (formula_str[i].isalnum() or formula_str[i] == '_'):
                    i += 1
                tokens.append(formula_str[start:i])
                continue
            
            # Handle special symbols
            if char == '→':
                tokens.append('->')
                i += 1
                continue
            
            if char == '↔':
                tokens.append('<->')
                i += 1
                continue
            
            if char == '∧':
                tokens.append('&')
                i += 1
                continue
            
            if char == '∨':
                tokens.append('|')
                i += 1
                continue
            
            # Skip any other characters
            i += 1
        
        self.tokens = tokens
    
    def match(self, expected):
        """
        Check if the current token matches the expected token.
        """
        if self.current >= len(self.tokens):
            return False
        
        if self.tokens[self.current] == expected:
            self.current += 1
            return True
        
        return False
    
    def peek(self):
        """
        Return the current token without consuming it.
        """
        if self.current >= len(self.tokens):
            return None
        
        return self.tokens[self.current]
    
    def consume(self):
        """
        Consume and return the current token.
        """
        token = self.peek()
        self.current += 1
        return token
    
    def parse_biconditional(self):
        """
        Parse a biconditional expression.
        biconditional ::= implication ("<->" implication)*
        """
        left = self.parse_implication()
        
        while self.match('<->'):
            right = self.parse_implication()
            left = Biconditional(left, right)
        
        return left
    
    def parse_implication(self):
        """
        Parse an implication expression.
        implication ::= disjunction ("->" disjunction)*
        """
        left = self.parse_disjunction()
        
        while self.match('->'):
            right = self.parse_disjunction()
            left = Implication(left, right)
        
        return left
    
    def parse_disjunction(self):
        """
        Parse a disjunction expression.
        disjunction ::= conjunction ("|" conjunction)*
        """
        left = self.parse_conjunction()
        
        while self.match('|'):
            right = self.parse_conjunction()
            left = Disjunction(left, right)
        
        return left
    
    def parse_conjunction(self):
        """
        Parse a conjunction expression.
        conjunction ::= negation ("&" negation)*
        """
        left = self.parse_negation()
        
        while self.match('&'):
            right = self.parse_negation()
            left = Conjunction(left, right)
        
        return left
    
    def parse_negation(self):
        """
        Parse a negation expression.
        negation ::= "!" negation | primary
        """
        if self.match('!'):
            return Negation(self.parse_negation())
        
        return self.parse_primary()
    
    def parse_primary(self):
        """
        Parse a primary expression.
        primary ::= atom | "(" biconditional ")"
        """
        if self.match('('):
            expr = self.parse_biconditional()
            if not self.match(')'):
                raise ValueError("Expected closing parenthesis")
            return expr
        
        # Must be an atom
        token = self.consume()
        if token is None:
            raise ValueError("Unexpected end of input")
        
        return Atom(token)
