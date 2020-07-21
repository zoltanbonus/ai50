import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    probabilities = set()

    for person in people:
        genes = number_of_genes(person, one_gene, two_genes)
        trait = has_trait(person, have_trait)
        trait_prob = PROBS["trait"][genes][trait]
       
        mother = people[person]["mother"]
        father = people[person]["father"]
        
        gene_prob = 1
        if mother == None and father == None:
            gene_prob = PROBS["gene"][genes]
        else:
            mother_genes = number_of_genes(mother, one_gene, two_genes)            
            father_genes = number_of_genes(father, one_gene, two_genes)
            
            mother_heredity_prob = heredity_probability(mother_genes)
            father_heredity_prob = heredity_probability(father_genes)

            # Case 1: gets the gene from his mother and NOT his father
            prob1 = mother_heredity_prob * (1-father_heredity_prob)

            # Case 2: gets the gene from his father and NOT his mother
            prob2 = father_heredity_prob * (1-mother_heredity_prob)

            gene_prob = prob1 + prob2

        probabilities.add(gene_prob * trait_prob)

    result = 1
    for prob in probabilities:
        result *= prob

    return result


def heredity_probability(genes):
    if genes == 0:
        return PROBS["mutation"]
    
    if genes == 1:
        return 0.5

    if genes == 2:
        return 1-PROBS["mutation"]


def number_of_genes(person, one_gene, two_genes):
    number_of_genes = 0
    if person in one_gene:
        number_of_genes = 1

    if person in two_genes:
        number_of_genes = 2

    return number_of_genes


def has_trait(person, have_trait):
    trait = False
    if person in have_trait:
        trait = True

    return trait


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        genes = number_of_genes(person, one_gene, two_genes)
        trait = has_trait(person, have_trait)
       
        probabilities[person]["gene"][genes] += p
        probabilities[person]["trait"][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        trait = probabilities[person]["trait"][True]
        no_trait = probabilities[person]["trait"][False]
        sum = trait + no_trait
        if sum != 0:
            multiplier = 1 / sum
            probabilities[person]["trait"][True] = trait * multiplier
            probabilities[person]["trait"][False] = no_trait * multiplier

        no_gene = probabilities[person]["gene"][0]
        one_gene = probabilities[person]["gene"][1]
        two_genes = probabilities[person]["gene"][2]
        sum = no_gene + one_gene + two_genes
        if sum != 0:
            multiplier = 1 / sum
            probabilities[person]["gene"][0] = no_gene * multiplier
            probabilities[person]["gene"][1] = one_gene * multiplier
            probabilities[person]["gene"][2] = two_genes * multiplier    


if __name__ == "__main__":
    main()
