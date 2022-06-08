
import unittest 
import genome
import numpy as np
import os

class GenomeTest (unittest.TestCase):
    def testClassExists(self):
        self.assertIsNotNone(genome.Genome)


    def testClassExists(self):
        self.assertIsNotNone(genome.Genome)

    def testRandomGene(self):
        self.assertIsNotNone(genome.Genome.get_random_gene)

    def testRandomGeneNotNone(self):
        self.assertIsNotNone(genome.Genome.get_random_gene(5))

    def testRandomGeneHasValues(self):
        gene = genome.Genome.get_random_gene(5)
        self.assertIsNotNone(gene[0])

    def testRandomGeneLength(self):
        gene = genome.Genome.get_random_gene(20)
        self.assertEqual(len(gene), 20)

    def testRandGeneIsNumpyArrays(self):
        gene = genome.Genome.get_random_gene(20)
        self.assertEqual(type(gene), np.ndarray)

    def testRandomGenomeExists(self):
        data = genome.Genome.get_random_genome(20, 5)
        self.assertIsNotNone(data)

    def testGeneSpecExist(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec)
    
    def testGeneSpecHasLinkLength(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec['link-length'])

    def testGeneSpecHasLinkLength(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec['link-length']["ind"])

    def testGeneSpecScale(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(20)
        self.assertGreater(gene[spec["link-length"]["ind"]], 0)


    def testGeneToGeneDict(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(len(spec))
        gene_dict = genome.Genome.get_gene_dict(gene, spec)
        self.assertIn("link-recurrence", gene_dict)

    def testGenomeToDict(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)
        self.assertEqual(len(genome_dicts), 3)

    def testFlatLinks(self):
        links = [
          genome.URDFLink(name="A", parent_name=None, recur=1), 
          genome.URDFLink(name="B", parent_name="A", recur=2), 
          genome.URDFLink(name="C", parent_name="B", recur=2)
        ]
        self.assertIsNotNone(links)

    def testExpandLinks(self):
        links = [
            genome.URDFLink(name="A", parent_name="None", recur=1), 
            genome.URDFLink(name="B", parent_name="A", recur=1), 
            genome.URDFLink(name="C", parent_name="B", recur=2), 
            genome.URDFLink(name="D", parent_name="C", recur=1), 
        ]
        exp_links = [links[0]]
        genome.Genome.expandLinks(links[0], links[0].name, links, exp_links)   
        self.assertEqual(len(exp_links), 6)

    def testCrossover(self):
        g1 = [[1], [2], [3]]
        g2 = [[4], [5], [6]]
        for i in range(10):
            g3 = genome.Genome.crossover(g1, g2)
            self.assertGreater(len(g3), 0)
    
    def test_point(self):
        g1 = np.array([[1.0], [2.0], [3.0]])
        g2 = genome.Genome.point_mutate(g1, rate=1, amount=0.25)
        self.assertFalse(np.array_equal(g1, g2))
    
    def test_point_range(self):
        g1 = np.array([[1.0], [0.0], [1.0], [0.0]])
        for i in range(100):
            g2 = genome.Genome.point_mutate(g1, rate=1, amount=0.25)
            self.assertLessEqual(np.max(g2), 1.0)
            self.assertGreaterEqual(np.min(g2), 0.0)
    
    def test_shrink(self):
        g1 = np.array([[1.0], [2.0]])
        g2 = genome.Genome.shrink_mutate(g1, rate=1.0)
        # should def. shrink as rate = 1
        self.assertEqual(len(g2), 1) 

    def test_shrink2(self):
        g1 = np.array([[1.0], [2.0]])
        g2 = genome.Genome.shrink_mutate(g1, rate=0.0)
        # should not shrink as rate = 0
        self.assertEqual(len(g2), 2) 

    def test_shrink3(self):
        g1 = np.array([[1.0]])
        g2 = genome.Genome.shrink_mutate(g1, rate=1.0)
        # should not shrink if already len 1
        self.assertEqual(len(g2), 1) 
    
    def test_grow1(self):
        g1 = np.array([[1.0], [2.0]])
        g2 = genome.Genome.grow_mutate(g1, rate=1)
        self.assertGreater(len(g2), len(g1))

    def test_grow2(self):
        g1 = np.array([[1.0], [2.0]])
        g2 = genome.Genome.grow_mutate(g1, rate=0)
        self.assertEqual(len(g2), len(g1))

    def test_tocsv(self):
        g1 = [[1,2,3]]
        genome.Genome.to_csv(g1, 'test.csv')
        self.assertTrue(os.path.exists('test.csv'))

    def test_tocsv_content(self):
        g1 = [[1,2,3]]
        genome.Genome.to_csv(g1, 'test.csv')
        expect = "1,2,3,\n"
        with open('test.csv') as f:
            csv_str = f.read() 
        self.assertEqual(csv_str, expect)

    def test_tocsv_content2(self):
        g1 = [[1,2,3], [4,5,6]]
        genome.Genome.to_csv(g1, 'test.csv')
        expect = "1,2,3,\n4,5,6,\n"
        with open('test.csv') as f:
            csv_str = f.read() 
        self.assertEqual(csv_str, expect)

    def test_from_csv(self):
        g1 = [[1,2,3]]
        genome.Genome.to_csv(g1, 'test.csv')
        g2 = genome.Genome.from_csv('test.csv')
        print(g1, g2)
        self.assertTrue(np.array_equal(g1, g2))

    def test_from_csv2(self):
        g1 = [[1,2,3], [4,5,6]]
        genome.Genome.to_csv(g1, 'test.csv')
        g2 = genome.Genome.from_csv('test.csv')
        print(g1, g2)
        self.assertTrue(np.array_equal(g1, g2))

unittest.main()
