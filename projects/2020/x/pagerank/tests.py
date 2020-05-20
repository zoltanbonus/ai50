import unittest
from pagerank import transition_model, sample_pagerank

class TestPageRank(unittest.TestCase):
    def test_transition_model_example(self):
        corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
        page = "1.html"
        damping_factor = 0.85
        expected = {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}

        result = transition_model(corpus, page, damping_factor)

        self.assertEqual(result, expected)

    def test_transition_model_no_links(self):
        corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}, "4.html": {}}
        page = "4.html"
        damping_factor = 0.85
        expected = {"1.html": 0.25, "2.html": 0.25, "3.html": 0.25, "4.html": 0.25}

        result = transition_model(corpus, page, damping_factor)

        self.assertEqual(result, expected)

    def test_transition_model_random(self):
        corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
        page = "2.html"
        damping_factor = 0.85
        expected = {"1.html": 0.05, "2.html": 0.05, "3.html": 0.9}

        result = transition_model(corpus, page, damping_factor)

        self.assertEqual(result, expected)

    def test_sample_pagerank(self):
        corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
        damping_factor = 0.85
        n = 100
        result = sample_pagerank(corpus, damping_factor, n)



if __name__ == '__main__':
    unittest.main()