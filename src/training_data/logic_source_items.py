from __future__ import annotations

from source_items import Item


def item(
    question: str,
    correct: str,
    wrong: str,
    distractor_1: str,
    distractor_2: str,
    note: str,
) -> Item:
    return Item(
        question,
        correct,
        wrong,
        distractor_1,
        distractor_2,
        note,
    )


def build_easy_items() -> list[Item]:
    items: list[Item] = []

    modus_ponens = [
        ("If a card is red, then it is marked. This card is red.", "The card is marked.", "The card is not marked.", "Every marked card is red.", "No red card is marked."),
        ("If the alarm rings, the lamp flashes. The alarm rings.", "The lamp flashes.", "The lamp does not flash.", "Only lamps can ring.", "The alarm is a lamp."),
        ("If a file is archived, it is read-only. File K is archived.", "File K is read-only.", "File K is writable.", "Every read-only file is archived.", "No archive contains File K."),
        ("If a shape is a square, it has four sides. Shape S is a square.", "Shape S has four sides.", "Shape S has three sides.", "Every four-sided shape is a square.", "Shape S has no sides."),
        ("If a token is valid, the gate opens. This token is valid.", "The gate opens.", "The gate remains closed.", "The gate is a token.", "Every open gate makes tokens valid."),
    ]
    for premise, correct, wrong, d1, d2 in modus_ponens:
        items.append(item(
            f"{premise} What must follow?",
            correct, wrong, d1, d2,
            "This is modus ponens: P and P implies Q entail Q.",
        ))

    modus_tollens = [
        ("If the heater works, the room warms. The room did not warm.", "The heater did not work.", "The heater worked.", "The room was a heater.", "Nothing can be inferred."),
        ("If a key fits, the lock turns. The lock did not turn.", "The key did not fit.", "The key fit.", "Every turning lock has this key.", "The lock has no keyhole."),
        ("If the server responds, the status light is green. The light is not green.", "The server did not respond.", "The server responded.", "Green lights never respond.", "The server is green."),
        ("If the road is open, the bus arrives. The bus did not arrive.", "The road was not open.", "The road was open.", "Every arriving bus opens roads.", "The road is a bus."),
        ("If the code compiles, an executable is produced. No executable was produced.", "The code did not compile.", "The code compiled.", "Every executable is source code.", "Compilation is irrelevant."),
    ]
    for premise, correct, wrong, d1, d2 in modus_tollens:
        items.append(item(
            f"{premise} What follows under the stated conditional?",
            correct, wrong, d1, d2,
            "This is modus tollens: P implies Q and not Q entail not P.",
        ))

    syllogisms = [
        ("All lumes are bright. All bright things are visible. Nia is a lume.", "Nia is visible.", "Nia is not visible.", "All visible things are lumes.", "No bright thing is a lume."),
        ("All vedas are round. No round object is square. Object R is a veda.", "Object R is not square.", "Object R is square.", "Every nonsquare object is a veda.", "No veda is round."),
        ("No pilots are statues. Mara is a pilot.", "Mara is not a statue.", "Mara is a statue.", "All nonstatues are pilots.", "No conclusion about Mara follows."),
        ("All zins are metal. Some tools are zins.", "Some tools are metal.", "All tools are metal.", "No tool is metal.", "All metal objects are tools."),
        ("Some poets are teachers. All teachers are readers.", "Some poets are readers.", "All poets are readers.", "No poets are readers.", "All readers are poets."),
        ("No red objects are cold. Some boxes are red.", "Some boxes are not cold.", "All boxes are warm.", "No boxes are red.", "Every noncold thing is a box."),
        ("All maps are documents. No document is edible.", "No map is edible.", "Every edible thing is a map.", "Some maps are edible.", "No map is a document."),
        ("Some runners are musicians. No musician is silent.", "Some runners are not silent.", "No runner is silent.", "All runners are musicians.", "Some silent people are musicians."),
        ("All cedars are trees. Some park plants are cedars.", "Some park plants are trees.", "All park plants are trees.", "No park plant is a tree.", "All trees are cedars."),
        ("No glass objects are flexible. Every vial is glass.", "No vial is flexible.", "Every flexible object is a vial.", "Some vials are flexible.", "No vial is glass."),
    ]
    for premises, correct, wrong, d1, d2 in syllogisms:
        items.append(item(
            f"{premises} Which conclusion must be true?",
            correct, wrong, d1, d2,
            "The conclusion follows by applying the stated universal relation to the specified member or subgroup.",
        ))

    negations = [
        ("Every lamp is on.", "At least one lamp is not on.", "No lamp is on.", "Every lamp is off.", "At least one lamp is on."),
        ("No boxes are empty.", "At least one box is empty.", "Every box is empty.", "Some boxes are not empty.", "There are no boxes."),
        ("Some birds can swim.", "No bird can swim.", "Every bird can swim.", "Some birds cannot swim.", "Only birds can swim."),
        ("At least one key works.", "No key works.", "Every key works.", "At least two keys work.", "Some key does not work."),
        ("All reports are complete.", "Some report is incomplete.", "No report is complete.", "Some report is complete.", "Reports do not exist."),
        ("Some tiles are blue.", "No tile is blue.", "All tiles are blue.", "Some tiles are not blue.", "Blue objects are tiles."),
        ("No train is late.", "At least one train is late.", "Every train is late.", "Some train is on time.", "No train exists."),
        ("Every member voted.", "At least one member did not vote.", "No member voted.", "Exactly one member voted.", "Some member voted."),
    ]
    for statement, correct, wrong, d1, d2 in negations:
        items.append(item(
            f"What is the logical negation of: {statement}",
            correct, wrong, d1, d2,
            "Negating a universal introduces an existential counterexample; negating an existential removes all witnesses.",
        ))

    truth_items = [
        ("P is true and Q is false. What is P AND Q?", "False", "True", "Both true and false", "Undefined", "A conjunction is true only when both operands are true."),
        ("P is false and Q is true. What is P OR Q?", "True", "False", "Undefined", "A contradiction", "A disjunction is true when at least one operand is true."),
        ("P is false. What is NOT P?", "True", "False", "P", "Undefined", "Negation reverses the truth value."),
        ("P is true and Q is false. What is P implies Q?", "False", "True", "Equivalent to P", "Undefined", "An implication is false only when its antecedent is true and consequent false."),
        ("P is false and Q is false. What is P implies Q?", "True", "False", "Both", "Undefined", "An implication with a false antecedent is true in classical logic."),
        ("P is true and Q is true. What is P XOR Q?", "False", "True", "Undefined", "Equivalent to AND", "Exclusive OR is true when exactly one operand is true."),
        ("P is false and Q is true. What is P XOR Q?", "True", "False", "Undefined", "Equivalent to NOT Q", "Exactly one operand is true, so XOR is true."),
        ("P is true. What is P OR NOT P?", "True", "False", "P is undefined", "A contradiction", "P or its negation is a tautology."),
        ("P is false. What is P AND NOT P?", "False", "True", "Equivalent to NOT P", "Undefined", "A proposition and its negation cannot both be true."),
        ("P is true and Q is true. What is NOT(P AND Q)?", "False", "True", "Equivalent to P", "Undefined", "P AND Q is true, so its negation is false."),
    ]
    for question, correct, wrong, d1, d2, note in truth_items:
        items.append(item(question, correct, wrong, d1, d2, note))

    sequences = [
        ("3, 6, 9, 12, ...", "15", "14", "18", "13", "The sequence adds 3 each step."),
        ("1, 4, 9, 16, ...", "25", "20", "32", "24", "The terms are consecutive positive squares."),
        ("2, 3, 5, 8, 12, ...", "17", "16", "20", "24", "The successive additions are 1, 2, 3, 4, then 5."),
        ("64, 32, 16, 8, ...", "4", "0", "2", "6", "Each term is half the previous term."),
        ("A, C, E, G, ...", "I", "H", "J", "K", "The sequence advances two alphabet positions."),
        ("10, 9, 7, 4, ...", "0", "1", "-1", "2", "The sequence subtracts 1, then 2, then 3, then 4."),
        ("1, 2, 6, 24, ...", "120", "48", "96", "100", "Each term multiplies by the next integer."),
        ("5, 10, 20, 40, ...", "80", "60", "100", "45", "Each term doubles."),
        ("21, 18, 15, 12, ...", "9", "8", "6", "10", "Each term decreases by 3."),
        ("2, 5, 11, 23, ...", "47", "46", "35", "48", "Each term is twice the previous term plus 1."),
        ("100, 50, 25, 12.5, ...", "6.25", "7.5", "5", "25", "Each term is divided by 2."),
        ("7, 14, 13, 26, 25, ...", "50", "49", "24", "52", "The operations alternate multiply by 2 and subtract 1."),
        ("1, 3, 7, 15, ...", "31", "30", "23", "32", "Each term is twice the previous term plus 1."),
        ("30, 26, 22, 18, ...", "14", "16", "12", "10", "Each term decreases by 4."),
        ("B, E, H, K, ...", "N", "M", "O", "P", "Letters advance by three positions."),
    ]
    for sequence, correct, wrong, d1, d2, note in sequences:
        items.append(item(
            f"What is the next term in the sequence {sequence}?",
            correct, wrong, d1, d2, note,
        ))

    set_items = [
        ("A = {1, 2, 5} and B = {2, 4, 5}. Which elements belong to both sets?", "{2, 5}", "{1, 2, 4, 5}", "{1, 4}", "{5}", "The elements common to both sets are 2 and 5."),
        ("A = {p, q, r} and B = {q, s}. What is the set difference A minus B?", "{p, r}", "{q}", "{p, q, r, s}", "{s}", "Removing B's shared element q from A leaves p and r."),
        ("Which relation holds if every element of X is also in Y?", "X is a subset of Y", "Y is disjoint from X", "X equals the empty set necessarily", "Y is a member of X", "Subset means all members of one set belong to the other."),
        ("What is the cardinality of {red, blue, green, yellow}?", "4", "3", "5", "1", "Cardinality counts distinct elements."),
        ("What is the intersection of two disjoint sets?", "The empty set", "Their union", "The first set", "A universal set", "Disjoint sets have no common element."),
        ("If U = {1,2,3,4} and A = {1,4}, what is A's complement in U?", "{2,3}", "{1,4}", "{1,2,3,4}", "The empty set", "The complement contains universal-set elements not in A."),
        ("Which item belongs to the set of even positive integers?", "14", "9", "-3", "7", "Fourteen is positive and divisible by 2."),
        ("Which set is empty?", "{x: x is an integer greater than 2 and less than 3}", "{2}", "{0}", "{x: x is an even prime}", "No integer lies strictly between 2 and 3."),
        ("If A is a proper subset of B, what must be true?", "B has at least one element not in A", "A and B are disjoint", "A contains B", "A equals B", "A proper subset is contained in but not equal to B."),
        ("If x belongs to A intersect B, what follows?", "x belongs to both A and B", "x belongs to neither set", "x belongs only to A", "A and B are disjoint", "Intersection membership requires membership in each set."),
    ]
    for question, correct, wrong, d1, d2, note in set_items:
        items.append(item(question, correct, wrong, d1, d2, note))

    items.extend([
        item("If every blue token is large and token K is blue, what can be concluded?", "K is large", "K is not large", "Every large token is blue", "No blue token is large", "Universal instantiation applies the property of blue tokens to K."),
        item("No circles are triangles, and shape M is a circle. What follows?", "M is not a triangle", "M is a triangle", "All nontriangles are circles", "Nothing follows", "Membership in circles excludes membership in triangles."),
        item("Some cups are red, and every red object is visible. What follows?", "Some cups are visible", "All cups are visible", "No cups are visible", "All visible objects are cups", "The red cups are witnesses that are also visible."),
        item("All novels are books, and no book is liquid. What follows?", "No novel is liquid", "Some novels are liquid", "All liquids are novels", "No novel is a book", "Novel membership implies book membership, which excludes liquids."),
        item("Some dancers are engineers, and no engineer is asleep. What follows?", "Some dancers are not asleep", "No dancer is asleep", "All dancers are engineers", "Some engineers are asleep", "The dancers who are engineers inherit the not-asleep property."),
        item("If P is true, what is the truth value of P AND true?", "True", "False", "Undefined", "Both", "Conjunction with true preserves P."),
        item("If P is false, what is the truth value of P OR false?", "False", "True", "Undefined", "Both", "Disjunction with false preserves P."),
        item("What is the truth value of true implies false?", "False", "True", "Undefined", "Both", "Material implication is false in exactly this truth-value case."),
        item("What is the truth value of false implies true?", "True", "False", "Undefined", "Both", "An implication with false antecedent is true."),
        item("What is the truth value of true if and only if false?", "False", "True", "Undefined", "Both", "A biconditional is false when its sides differ."),
        item("Which phrase expresses P AND Q?", "Both P and Q", "P or Q or both", "Not P", "If P then Q", "A conjunction asserts both components."),
        item("Which phrase expresses P OR Q inclusively?", "At least one of P and Q", "Exactly one of P and Q", "Neither P nor Q", "P only", "Inclusive OR permits one or both operands."),
        item("Which phrase expresses NOT P?", "It is not the case that P", "P and Q", "P follows Q", "P is sufficient for Q", "Negation denies the proposition."),
        item("If A is a subset of B, which statement about an element x in A is true?", "x is also in B", "x cannot be in B", "B is empty", "x equals B", "Subset membership transfers each A element into B."),
        item("What is the union of {1, 2} and {2, 3}?", "{1, 2, 3}", "{2}", "{1, 3}", "{1, 2, 2, 3}", "A set union lists each distinct element in either set."),
        item("What is the intersection of {a, c, d} and {b, c, d}?", "{c, d}", "{a, b}", "{a, b, c, d}", "The empty set", "The common elements are c and d."),
        item("How many elements are in the empty set?", "0", "1", "-1", "Undefined", "The empty set contains no elements."),
        item("Which symbol sequence continues AB, BC, CD, DE, ...?", "EF", "DF", "EE", "FG", "Each pair shifts both letters one position forward."),
        item("Which number continues 2, 4, 8, 16, ...?", "32", "24", "18", "64", "Each term is twice its predecessor."),
        item("Which number continues 9, 16, 25, 36, ...?", "49", "45", "48", "64", "The values are squares 3², 4², 5², 6², then 7²."),
        item("If Kai is older than Lea, which statement is equivalent?", "Lea is younger than Kai", "Lea is older than Kai", "They have the same age", "No age comparison is possible", "Older-than reverses to younger-than when the subjects swap."),
        item("If X is north of Y, where is Y relative to X?", "South", "North", "East", "At the same location", "The inverse direction of north is south."),
        item("If event A occurs before B, can B occur before A in the same strict ordering?", "No", "Yes, necessarily", "Only if A equals B", "Ordering has no direction", "A strict before relation is asymmetric."),
        item("Which argument form is valid?", "P; if P then Q; therefore Q", "Q; if P then Q; therefore P", "Not P; if P then Q; therefore not Q", "P or Q; therefore P", "The first form is modus ponens."),
        item("Which statement is a contradiction?", "The door is open and the door is not open", "The door is open or not open", "If the door is open, it is open", "The door may be open", "A proposition conjoined with its negation cannot be true."),
    ])

    if len(items) != 88:
        raise ValueError(
            f"Expected 88 easy logic items, found {len(items)}"
        )

    return items


