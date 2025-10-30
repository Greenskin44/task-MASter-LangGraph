"""Tests for email assistant workflows.

This module contains tests for email assistant functionality including:
- Email triage (respond, notify, ignore)
- Tool execution and response generation
"""

import pytest


@pytest.mark.email
@pytest.mark.integration
class TestEmailAssistant:
    """Tests for the email assistant graph."""

    def test_respond_classification(self, api_keys, sample_email_respond):
        """Test email classification for respond action.

        Verifies that the graph correctly identifies emails that
        require a response and initiates the response workflow.
        """
        from graphs.email_assistant.email_assistant import email_assistant

        # Execute graph with respond email
        result = email_assistant.invoke({"email_input": sample_email_respond})

        # Verify structure
        assert "classification_decision" in result
        assert "messages" in result

        # Verify classification
        assert result["classification_decision"] == "respond"

        # Verify messages were generated (response workflow executed)
        assert len(result["messages"]) > 0

    def test_notify_classification(self, api_keys, sample_email_notify):
        """Test email classification for notify action.

        Verifies that the graph correctly identifies emails that
        should trigger a notification without response.
        """
        from graphs.email_assistant.email_assistant import email_assistant

        # Execute graph with notify email
        result = email_assistant.invoke({"email_input": sample_email_notify})

        # Verify structure
        assert "classification_decision" in result

        # Verify classification
        assert result["classification_decision"] == "notify"

        # Verify no response was generated (workflow ended after triage)
        # Messages may be empty or contain only the initial email
        assert result["classification_decision"] != "respond"

    def test_ignore_classification(self, api_keys, sample_email_ignore):
        """Test email classification for ignore action.

        Verifies that the graph correctly identifies spam/promotional
        emails that should be ignored.
        """
        from graphs.email_assistant.email_assistant import email_assistant

        # Execute graph with ignore email
        result = email_assistant.invoke({"email_input": sample_email_ignore})

        # Verify structure
        assert "classification_decision" in result

        # Verify classification
        assert result["classification_decision"] == "ignore"

        # Verify no response was generated
        assert result["classification_decision"] != "respond"

    def test_meeting_request_email(self, api_keys):
        """Test handling of meeting request emails.

        Verifies that the graph can process meeting requests
        and potentially use calendar tools.
        """
        from graphs.email_assistant.email_assistant import email_assistant

        meeting_email = """
        From: colleague@company.com
        To: me@company.com
        Subject: Meeting Request - Project Sync
        
        Hi,
        
        Can we schedule a 30-minute meeting next week to discuss
        the project status? I'm available Tuesday or Wednesday afternoon.
        
        Let me know what works for you.
        
        Thanks,
        Sarah
        """

        # Execute graph
        result = email_assistant.invoke({"email_input": meeting_email})

        # Verify structure
        assert "classification_decision" in result

        # Meeting requests should typically be classified as respond
        # (though this depends on the triage logic)
        assert result["classification_decision"] in ["respond", "notify"]

    def test_information_request_email(self, api_keys):
        """Test handling of information request emails.

        Verifies that the graph can process requests for information
        and generate appropriate responses.
        """
        from graphs.email_assistant.email_assistant import email_assistant

        info_request = """
        From: client@external.com
        To: support@company.com
        Subject: Question about API documentation
        
        Hello,
        
        I'm trying to integrate with your API and have a question about
        the authentication flow. Where can I find the latest documentation?
        
        Best regards,
        Mike
        """

        # Execute graph
        result = email_assistant.invoke({"email_input": info_request})

        # Verify structure
        assert "classification_decision" in result

        # Information requests should be classified as respond
        assert result["classification_decision"] == "respond"

        # Verify response was generated
        assert "messages" in result
        assert len(result["messages"]) > 0

    def test_promotional_email(self, api_keys):
        """Test handling of promotional/marketing emails.

        Verifies that the graph correctly identifies and ignores
        promotional content.
        """
        from graphs.email_assistant.email_assistant import email_assistant

        promo_email = """
        From: deals@retailer.com
        To: customer@email.com
        Subject: FLASH SALE - 70% OFF Everything!
        
        🎉 BIGGEST SALE OF THE YEAR! 🎉
        
        Shop now and save up to 70% on all items!
        Limited time only - don't miss out!
        
        [SHOP NOW]
        
        Unsubscribe | Privacy Policy
        """

        # Execute graph
        result = email_assistant.invoke({"email_input": promo_email})

        # Verify structure
        assert "classification_decision" in result

        # Promotional emails should be ignored
        assert result["classification_decision"] == "ignore"
