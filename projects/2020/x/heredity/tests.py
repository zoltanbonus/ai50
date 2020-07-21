import unittest
from heredity import joint_probability, update, normalize

class TestPageRank(unittest.TestCase):
    def test_joint_probability(self):
        people = {
            'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False},
            'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
            'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None}
        }
        one_gene = { "Harry" }
        two_genes = { "James" }
        have_trait = { "James" }
        
        result = joint_probability(people, one_gene, two_genes, have_trait)

        self.assertEqual(result, 0.0026643247488)


    def test_update(self):
        people = {
            'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False},
            'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
            'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None}
        }        
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
        one_gene = { "James" }
        two_genes = { "Harry" }
        have_trait = { "Harry" }
        p = 0.665
        update(probabilities, one_gene, two_genes, have_trait, p)

        self.assertEqual(probabilities["Harry"]["gene"][0], 0)
        self.assertEqual(probabilities["Harry"]["gene"][1], 0)
        self.assertEqual(probabilities["Harry"]["gene"][2], p)
        self.assertEqual(probabilities["Harry"]["trait"][True], p)
        self.assertEqual(probabilities["Harry"]["trait"][False], 0)

        self.assertEqual(probabilities["Lily"]["gene"][0], p)
        self.assertEqual(probabilities["Lily"]["gene"][1], 0)
        self.assertEqual(probabilities["Lily"]["gene"][2], 0)
        self.assertEqual(probabilities["Lily"]["trait"][True], 0)
        self.assertEqual(probabilities["Lily"]["trait"][False], p)

        self.assertEqual(probabilities["James"]["gene"][0], 0)
        self.assertEqual(probabilities["James"]["gene"][1], p)
        self.assertEqual(probabilities["James"]["gene"][2], 0)
        self.assertEqual(probabilities["James"]["trait"][True], 0)
        self.assertEqual(probabilities["James"]["trait"][False], p)


    def test_normalize_traits(self):
        probabilities = {
            "Harry": {
                "gene": {
                    2: 0,
                    1: 0,
                    0: 0
                },
                "trait": {
                    True: 0.1,
                    False: 0.3
                }
            }
        }  

        normalize(probabilities)

        self.assertEqual(probabilities["Harry"]["trait"][True], 0.25)
        self.assertEqual(probabilities["Harry"]["trait"][False], 0.75)


    def test_normalize_genes(self):
        probabilities = {
            "Harry": {
                "gene": {
                    2: 0.1,
                    1: 0.1,
                    0: 0.1
                },
                "trait": {
                    True: 0.1,
                    False: 0.3
                }
            }
        }  

        normalize(probabilities)

        self.assertEqual(probabilities["Harry"]["gene"][0], 0.3333333333333333)
        self.assertEqual(probabilities["Harry"]["gene"][1], 0.3333333333333333)
        self.assertEqual(probabilities["Harry"]["gene"][2], 0.3333333333333333)


if __name__ == '__main__':
    unittest.main()