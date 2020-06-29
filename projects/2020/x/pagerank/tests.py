import unittest
from pagerank import transition_model, sample_pagerank, iterate_pagerank, links_to_page

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
        
        self.assertEqual(1, round(sum(result.values()), 3))

    def test_links_top_page_1(self):
        corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
        page = "1.html"
        expected = set()

        self.assertEqual(expected, links_to_page(corpus, page))


    def test_links_top_page_2(self):
        corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
        page = "2.html"
        expected = {"1.html", "3.html"}

        self.assertEqual(expected, links_to_page(corpus, page))


    def test_links_top_page_3(self):
        corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
        page = "3.html"
        expected = {"1.html", "2.html"}

        self.assertEqual(expected, links_to_page(corpus, page))
        

    def test_iterate_pagerank(self):
        corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
        damping_factor = 0.85

        result = iterate_pagerank(corpus, damping_factor)
        self.assertEqual(1, round(sum(result.values()), 4))

        
    def test_iterate_pagerank_corpus0(self):
        corpus = {"1.html": {"2.html"}, "2.html": {"1.html", "3.html"}, "3.html": {"2.html", "4.html"}, "4.html": {"2.html"}}
        damping_factor = 0.85

        result = iterate_pagerank(corpus, damping_factor)
        self.assertEqual(1, round(sum(result.values()), 4))
        self.assertEqual(0.2202, round(result["1.html"], 4))
        self.assertEqual(0.4289, round(result["2.html"], 4))
        self.assertEqual(0.2202, round(result["3.html"], 4))
        self.assertEqual(0.1307, round(result["4.html"], 4))


if __name__ == '__main__':
    unittest.main()