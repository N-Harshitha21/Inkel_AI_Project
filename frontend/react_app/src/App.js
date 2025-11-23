import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import TourismAssistant from './components/TourismAssistant';
import ApiStatus from './components/ApiStatus';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
`;

const MainCard = styled.div`
  max-width: 900px;
  margin: 0 auto;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  overflow: hidden;
`;

const Header = styled.div`
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  padding: 40px 30px;
  text-align: center;
`;

const Title = styled.h1`
  font-size: 3rem;
  margin-bottom: 15px;
  font-weight: 700;
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  opacity: 0.95;
  font-weight: 300;
`;

const ContentArea = styled.div`
  padding: 40px;
`;

const Footer = styled.div`
  background: #f8f9fa;
  padding: 25px;
  text-align: center;
  color: #666;
  border-top: 1px solid #e1e5e9;
  font-size: 0.9rem;
`;

function App() {
  const [apiStatus, setApiStatus] = useState('checking');

  const checkApiStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/health');
      if (response.ok) {
        setApiStatus('online');
      } else {
        setApiStatus('offline');
      }
    } catch (error) {
      setApiStatus('offline');
    }
  };

  useEffect(() => {
    checkApiStatus();
    // Check API status every 30 seconds
    const interval = setInterval(checkApiStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <AppContainer>
      <MainCard>
        <Header>
          <Title>🌍 AI Tourism Assistant</Title>
          <Subtitle>
            Discover weather conditions and amazing places to visit worldwide!
          </Subtitle>
        </Header>
        
        <ContentArea>
          <ApiStatus status={apiStatus} onRetry={checkApiStatus} />
          <TourismAssistant apiStatus={apiStatus} />
        </ContentArea>
        
        <Footer>
          <p>
            <strong>Powered by Multi-Agent AI System</strong><br />
            Weather: Open-Meteo | Places: OpenStreetMap | Geocoding: Nominatim
          </p>
        </Footer>
      </MainCard>
    </AppContainer>
  );
}

export default App;