def build_medium_items() -> list[Item]:
    items: list[Item] = []

    conditional_rows = [
        ("If P then Q. If Q then R. P is true.", "R is true.", "R is false.", "Q is false.", "P is false.", "Implication chains give Q and then R."),
        ("If A then B. If B then C. C is false.", "A is false.", "A is true.", "B is true.", "Nothing follows.", "C false implies B false, which implies A false."),
        ("If M then N. N is true.", "M may be true or false.", "M must be true.", "M must be false.", "N must be false.", "Affirming the consequent is invalid; N can have another cause."),
        ("If S then T. S is false.", "T may be true or false.", "T must be false.", "T must be true.", "S must be true.", "Denying the antecedent is invalid."),
        ("P is sufficient for Q.", "P guarantees Q.", "Q guarantees P.", "P and Q are unrelated.", "P is necessary for Q.", "Sufficiency means P implies Q."),
        ("R is necessary for S.", "S implies R.", "R implies S.", "R and S are equivalent necessarily.", "S implies not R.", "A necessary condition must hold whenever S holds."),
        ("P if and only if Q. P is false.", "Q is false.", "Q is true.", "Nothing follows.", "P becomes true.", "A biconditional gives Q implies P; not P therefore implies not Q."),
        ("Either A or B, but not both. A is true.", "B is false.", "B is true.", "Both are false.", "Nothing follows.", "Exclusive disjunction permits exactly one true alternative."),
        ("At least one of X and Y is true. X is false.", "Y is true.", "Y is false.", "Both are false.", "Nothing follows.", "The inclusive disjunction plus not X entails Y."),
        ("Not both P and Q. P is true.", "Q is false.", "Q is true.", "P is false.", "Both are true.", "If the conjunction is forbidden and P holds, Q cannot hold."),
        ("If not A then B. B is false.", "A is true.", "A is false.", "B is true.", "Nothing follows.", "Modus tollens yields not(not A), equivalent to A."),
        ("If C then not D. D is true.", "C is false.", "C is true.", "D is false.", "Nothing follows.", "D contradicts the consequent not D, so C is false."),
        ("If P then Q, and if not P then Q.", "Q is true regardless of P.", "Q is false.", "P is true.", "P is false.", "The two cases cover P and not P, each yielding Q."),
        ("If A then B. If A then not B.", "A must be false in any consistent assignment.", "A must be true.", "B must be both true and false.", "B must be true.", "A would imply a contradiction, so consistency requires not A."),
        ("P implies Q and Q implies P.", "P and Q have the same truth value.", "P is always true.", "Q is always false.", "P and Q cannot both be true.", "Mutual implication is a biconditional."),
    ]
    for premises, correct, wrong, d1, d2, note in conditional_rows:
        items.append(item(
            f"{premises} Which conclusion is valid?",
            correct, wrong, d1, d2, note,
        ))

    quantifier_rows = [
        ("All A are B. Some B are C.", "It is possible that no A are C.", "Some A must be C.", "All C are A.", "No B are C.", "The B that are C need not be among the A."),
        ("Some A are B. Some B are C.", "No relation between A and C is forced.", "Some A must be C.", "All A are C.", "No A are C.", "The two existential groups within B may be different members."),
        ("All A are B. No B are C.", "No A are C.", "Some A are C.", "All C are A.", "No A are B.", "A is contained in B, which is disjoint from C."),
        ("No A are B. Some C are A.", "Some C are not B.", "All C are not B.", "Some C are B.", "No C are A.", "The C that are A inherit exclusion from B."),
        ("All A are B. Some A exist.", "Some B exist.", "No B exist.", "All B are A.", "Some non-A are B.", "An existing A is also an existing B."),
        ("All A are B. No A exist.", "No conclusion about whether B exist follows.", "No B exist.", "Some B exist.", "All B are A.", "A universal statement can be vacuously true when A is empty."),
        ("Some A are not B.", "Not all A are B.", "No A are B.", "All A are not B.", "Some B are A necessarily.", "One counterexample suffices to negate the universal."),
        ("Not all A are B, and A exist.", "Some A are not B.", "No A are B.", "All A are B.", "Some B are not A.", "Not all A are B is equivalent to an A counterexample."),
        ("Exactly one A is B.", "Some A is B.", "All A are B.", "No A is B.", "At least two A are B.", "Exactly one implies existence of at least one."),
        ("At most one A is B.", "Two distinct A cannot both be B.", "Exactly one A is B.", "At least one A is B.", "No A can be B.", "At most one permits zero or one, but not two."),
        ("At least two A are B.", "Some A are B.", "Exactly two A are B.", "All A are B.", "No A are B.", "At least two entails at least one but may allow more."),
        ("Every A is either B or C, and no A is B.", "Every A is C.", "No A is C.", "Every B is A.", "Some A is B.", "The B alternative is excluded for each A."),
        ("No A are both B and C. Some A are B.", "Some A are not C.", "All A are not C.", "Some A are C.", "No A are B.", "The specified A that are B cannot also be C."),
        ("All A are B or C. Some A are not B.", "Some A are C.", "No A are C.", "All A are C.", "Some B are C.", "An A outside B must satisfy the remaining C alternative."),
        ("Only A are B.", "All B are A.", "All A are B.", "No A are B.", "Some B are not A.", "'Only A are B' makes A a necessary condition for B."),
    ]
    for premises, correct, wrong, d1, d2, note in quantifier_rows:
        items.append(item(
            f"{premises} What follows?",
            correct, wrong, d1, d2, note,
        ))

    set_rows = [
        ("A has 12 elements, B has 9, and their intersection has 4. How many elements are in A union B?", "17", "21", "25", "8", "Inclusion-exclusion gives 12+9-4 = 17."),
        ("A class has 30 students; 18 study French, 15 study German, and 7 study both. How many study at least one?", "26", "33", "23", "10", "Inclusion-exclusion gives 18+15-7 = 26."),
        ("In a group of 40, 22 like tea, 19 like coffee, and 9 like both. How many like neither?", "8", "12", "31", "49", "The union is 22+19-9=32, leaving 8."),
        ("Set A has 5 elements and set B has 3. If they are disjoint, how many elements are in A union B?", "8", "5", "15", "2", "Disjoint sets contribute all 5+3 elements."),
        ("How many subsets does a three-element set have?", "8", "6", "3", "9", "An n-element set has 2^n subsets."),
        ("How many proper subsets does a four-element set have?", "15", "16", "8", "4", "There are 16 subsets total and one is the whole set."),
        ("If A is a subset of B and B is a subset of C, what relation follows?", "A is a subset of C", "C is a subset of A", "A and C are disjoint", "B is empty", "Subset inclusion is transitive."),
        ("If A union B equals A, what must be true?", "B is a subset of A", "A is a subset of B", "A and B are disjoint", "B is empty necessarily", "Adding B introduces nothing new exactly when B is contained in A."),
        ("If A intersect B equals A, what must be true?", "A is a subset of B", "B is a subset of A", "A and B are disjoint", "A is empty necessarily", "Every A element surviving intersection means every A element lies in B."),
        ("If A and B are complements in U, what are A union B and A intersect B?", "U and the empty set", "The empty set and U", "A and B", "U and U", "Complements exhaust U and share no elements."),
    ]
    for question, correct, wrong, d1, d2, note in set_rows:
        items.append(item(question, correct, wrong, d1, d2, note))

    order_rows = [
        ("Ana finishes before Bo, and Bo finishes before Cy. Who finishes first?", "Ana", "Bo", "Cy", "Cannot be determined", "Transitivity gives Ana before Bo before Cy."),
        ("L is taller than M, and N is taller than L. Who is tallest?", "N", "L", "M", "L and N tie", "N > L > M."),
        ("Red is left of Blue, and Green is right of Blue. What is the order?", "Red, Blue, Green", "Green, Blue, Red", "Blue, Red, Green", "Red, Green, Blue", "Red lies before Blue, which lies before Green."),
        ("Task Q follows P, and R follows Q. Which task is last?", "R", "Q", "P", "P and R tie", "The order is P, Q, R."),
        ("Book A is below B; B is below C. Which book is highest?", "C", "B", "A", "A and C", "The vertical order is A below B below C."),
        ("J arrives after K but before L. Who arrives second among the three?", "J", "K", "L", "Cannot be determined", "The order is K, J, L."),
        ("Mira ranks above Noel; Omar ranks below Noel. Who ranks in the middle?", "Noel", "Mira", "Omar", "Mira and Omar", "The order is Mira, Noel, Omar."),
        ("Station X is east of Y, and Z is west of Y. Which is westernmost?", "Z", "Y", "X", "X and Z tie", "The west-east order is Z, Y, X."),
        ("Box C is heavier than D, and D is heavier than E. Which is lightest?", "E", "D", "C", "C and E tie", "C > D > E by weight."),
        ("Ruth starts before Sam; Tara starts after Sam. Who starts last?", "Tara", "Sam", "Ruth", "Cannot be determined", "The order is Ruth, Sam, Tara."),
    ]
    for premises, correct, wrong, d1, d2, note in order_rows:
        items.append(item(
            f"{premises}",
            correct, wrong, d1, d2, note,
        ))

    fallacy_rows = [
        ("If it rains, the street is wet. The street is wet, so it rained.", "Affirming the consequent", "Modus ponens", "Modus tollens", "Valid biconditional reasoning", "The wet street could have another cause."),
        ("If a device is charged, it turns on. It is not charged, so it cannot turn on.", "Denying the antecedent", "Modus tollens", "Modus ponens", "Valid disjunction", "A different power source could make it turn on."),
        ("Everyone I asked prefers tea, so everyone in the country prefers tea.", "Hasty generalization", "Deductive certainty", "Modus ponens", "Circular definition", "A small or biased sample does not justify a universal population claim."),
        ("The proposal is wrong because the person presenting it is unpleasant.", "Ad hominem", "Appeal to valid evidence", "Modus tollens", "Statistical sampling", "The argument attacks the person rather than the proposal."),
        ("Either we ban all cars or traffic will never improve.", "False dilemma", "Valid exhaustive disjunction", "Appeal to tradition", "Composition", "The claim ignores other possible traffic policies."),
        ("This rule is good because it is a good rule.", "Circular reasoning", "Causal inference", "Analogy", "Contraposition", "The conclusion is merely restated as its own support."),
        ("After the new sign was installed, sales rose; therefore the sign caused all of the rise.", "Post hoc causal error", "Valid controlled experiment", "Deductive proof", "Definition", "Timing alone does not rule out other causes."),
        ("No one has proved that aliens are absent, so aliens definitely visit us.", "Appeal to ignorance", "Modus ponens", "Valid induction", "Contradiction", "Lack of disproof is not proof of the positive claim."),
        ("Most people believe the rumor, so it must be true.", "Appeal to popularity", "Valid majority theorem", "Modus tollens", "Equivocation", "Popularity does not establish factual truth."),
        ("One part in this machine is light, so the whole machine must be light.", "Fallacy of composition", "Fallacy of division", "Valid measurement", "Contraposition", "A property of one component need not characterize the whole."),
        ("The team is excellent, so every player must be excellent.", "Fallacy of division", "Fallacy of composition", "Valid universal instantiation", "Modus ponens", "A property of a whole need not hold for each member."),
        ("The word 'bank' means a financial institution, so a river bank stores money.", "Equivocation", "Valid analogy", "Modus tollens", "Sampling bias", "The argument switches between different meanings of the same word."),
        ("We have always used this method, so it is the best method.", "Appeal to tradition", "Controlled comparison", "Valid deduction", "False cause only", "Past use alone does not establish optimality."),
        ("An expert in music says this medicine works, so it must work.", "Irrelevant authority", "Relevant expert consensus", "Modus ponens", "Definition", "Expertise outside the relevant field does not establish the medical claim."),
        ("Changing one minor rule will inevitably destroy the entire institution.", "Slippery slope", "Valid causal chain with evidence", "Conjunction", "Sampling", "The conclusion asserts extreme consequences without supporting intermediate links."),
    ]
    for argument, correct, wrong, d1, d2, note in fallacy_rows:
        items.append(item(
            f"Which reasoning error best describes this argument: {argument}",
            correct, wrong, d1, d2, note,
        ))

    argument_rows = [
        ("Premise: All metals conduct. Premise: Copper is a metal. Conclusion: Copper conducts.", "Deductively valid", "Invalid by affirming the consequent", "A contradiction", "A false dilemma", "The conclusion follows by universal instantiation and modus ponens."),
        ("Premise: Some artists are teachers. Conclusion: All artists are teachers.", "Invalid because 'some' does not imply 'all'", "Deductively valid", "Valid contraposition", "A tautology", "An existential premise cannot support a universal conclusion."),
        ("Premise: No squares are circles. Premise: Shape X is a square. Conclusion: X is not a circle.", "Deductively valid", "Invalid because X may be a circle", "Circular", "An appeal to popularity", "Membership in the excluded class entails nonmembership in circles."),
        ("Premise: If P then Q. Premise: Q. Conclusion: P.", "Invalid: affirming the consequent", "Valid modus ponens", "Valid modus tollens", "A contradiction", "Q can be true without P."),
        ("Premise: If P then Q. Premise: not Q. Conclusion: not P.", "Valid modus tollens", "Invalid denying the antecedent", "Affirming the consequent", "Circular", "The conclusion is the contrapositive inference."),
        ("Premise: P or Q. Premise: not P. Conclusion: Q.", "Valid disjunctive syllogism", "Invalid affirming the consequent", "A false dilemma necessarily", "Circular", "Eliminating P from the stated disjunction leaves Q."),
        ("Premise: All A are B. Premise: All B are C. Conclusion: All A are C.", "Deductively valid", "Invalid reversal", "A contradiction", "An analogy", "Class inclusion is transitive."),
        ("Premise: Some A are B. Premise: No B are C. Conclusion: Some A are not C.", "Deductively valid", "Invalid because no A exist", "Universal overreach", "Affirming the consequent", "The existing A that are B cannot be C."),
        ("Premise: All A are B. Conclusion: Some A are B.", "Invalid without an existence premise", "Valid in modern predicate logic", "A contradiction", "Modus tollens", "A universal can be true when no A exist."),
        ("Premise: Exactly one key opens the lock. Premise: Key K opens it. Conclusion: No other key opens it.", "Deductively valid", "Invalid because another key may open it", "Affirming the consequent", "A composition fallacy", "Exactly one plus K as a witness excludes every other key."),
    ]
    for argument, correct, wrong, d1, d2, note in argument_rows:
        items.append(item(
            f"How should this argument be classified? {argument}",
            correct, wrong, d1, d2, note,
        ))

    truth_equiv = [
        ("Which expression is equivalent to NOT(P AND Q)?", "NOT P OR NOT Q", "NOT P AND NOT Q", "P OR Q", "P AND Q", "De Morgan's law negates each operand and swaps AND for OR."),
        ("Which expression is equivalent to NOT(P OR Q)?", "NOT P AND NOT Q", "NOT P OR NOT Q", "P AND Q", "P implies Q", "De Morgan's law negates each operand and swaps OR for AND."),
        ("Which expression is equivalent to P implies Q?", "NOT P OR Q", "P OR NOT Q", "P AND Q", "NOT P AND Q", "Material implication is not P or Q."),
        ("Which expression is the contrapositive of P implies Q?", "NOT Q implies NOT P", "Q implies P", "NOT P implies NOT Q", "P implies NOT Q", "The contrapositive reverses and negates antecedent and consequent."),
        ("Which expression is the converse of P implies Q?", "Q implies P", "NOT Q implies NOT P", "NOT P implies NOT Q", "P AND Q", "The converse reverses the conditional without negating."),
        ("Which expression is the inverse of P implies Q?", "NOT P implies NOT Q", "Q implies P", "NOT Q implies NOT P", "P OR Q", "The inverse negates both parts without reversing."),
        ("When is P if and only if Q true?", "When P and Q have the same truth value", "Only when P is true", "Only when Q is false", "When exactly one is true", "A biconditional is true when both sides match."),
        ("Which is a tautology?", "P OR NOT P", "P AND NOT P", "P AND Q", "P implies NOT P", "The law of excluded middle is true under every valuation."),
        ("Which is a contradiction?", "P AND NOT P", "P OR NOT P", "P implies P", "P if and only if P", "A proposition and its negation cannot both hold."),
        ("If P implies Q is false, what are P and Q?", "P true and Q false", "P false and Q true", "Both false", "Both true", "This is the only false row of material implication."),
    ]
    for question, correct, wrong, d1, d2, note in truth_equiv:
        items.append(item(question, correct, wrong, d1, d2, note))

    items.extend([
        item("Four runners J, K, L, M finish with J before K, K before L, and L before M. Who is second?", "K", "J", "L", "M", "The complete chain is J, K, L, M."),
        item("Four books A, B, C, D are shelved with D before B, B before A, and A before C. Which is last?", "C", "A", "B", "D", "The constraints form D, B, A, C."),
        item("Nora arrives before Omar, Priya after Omar, and Quinn before Nora. Who arrives first?", "Quinn", "Nora", "Omar", "Priya", "The chain is Quinn before Nora before Omar before Priya."),
        item("Three boxes X, Y, Z have different weights. X is heavier than Y, and Z is heavier than X. Which is lightest?", "Y", "X", "Z", "Cannot be determined", "Z > X > Y."),
        item("A meeting is after lunch but before sunset. Dinner is after sunset. Which event is earliest?", "Lunch", "Meeting", "Sunset", "Dinner", "The order is lunch, meeting, sunset, dinner."),
        item("If all valid tickets are stamped and no stamped ticket is blank, what follows about valid tickets?", "No valid ticket is blank", "All blank tickets are valid", "Some valid tickets are blank", "No valid ticket is stamped", "Valid implies stamped, and stamped excludes blank."),
        item("Some metal objects are rings; every ring is circular. What follows?", "Some metal objects are circular", "All metal objects are circular", "No rings are metal", "All circular objects are rings", "The metal objects that are rings are also circular."),
        item("All A are B, all C are B, and no B are D. What follows?", "Neither A nor C overlaps D", "A and C are identical", "Every D is B", "Some A are D", "Both A and C are subsets of B, which is disjoint from D."),
        item("No poets are robots; some teachers are poets. Which conclusion follows?", "Some teachers are not robots", "No teachers are robots", "All teachers are poets", "Some robots are poets", "The teachers that are poets cannot be robots."),
        item("All keys are metal, and some metal objects are old. Does it follow that some keys are old?", "No, the old metal objects need not be keys", "Yes, necessarily", "No key can be old", "All old things are keys", "The existential metal group may lie outside the key subset."),
        item("If P is necessary but not sufficient for Q, which statement is correct?", "Q implies P, but P does not guarantee Q", "P implies Q, but Q does not imply P", "P and Q are equivalent", "P and Q cannot both hold", "Necessity gives Q→P; lack of sufficiency denies P→Q as a general rule."),
        item("If P is sufficient but not necessary for Q, which statement is correct?", "P implies Q, but Q can occur without P", "Q implies P, but P can occur without Q", "P and Q are equivalent", "Q is impossible", "Sufficiency gives P→Q; nonnecessity permits Q with not P."),
        item("A password is accepted only if it has a digit. What does this say?", "Having a digit is necessary for acceptance", "Having a digit guarantees acceptance", "Acceptance prevents digits", "Digits and acceptance are unrelated", "'Only if' introduces a necessary condition."),
        item("A lamp turns on if its switch is closed. What does this say in the stated model?", "A closed switch is sufficient for the lamp turning on", "A closed switch is necessary but never sufficient", "The lamp on implies the switch is open", "The switch and lamp are unrelated", "'If' marks the antecedent as sufficient."),
        item("Unless P, Q. Which standard conditional expresses this?", "If not P, then Q", "If P, then Q", "If Q, then P", "P and Q", "'Unless P, Q' is conventionally represented as not P implies Q."),
        item("P only if Q. Which direction is correct?", "P implies Q", "Q implies P", "Not P implies Q", "P and Q are disjoint", "'Only if Q' makes Q necessary for P."),
        item("P if Q. Which direction is correct?", "Q implies P", "P implies Q", "Not Q implies P", "P and Q are contradictory", "'P if Q' states that Q is sufficient for P."),
        item("Which is logically equivalent to 'No A are B'?", "All A are not B", "Some A are B", "All B are A", "Some B are not A", "Both formulations exclude every A from B."),
        item("Which is logically equivalent to 'Not every A is B'?", "Some A is not B", "No A is B", "Every B is A", "Some A is B", "A universal statement is false exactly when a counterexample exists."),
        item("If exactly three of five switches are on, how many are off?", "2", "3", "5", "8", "Five total minus three on leaves two off."),
        item("A four-character string uses A or B and begins with A. How many such strings exist?", "8", "4", "16", "6", "The first position is fixed and the remaining three each have two choices: 2³ = 8."),
        item("How many ordered pairs can be formed with first element from {1,2,3} and second from {x,y}?", "6", "5", "3", "2", "The product rule gives 3×2 = 6 pairs."),
        item("Three roads connect A to B and two roads connect B to C. How many A-to-C route combinations via B exist?", "6", "5", "3", "2", "Choose one of three first roads and one of two second roads."),
        item("A claim predicts both R and S. Observation shows R but not S. What happens to the conjunction prediction?", "It is falsified", "It is confirmed", "It becomes a tautology", "Nothing can be assessed", "A conjunction requires both predicted components."),
        item("An argument has true premises but a false conclusion. What can be said about its deductive validity?", "It is invalid", "It is valid", "It is sound", "It is a tautology", "A valid argument cannot have true premises and a false conclusion."),
    ])

    if len(items) != 110:
        raise ValueError(
            f"Expected 110 medium logic items, found {len(items)}"
        )

    return items


