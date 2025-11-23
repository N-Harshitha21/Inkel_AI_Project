import React from 'react';
import styled from 'styled-components';

const StatusContainer = styled.div`
  background: ${props => 
    props.status === 'online' ? '#e8f5e8' : 
    props.status === 'offline' ? '#ffe8e8' : '#e8f4fd'};
  border-left: 4px solid ${props => 
    props.status === 'online' ? '#28a745' : 
    props.status === 'offline' ? '#dc3545' : '#007bff'};
  padding: 15px 20px;
  border-radius: 8px;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const StatusInfo = styled.div`
  display: flex;
  align-items: center;
`;

const StatusIndicator = styled.div`
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: ${props => 
    props.status === 'online' ? '#28a745' : 
    props.status === 'offline' ? '#dc3545' : '#6c757d'};
  margin-right: 12px;
  animation: ${props => props.status === 'checking' ? 'pulse 1.5s infinite' : 'none'};

  @keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
  }
`;

const StatusText = styled.span`
  font-weight: 500;
  color: ${props => 
    props.status === 'online' ? '#155724' : 
    props.status === 'offline' ? '#721c24' : '#004085'};
`;

const RetryButton = styled.button`
  background: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s;

  &:hover {
    background: #0056b3;
  }

  &:disabled {
    background: #6c757d;
    cursor: not-allowed;
  }
`;

const getStatusMessage = (status) => {
  switch(status) {
    case 'online':
      return '✅ API is online and ready';
    case 'offline':
      return '❌ API is offline - Please start the backend server';
    case 'checking':
      return '🔄 Checking API connection...';
    default:
      return '❓ Unknown status';
  }
};

function ApiStatus({ status, onRetry }) {
  return (
    <StatusContainer status={status}>
      <StatusInfo>
        <StatusIndicator status={status} />
        <StatusText status={status}>
          {getStatusMessage(status)}
        </StatusText>
      </StatusInfo>
      {status === 'offline' && (
        <RetryButton onClick={onRetry}>
          Retry Connection
        </RetryButton>
      )}
    </StatusContainer>
  );
}

export default ApiStatus;