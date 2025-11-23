import React, { useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';

const AssistantContainer = styled.div`
  margin-top: 20px;
`;

const InputSection = styled.div`
  margin-bottom: 30px;
`;

const InputGroup = styled.div`
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
`;

const QueryInput = styled.textarea`
  flex: 1;
  padding: 15px 20px;
  border: 2px solid #e1e5e9;
  border-radius: 15px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  min-height: 80px;
  transition: border-color 0.3s ease;

  &:focus {
    outline: none;
    border-color: #4facfe;
  }

  &::placeholder {
    color: #999;
  }
`;

const SubmitButton = styled.button`
  padding: 15px 25px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  border: none;
  border-radius: 15px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 120px;
  height: fit-content;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(79, 172, 254, 0.3);
  }

  &:disabled {
    background: #ccc;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
`;

const ExamplesSection = styled.div`
  margin-bottom: 30px;
`;

const ExamplesTitle = styled.h3`
  margin-bottom: 15px;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const ExampleItem = styled.div`
  background: #f8f9fa;
  padding: 12px 18px;
  margin: 8px 0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-left: 4px solid #4facfe;
  font-size: 0.95rem;

  &:hover {
    background: #e9ecef;
    transform: translateX(5px);
  }
`;

const ResponseSection = styled.div`
  margin-top: 30px;
`;

const ResponseContainer = styled.div`
  background: ${props => 
    props.type === 'loading' ? '#e8f4fd' :
    props.type === 'success' ? '#f0fff4' :
    props.type === 'error' ? '#fff5f5' : '#f8f9fa'};
  border-left: 5px solid ${props => 
    props.type === 'loading' ? '#007bff' :
    props.type === 'success' ? '#28a745' :
    props.type === 'error' ? '#dc3545' : '#6c757d'};
  border-radius: 12px;
  padding: 25px;
  margin-top: 20px;
  animation: slideIn 0.3s ease-out;

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;

const ResponseHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
  font-weight: 600;
  color: ${props => 
    props.type === 'loading' ? '#007bff' :
    props.type === 'success' ? '#155724' :
    props.type === 'error' ? '#721c24' : '#333'};
`;

const ResponseText = styled.div`
  font-size: 1.1rem;
  line-height: 1.8;
  white-space: pre-line;
  color: #2d3748;
`;

const PlaceInfo = styled.div`
  margin-top: 15px;
  padding: 10px 15px;
  background: rgba(79, 172, 254, 0.1);
  border-radius: 8px;
  font-size: 0.9rem;
  color: #0066cc;
`;

const API_BASE_URL = 'http://localhost:8000';

const exampleQueries = [
  "I'm going to go to Bangalore, let's plan my trip.",
  "I'm going to go to Paris, what is the temperature there?",
  "I'm going to go to Tokyo, what is the temperature there? And what are the places I can visit?",
  "I'm going to visit London, show me tourist attractions.",
  "I'm going to New York, what's the weather and what places can I visit?"
];

function TourismAssistant({ apiStatus }) {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    if (!query.trim()) {
      alert('Please enter a query!');
      return;
    }

    if (apiStatus !== 'online') {
      alert('API is not available. Please check the backend server.');
      return;
    }

    setIsLoading(true);
    setResponse({
      type: 'loading',
      text: '🤖 AI is processing your request...\nThis may take a few seconds as we fetch live data from multiple APIs.',
      placeName: null
    });

    try {
      const result = await axios.post(`${API_BASE_URL}/query`, {
        query: query
      }, {
        timeout: 30000
      });

      setResponse({
        type: 'success',
        text: result.data.response,
        placeName: result.data.place_name
      });
    } catch (error) {
      let errorMessage = 'Network Error: Unable to connect to the server.';
      
      if (error.response) {
        errorMessage = `Error: ${error.response.data.detail || 'Something went wrong'}`;
      } else if (error.request) {
        errorMessage = `Network Error: ${error.message}\n\nPlease make sure the backend server is running on ${API_BASE_URL}`;
      }

      setResponse({
        type: 'error',
        text: errorMessage,
        placeName: null
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleExampleClick = (example) => {
    setQuery(example);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      handleSubmit();
    }
  };

  const getResponseIcon = (type) => {
    switch(type) {
      case 'loading': return '⏳';
      case 'success': return '🎯';
      case 'error': return '❌';
      default: return '💬';
    }
  };

  const getResponseTitle = (type) => {
    switch(type) {
      case 'loading': return 'Processing Request';
      case 'success': return 'AI Assistant Response';
      case 'error': return 'Error Occurred';
      default: return 'Response';
    }
  };

  return (
    <AssistantContainer>
      <InputSection>
        <InputGroup>
          <QueryInput
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="e.g., I'm going to Paris, what's the weather and places to visit?"
            maxLength={500}
          />
          <SubmitButton 
            onClick={handleSubmit}
            disabled={isLoading || apiStatus !== 'online'}
          >
            {isLoading ? 'Processing...' : '🚀 Ask AI'}
          </SubmitButton>
        </InputGroup>
        <small style={{color: '#666'}}>
          💡 Tip: Press Ctrl+Enter to submit quickly
        </small>
      </InputSection>

      <ExamplesSection>
        <ExamplesTitle>
          💡 Try these example queries:
        </ExamplesTitle>
        {exampleQueries.map((example, index) => (
          <ExampleItem 
            key={index}
            onClick={() => handleExampleClick(example)}
          >
            {example}
          </ExampleItem>
        ))}
      </ExamplesSection>

      {response && (
        <ResponseSection>
          <ResponseContainer type={response.type}>
            <ResponseHeader type={response.type}>
              {getResponseIcon(response.type)}
              {getResponseTitle(response.type)}
            </ResponseHeader>
            <ResponseText>{response.text}</ResponseText>
            {response.placeName && response.type === 'success' && (
              <PlaceInfo>
                📍 Detected location: <strong>{response.placeName}</strong>
              </PlaceInfo>
            )}
          </ResponseContainer>
        </ResponseSection>
      )}
    </AssistantContainer>
  );
}

export default TourismAssistant;