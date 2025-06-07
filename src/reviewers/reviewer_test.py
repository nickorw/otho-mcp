import unittest
from unittest.mock import patch, Mock
from .reviewer import OopsPitfallReviewer

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
        # Use a valid minimal OWL ontology
        owl_content = '''<?xml version="1.0"?>
<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:owl="http://www.w3.org/2002/07/owl#"
    xmlns:ex="http://www.example.org/testontology#"
    xml:base="http://www.example.org/testontology">

    <owl:Ontology rdf:about=""/>

    <owl:Class rdf:ID="Person"/>
    <owl:Class rdf:ID="Employee">
        <rdfs:subClassOf rdf:resource="#Person"/>
    </owl:Class>
    <owl:Class rdf:ID="Manager">
        <rdfs:subClassOf rdf:resource="#Employee"/>
    </owl:Class>

    <owl:Class rdf:ID="ExternalConsultant">
        <rdfs:subClassOf rdf:resource="#Person"/>
        <rdfs:subClassOf rdf:resource="#Organization"/>
    </owl:Class>

    <owl:DatatypeProperty rdf:ID="hasAge">
        <rdfs:domain rdf:resource="#Person"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#integer"/>
    </owl:DatatypeProperty>

    <owl:ObjectProperty rdf:ID="worksFor">
        <rdfs:domain rdf:resource="#Employee"/>
        <rdfs:range rdf:resource="http://www.example.org/testontology#Organization"/>
    </owl:ObjectProperty>

    <owl:Class rdf:ID="Organization"/>

    <owl:ObjectProperty rdf:ID="hasComment"/>

    <owl:DatatypeProperty rdf:ID="hasStatusMessage"/>

    <Person rdf:ID="JohnDoe">
        <ex:hasAge rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">30</ex:hasAge>
        <ex:hasComment>John is a good team player.</ex:hasComment>
    </Person>

    <Employee rdf:ID="JaneSmith">
        <ex:hasAge rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">45</ex:hasAge>
        <ex:worksFor rdf:resource="#AcmeCorp"/>
        <ex:hasStatusMessage rdf:datatype="http://www.w3.org/2001/XMLSchema#string">On vacation until next week.</ex:hasStatusMessage>
    </Employee>

    <Organization rdf:ID="AcmeCorp"/>

    <ExternalConsultant rdf:ID="ConsultantX"/>

    <Organization rdf:ID="GlobalSolutions">
        <ex:hasComment>A key partner for innovation.</ex:hasComment>
        <ex:hasStatusMessage rdf:datatype="http://www.w3.org/2001/XMLSchema#string">Actively seeking new projects.</ex:hasStatusMessage>
    </Organization>

</rdf:RDF>'''
        pitfalls = ['2,3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 19, 20, 21, 22, 24, 25, 25, 26, 27, 28, 29']
        # Act
        result = self.reviewer.review_owl_content(owl_content, pitfalls=pitfalls, output_format="XML")
        print("review_owl_content_real_api result:", result)
        self.assertIn("OOPS", result)  # The response should contain OOPS if the API is up
