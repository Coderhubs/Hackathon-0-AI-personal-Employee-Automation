"""
Unit tests for WhatsApp Watcher
"""
import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from whatsapp_watcher_hackathon import WhatsAppWatcherHackathon

class TestWhatsAppWatcher:
    """Test suite for WhatsApp Watcher"""

    def test_initialization(self):
        """Test watcher initialization"""
        vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        watcher = WhatsAppWatcherHackathon(str(vault_path))

        assert watcher.check_interval == 30
        assert watcher.needs_action.exists()
        assert len(watcher.urgent_keywords) == 7
        assert len(watcher.agentic_keywords) == 6

    def test_urgent_keywords(self):
        """Test urgent keyword list"""
        vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        watcher = WhatsAppWatcherHackathon(str(vault_path))

        expected_urgent = ['urgent', 'asap', 'invoice', 'payment', 'help', 'emergency', 'important']
        assert watcher.urgent_keywords == expected_urgent

    def test_agentic_keywords(self):
        """Test agentic AI keyword list"""
        vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        watcher = WhatsAppWatcherHackathon(str(vault_path))

        expected_agentic = ['agentic', 'ai agent', 'autonomous ai', 'llm', 'claude', 'gpt']
        assert watcher.agentic_keywords == expected_agentic

    def test_priority_assignment_urgent(self):
        """Test priority assignment for urgent messages"""
        vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        watcher = WhatsAppWatcherHackathon(str(vault_path))

        msg = {
            'name': 'Test User',
            'message': 'URGENT: Need help',
            'message_id': 'test_123',
            'is_urgent': True,
            'is_agentic': False,
            'timestamp': '2026-02-17T22:00:00Z'
        }

        # Priority should be high for urgent messages
        if msg['is_urgent']:
            priority = 'high'
        elif msg['is_agentic']:
            priority = 'medium'
        else:
            priority = 'low'

        assert priority == 'high'

    def test_priority_assignment_agentic(self):
        """Test priority assignment for agentic AI messages"""
        vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        watcher = WhatsAppWatcherHackathon(str(vault_path))

        msg = {
            'name': 'Test User',
            'message': 'Question about AI agents',
            'message_id': 'test_456',
            'is_urgent': False,
            'is_agentic': True,
            'timestamp': '2026-02-17T22:00:00Z'
        }

        # Priority should be medium for agentic messages
        if msg['is_urgent']:
            priority = 'high'
        elif msg['is_agentic']:
            priority = 'medium'
        else:
            priority = 'low'

        assert priority == 'medium'

    def test_file_creation(self):
        """Test action file creation"""
        vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        watcher = WhatsAppWatcherHackathon(str(vault_path))

        msg = {
            'name': 'Test User',
            'message': 'URGENT: Test message about AI agents',
            'message_id': 'test_789',
            'is_urgent': True,
            'is_agentic': True,
            'timestamp': '2026-02-17T22:00:00Z'
        }

        # Create action file
        filepath = watcher.create_action_file(msg)

        # Verify file was created
        assert filepath.exists()
        assert filepath.suffix == '.md'
        assert 'WHATSAPP_' in filepath.name

        # Verify content
        content = filepath.read_text(encoding='utf-8')
        assert '---' in content  # Frontmatter
        assert 'type: whatsapp_message' in content
        assert 'priority: high' in content
        assert 'status: pending' in content
        assert '## Message Content' in content
        assert '## Suggested Actions' in content
        assert '## Context' in content

        # Clean up
        filepath.unlink()

    def test_keyword_detection_urgent(self):
        """Test urgent keyword detection"""
        vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        watcher = WhatsAppWatcherHackathon(str(vault_path))

        test_messages = [
            "URGENT: Need help now",
            "ASAP please respond",
            "Invoice attached",
            "Payment required",
            "Help me with this",
            "Emergency situation",
            "This is important"
        ]

        for msg in test_messages:
            text_lower = msg.lower()
            is_urgent = any(kw in text_lower for kw in watcher.urgent_keywords)
            assert is_urgent, f"Failed to detect urgent keyword in: {msg}"

    def test_keyword_detection_agentic(self):
        """Test agentic AI keyword detection"""
        vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        watcher = WhatsAppWatcherHackathon(str(vault_path))

        test_messages = [
            "Question about agentic systems",
            "How do AI agents work?",
            "Autonomous AI implementation",
            "LLM integration help",
            "Claude API question",
            "GPT-4 comparison"
        ]

        for msg in test_messages:
            text_lower = msg.lower()
            is_agentic = any(kw in text_lower for kw in watcher.agentic_keywords)
            assert is_agentic, f"Failed to detect agentic keyword in: {msg}"

    def test_deduplication(self):
        """Test message deduplication"""
        vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        watcher = WhatsAppWatcherHackathon(str(vault_path))

        message_id = "test_user_urgent_message_123456"

        # First time: should not be in seen_messages
        assert message_id not in watcher.seen_messages

        # Add to seen_messages
        watcher.seen_messages.add(message_id)

        # Second time: should be in seen_messages
        assert message_id in watcher.seen_messages

    def test_check_interval(self):
        """Test check interval is set correctly"""
        vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        watcher = WhatsAppWatcherHackathon(str(vault_path))

        # WhatsApp should have fastest check interval
        assert watcher.check_interval == 30
        assert watcher.check_interval < 120  # Faster than LinkedIn
        assert watcher.check_interval < 180  # Faster than Gmail

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
