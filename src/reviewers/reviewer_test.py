import unittest
from unittest.mock import patch, Mock
from .reviewer import OopsPitfallReviewer
import os

class TestOopsPitfallReviewer(unittest.TestCase):
    def setUp(self):
        self.reviewer = OopsPitfallReviewer(endpoint="http://localhost/OOPS/rest")

    @patch('src.reviewers.reviewer.requests.post')
    def test_review_owl_content(self, mock_post):
        # Arrange
        mock_response = Mock()
        mock_response.text = '<OOPSResponse>Success</OOPSResponse>'
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        owl_content = '<rdf:RDF></rdf:RDF>'
        pitfalls = ['P01', 'P02']
        # Act
        result = self.reviewer.review_owl_content(owl_content, pitfalls=pitfalls, output_format="XML")
        # Print the result to the console
        print("review_owl_content result:", result)
        # Assert
        self.assertIn('Success', result)
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertIn('application/xml', kwargs['headers']['Content-Type'])
        self.assertIn('P01,P02', kwargs['data'].decode('utf-8'))

    @patch('src.reviewers.reviewer.requests.post')
    def test_review_owl_file(self, mock_post):
        # Arrange
        mock_response = Mock()
        mock_response.text = '<OOPSResponse>FileSuccess</OOPSResponse>'
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        # Instead of reading a file, mock the method that reads the file
        test_content = '<rdf:RDF></rdf:RDF>'
        with patch.object(self.reviewer, 'review_owl_content', return_value=mock_response.text) as mock_review_content:
            result = self.reviewer.review_owl_content(test_content, pitfalls=None, output_format="XML")
            print("review_owl_file (mocked) result:", result)
            self.assertIn('FileSuccess', result)
            mock_review_content.assert_called_once_with(test_content, pitfalls=None, output_format="XML")

    def test_review_owl_content_real_api(self):
        # python -m unittest src.reviewers.reviewer_test.TestOopsPitfallReviewer.test_review_owl_content_real_api
        owl_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "output", "backup", "debug_owl_content_turtle_combined_owl.xml")

        with open(owl_file_path, "r", encoding="utf-8") as f:
            owl_content = f.read()
 
       
        pitfalls = ['2,3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 19, 20, 21, 22, 24, 25, 25, 26, 27, 28, 29']
        # Act
        result = self.reviewer.review_owl_content(owl_content, pitfalls=pitfalls, output_format="XML")
        print("review_owl_content_real_api result:", result)
        self.assertIn("OOPS", result)  # The response should contain OOPS if the API is up
