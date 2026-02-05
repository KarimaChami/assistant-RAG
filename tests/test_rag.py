# tests/test_rag.py
import pytest
from unittest.mock import patch, MagicMock

def test_ask_rag_returns_response():
    """Test avec mock du LLM"""
    with patch('src.utils.rag_service.llm') as mock_llm:
        # Mock de la réponse
        mock_response = MagicMock()
        mock_response.content = "Réponse de test"
        mock_llm.invoke.return_value = mock_response
        
        from src.utils.rag_service import ask_rag
        
        question = "Comment redémarrer un serveur ?"
        response, latency_ms = ask_rag(question)
        
        assert response == "Réponse de test"
        assert latency_ms > 0

def test_ask_rag_latency():
    """Test de la latence avec mock"""
    with patch('src.utils.rag_service.llm') as mock_llm:
        mock_response = MagicMock()
        mock_response.content = "Réponse rapide"
        mock_llm.invoke.return_value = mock_response
        
        from src.utils.rag_service import ask_rag
        
        question = "Test latence"
        response, latency_ms = ask_rag(question)
        
        assert latency_ms > 0
        assert latency_ms < 10000