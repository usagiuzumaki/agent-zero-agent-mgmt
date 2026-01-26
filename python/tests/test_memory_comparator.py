import unittest
import sys
from unittest.mock import MagicMock, patch

class TestMemoryComparator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Mock dependencies required for Memory import
        # We mock the modules that are missing in the test environment
        cls.module_patcher = patch.dict(sys.modules, {
            "langchain_core": MagicMock(),
            "langchain_core.stores": MagicMock(),
            "langchain.storage": MagicMock(),
            "langchain.embeddings": MagicMock(),
            "python.helpers.faiss_loader": MagicMock(),
            "python.helpers.faiss_loader.faiss": MagicMock(),
            "langchain_community": MagicMock(),
            "langchain_community.vectorstores": MagicMock(),
            "langchain_community.docstore.in_memory": MagicMock(),
            "langchain_community.vectorstores.utils": MagicMock(),
            "langchain_core.embeddings": MagicMock(),
            "python.helpers.knowledge_import": MagicMock(),
            "agents": MagicMock(),
            "models": MagicMock(),
            "langchain_core.documents": MagicMock(),
            "numpy": MagicMock(),
            "webcolors": MagicMock(),
            "regex": MagicMock(),
        })
        cls.module_patcher.start()

        # Import Memory after mocks are in place
        try:
            from python.helpers.memory import Memory
            cls.Memory = Memory
        except ImportError as e:
            # If it still fails, we'll see the error when running tests
            print(f"Failed to import Memory in setUpClass: {e}")
            cls.Memory = None

    @classmethod
    def tearDownClass(cls):
        cls.module_patcher.stop()

    def test_comparator_basic(self):
        if self.Memory is None:
            self.fail("Could not import Memory module")
        condition = "x > 10"
        comparator = self.Memory._get_comparator(condition)
        self.assertTrue(comparator({"x": 11}))
        self.assertFalse(comparator({"x": 10}))
        self.assertFalse(comparator({"x": 9}))

    def test_comparator_string(self):
        condition = "name == 'Alice'"
        comparator = self.Memory._get_comparator(condition)
        self.assertTrue(comparator({"name": "Alice"}))
        self.assertFalse(comparator({"name": "Bob"}))

    def test_comparator_compound(self):
        condition = "x > 10 and y < 5"
        comparator = self.Memory._get_comparator(condition)
        self.assertTrue(comparator({"x": 11, "y": 4}))
        self.assertFalse(comparator({"x": 11, "y": 5}))
        self.assertFalse(comparator({"x": 10, "y": 4}))

    def test_comparator_invalid_syntax(self):
        # Should handle invalid syntax gracefully
        condition = "x > " # Invalid
        comparator = self.Memory._get_comparator(condition)
        # Should return a function that returns False safely
        self.assertFalse(comparator({"x": 10}))

    def test_comparator_runtime_error(self):
        # Should handle runtime errors during evaluation
        condition = "x > 10"
        comparator = self.Memory._get_comparator(condition)
        # Missing key 'x'
        self.assertFalse(comparator({"y": 10}))

if __name__ == '__main__':
    unittest.main()