def build_hard_items() -> list[Item]:
    return [
        item("Four tasks W, X, Y, Z are scheduled once each. W is before X, Y is after X, and Z is before W. Which order is forced?", "Z, W, X, Y", "W, Z, X, Y", "Z, X, W, Y", "Y, X, W, Z", "The constraints chain as Z before W before X before Y."),
        item("A, B, and C sit in a row. A is not at an end, and B is left of C. What is the only order?", "B, A, C", "A, B, C", "C, A, B", "B, C, A", "A must occupy the middle; B left of C then forces B, A, C."),
        item("Five books P, Q, R, S, T are ordered. P is first, T is last, Q is immediately before R, and S is not second. Which book is second?", "Q", "R", "S", "T", "The middle slots are 2-4; Q,R must occupy 2,3 because S cannot be second."),
        item("Exactly two of P, Q, and R are true. P is true and Q is false. What is R?", "True", "False", "Both", "Undetermined", "With exactly two true, R must join P as the second true proposition."),
        item("Exactly two of A, B, C are false. A implies B, and B is false. What follows?", "A is false and C is true", "A is true and C is false", "A and C are both false", "C is false only", "B false forces A false by modus tollens; these are the two false propositions, so C is true."),
        item("Three boxes have labels 'Apples', 'Oranges', and 'Mixed', and every label is wrong. Drawing an apple from the box labeled 'Mixed' identifies that box as what?", "Apples", "Mixed", "Oranges", "Impossible to know", "The wrongly labeled Mixed box cannot be mixed; the apple draw makes it the Apples box."),
        item("A statement says, 'This statement is false.' What kind of issue does it illustrate?", "Self-referential paradox", "Valid tautology", "Modus ponens", "A statistical fallacy", "Assigning either truth value reverses what the sentence asserts."),
        item("Knights always tell truth and knaves always lie. Person A says, 'Both of us are knaves.' What are A and B?", "A is a knave and B is a knight", "Both are knights", "Both are knaves", "A is a knight and B a knave", "A cannot truthfully be a knight saying both are knaves; as a lying knave, the conjunction is false, so B is a knight."),
        item("P, Q, and R satisfy: P implies Q; Q implies R; and R is false. Which assignment is forced?", "P false, Q false, R false", "P true, Q false, R false", "P false, Q true, R false", "All true", "R false yields Q false by modus tollens, then P false."),
        item("A code has four positions filled with A or B and must contain exactly two A symbols. How many valid codes exist?", "6", "4", "8", "16", "Choose the two positions for A: 4 choose 2 = 6."),
        item("At a gathering of four people, every unordered pair exchanges one greeting. How many greetings occur?", "6", "8", "12", "4", "Each greeting is an unordered pair: 4 choose 2 = 6."),
        item("A committee of two is chosen from A, B, C, D, but A and B cannot serve together. How many committees are possible?", "5", "6", "4", "3", "There are 6 pairs total and only pair AB is forbidden."),
        item("A three-digit code uses distinct digits from {1,2,3,4}. How many codes are possible?", "24", "12", "64", "6", "There are 4×3×2 = 24 ordered choices."),
        item("A bag contains two red and two blue tokens. Two are drawn without replacement. Which color sequences are possible?", "RR, RB, BR, and BB", "Only RR and BB", "Only RB and BR", "Eight sequences", "With two of each color, every two-position color sequence can occur."),
        item("Premises: Every A is B; every B is C; no C is D; some A exist. Which conclusion is strongest?", "Some B are C and not D", "All C are A", "Some D are A", "No B are C", "An existing A belongs to B and C, and no C belongs to D."),
        item("Premises: Some A are B; all B are C; some C are D. Does 'some A are D' follow?", "No; the two existential groups in C may be different", "Yes, necessarily", "No A can be D", "All A are D", "The B-derived C member need not be the C member that is D."),
        item("P is true exactly when Q is false, and Q is true exactly when R is true. If R is false, what is P?", "True", "False", "Both", "Undetermined", "R false makes Q false; P is true exactly when Q is false."),
        item("A door opens iff both keys K and L are turned. The door is open. What follows?", "Both K and L are turned", "At least one key is not turned", "Only K is turned", "Neither key is turned", "The biconditional's open-to-condition direction yields the conjunction."),
        item("Rules: If A then B; if B then C; if C then not A. Which proposition cannot be true in a consistent assignment?", "A", "B", "C", "Not A", "A would imply B, then C, then not A, contradicting A."),
        item("Exactly one of statements X and Y is true. X says 'Y is false.' Which assignments satisfy this?", "Both X true/Y false and X false/Y true", "X true and Y false only", "X false and Y true only", "Neither assignment", "If X is true, Y is false; if X is false, its assertion is false so Y is true. Both assignments satisfy exactly-one truth."),
        item("A sequence is defined by a1=2 and a(n+1)=2a(n)+1. What is a4?", "23", "15", "17", "31", "The terms are 2, 5, 11, 23."),
        item("In a tournament, A beat B, B beat C, and C beat A. What does this show about 'beat' as a relation?", "It is not transitive", "It is transitive", "It is symmetric", "It is reflexive", "A beat B and B beat C but A did not beat C, violating transitivity."),
    ]


def build_logic_items() -> dict[str, list[Item]]:
    easy = build_easy_items()
    medium = build_medium_items()
    hard = build_hard_items()

    if len(hard) != 22:
        raise ValueError(
            f"Expected 22 hard logic items, found {len(hard)}"
        )

    return {
        "easy": easy,
        "medium": medium,
        "hard": hard,
    }
