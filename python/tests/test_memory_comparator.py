import unittest
from unittest.mock import patch, MagicMock
import sys
import importlib

class TestMemoryComparator(unittest.TestCase):
    def setUp(self):
        # Define mocks for all missing dependencies
        self.mock_modules = {
            'langchain_core': MagicMock(),
            'langchain_core.stores': MagicMock(),
            'langchain_core.embeddings': MagicMock(),
            'langchain_core.documents': MagicMock(),
            'langchain_community': MagicMock(),
            'langchain_community.vectorstores': MagicMock(),
            'langchain_community.docstore': MagicMock(),
            'langchain_community.docstore.in_memory': MagicMock(),
            'langchain_community.vectorstores.utils': MagicMock(),
            'langchain': MagicMock(),
            'langchain.storage': MagicMock(),
            'langchain.embeddings': MagicMock(),
            'python.helpers.faiss_loader': MagicMock(),
            'python.helpers.knowledge_import': MagicMock(),
            'python.helpers.log': MagicMock(),
            'agents': MagicMock(),
            'models': MagicMock(),
            'numpy': MagicMock(),
            'webcolors': MagicMock(),
            'python.helpers.print_style': MagicMock(),
        }

        # Start the patcher
        self.patcher = patch.dict(sys.modules, self.mock_modules)
        self.patcher.start()

        # Remove module from cache if it exists to force reload with mocks
        if 'python.helpers.memory' in sys.modules:
            del sys.modules['python.helpers.memory']

        # Import the module under test
        from python.helpers.memory import Memory
        self.Memory = Memory

    def tearDown(self):
        self.patcher.stop()
        # Clean up the module from sys.modules to prevent pollution
        if 'python.helpers.memory' in sys.modules:
            del sys.modules['python.helpers.memory']

    def test_comparator_basic(self):
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
        condition = "x > " # Invalid
        comparator = self.Memory._get_comparator(condition)
        self.assertFalse(comparator({"x": 10}))

    def test_comparator_runtime_error(self):
        condition = "x > 10"
        comparator = self.Memory._get_comparator(condition)
        self.assertFalse(comparator({"y": 10}))

if __name__ == '__main__':
    unittest.main()
