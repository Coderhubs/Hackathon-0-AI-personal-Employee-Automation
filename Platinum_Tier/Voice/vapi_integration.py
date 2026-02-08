#!/usr/bin/env python3
"""
Vapi Voice Integration - Platinum Tier
Handles inbound/outbound calls for appointment setting
"""

import os
import json
import asyncio
from datetime import datetime
from pathlib import Path
import logging
import aiohttp
from typing import Dict, Optional

class VapiIntegration:
    """
    Vapi AI Voice Integration

    Features:
    - Inbound call handling
    - Outbound call initiation
    - Call transcription
    - Appointment setting automation
    - Call logging and analytics
    """

    def __init__(self, base_dir="Platinum_Tier"):
        self.base_dir = Path(base_dir)
        self.logs = self.base_dir / "Logs"
        self.voice_logs = self.base_dir / "Voice" / "call_logs"
        self.voice_logs.mkdir(parents=True, exist_ok=True)

        # Vapi credentials
        self.api_key = os.getenv('VAPI_API_KEY')
        self.phone_number = os.getenv('VAPI_PHONE_NUMBER')
        self.assistant_id = os.getenv('VAPI_ASSISTANT_ID')

        self.base_url = "https://api.vapi.ai"

        self.setup_logging()

    def setup_logging(self):
        """Setup logging"""
        log_file = self.logs / f"vapi_{datetime.now().strftime('%Y%m%d')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('VapiIntegration')

    async def create_assistant(self, config: Dict) -> Optional[str]:
        """
        Create a Vapi assistant for handling calls.

        Args:
            config: Assistant configuration

        Returns:
            Assistant ID if successful
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }

                assistant_config = {
                    "name": config.get("name", "AI Employee Assistant"),
                    "voice": {
                        "provider": "11labs",
                        "voiceId": config.get("voice_id", "21m00Tcm4TlvDq8ikWAM")
                    },
                    "model": {
                        "provider": "openai",
                        "model": "gpt-4",
                        "messages": [
                            {
                                "role": "system",
                                "content": config.get("system_prompt",
                                    "You are a professional AI assistant helping with appointment scheduling. "
                                    "Be friendly, efficient, and gather: name, phone, email, preferred date/time, and reason for appointment.")
                            }
                        ]
                    },
                    "firstMessage": config.get("greeting",
                        "Hello! I'm calling to help schedule an appointment. May I have your name please?"),
                    "endCallMessage": config.get("goodbye",
                        "Thank you! Your appointment has been scheduled. You'll receive a confirmation shortly."),
                    "recordingEnabled": True,
                    "endCallFunctionEnabled": True
                }

                async with session.post(
                    f"{self.base_url}/assistant",
                    headers=headers,
                    json=assistant_config
                ) as response:
                    if response.status == 201:
                        data = await response.json()
                        assistant_id = data.get('id')
                        self.logger.info(f"Assistant created: {assistant_id}")
                        return assistant_id
                    else:
                        error = await response.text()
                        self.logger.error(f"Failed to create assistant: {error}")
                        return None

        except Exception as e:
            self.logger.error(f"Error creating assistant: {e}")
            return None

    async def make_outbound_call(self, phone_number: str, assistant_id: str, context: Dict = None) -> Optional[str]:
        """
        Initiate an outbound call.

        Args:
            phone_number: Phone number to call
            assistant_id: Vapi assistant ID
            context: Additional context for the call

        Returns:
            Call ID if successful
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }

                call_config = {
                    "assistantId": assistant_id,
                    "phoneNumberId": self.phone_number,
                    "customer": {
                        "number": phone_number
                    }
                }

                if context:
                    call_config["assistantOverrides"] = {
                        "variableValues": context
                    }

                async with session.post(
                    f"{self.base_url}/call/phone",
                    headers=headers,
                    json=call_config
                ) as response:
                    if response.status == 201:
                        data = await response.json()
                        call_id = data.get('id')
                        self.logger.info(f"Outbound call initiated: {call_id} to {phone_number}")

                        # Log call
                        await self.log_call({
                            'call_id': call_id,
                            'type': 'outbound',
                            'phone_number': phone_number,
                            'assistant_id': assistant_id,
                            'timestamp': datetime.now().isoformat(),
                            'status': 'initiated'
                        })

                        return call_id
                    else:
                        error = await response.text()
                        self.logger.error(f"Failed to initiate call: {error}")
                        return None

        except Exception as e:
            self.logger.error(f"Error making outbound call: {e}")
            return None

    async def handle_webhook(self, webhook_data: Dict) -> Dict:
        """
        Handle Vapi webhook events.

        Args:
            webhook_data: Webhook payload from Vapi

        Returns:
            Response dict
        """
        try:
            event_type = webhook_data.get('message', {}).get('type')
            call_id = webhook_data.get('message', {}).get('call', {}).get('id')

            self.logger.info(f"Webhook received: {event_type} for call {call_id}")

            if event_type == 'transcript':
                # Handle call transcript
                await self.process_transcript(webhook_data)

            elif event_type == 'function-call':
                # Handle function call (e.g., schedule appointment)
                return await self.handle_function_call(webhook_data)

            elif event_type == 'end-of-call-report':
                # Handle end of call
                await self.process_call_end(webhook_data)

            elif event_type == 'status-update':
                # Handle status update
                await self.update_call_status(webhook_data)

            return {'status': 'success'}

        except Exception as e:
            self.logger.error(f"Error handling webhook: {e}")
            return {'status': 'error', 'message': str(e)}

    async def process_transcript(self, data: Dict):
        """Process call transcript"""
        try:
            transcript = data.get('message', {}).get('transcript', '')
            call_id = data.get('message', {}).get('call', {}).get('id')
            role = data.get('message', {}).get('role')  # 'assistant' or 'user'

            # Save transcript
            transcript_file = self.voice_logs / f"{call_id}_transcript.txt"
            with open(transcript_file, 'a', encoding='utf-8') as f:
                f.write(f"[{role.upper()}] {transcript}\n")

            self.logger.info(f"Transcript saved for call {call_id}")

        except Exception as e:
            self.logger.error(f"Error processing transcript: {e}")

    async def handle_function_call(self, data: Dict) -> Dict:
        """
        Handle function calls from Vapi (e.g., schedule appointment).

        Returns:
            Function response
        """
        try:
            function_call = data.get('message', {}).get('functionCall', {})
            function_name = function_call.get('name')
            parameters = function_call.get('parameters', {})

            self.logger.info(f"Function call: {function_name} with params: {parameters}")

            if function_name == 'schedule_appointment':
                # Extract appointment details
                appointment = {
                    'name': parameters.get('name'),
                    'phone': parameters.get('phone'),
                    'email': parameters.get('email'),
                    'date': parameters.get('date'),
                    'time': parameters.get('time'),
                    'reason': parameters.get('reason'),
                    'timestamp': datetime.now().isoformat()
                }

                # Save appointment to Needs_Action for processing
                appointment_file = self.base_dir / "Needs_Action" / f"APPOINTMENT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(appointment_file, 'w', encoding='utf-8') as f:
                    json.dump(appointment, f, indent=2)

                self.logger.info(f"Appointment scheduled: {appointment}")

                return {
                    'result': {
                        'success': True,
                        'message': f"Appointment scheduled for {appointment['name']} on {appointment['date']} at {appointment['time']}"
                    }
                }

            return {'result': {'success': False, 'message': 'Unknown function'}}

        except Exception as e:
            self.logger.error(f"Error handling function call: {e}")
            return {'result': {'success': False, 'message': str(e)}}

    async def process_call_end(self, data: Dict):
        """Process end of call report"""
        try:
            call = data.get('message', {}).get('call', {})
            call_id = call.get('id')
            duration = call.get('duration')
            cost = call.get('cost')

            # Save call summary
            summary = {
                'call_id': call_id,
                'duration': duration,
                'cost': cost,
                'ended_at': datetime.now().isoformat(),
                'summary': call.get('summary', '')
            }

            summary_file = self.voice_logs / f"{call_id}_summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2)

            self.logger.info(f"Call ended: {call_id}, duration: {duration}s, cost: ${cost}")

        except Exception as e:
            self.logger.error(f"Error processing call end: {e}")

    async def update_call_status(self, data: Dict):
        """Update call status"""
        try:
            status = data.get('message', {}).get('status')
            call_id = data.get('message', {}).get('call', {}).get('id')

            await self.log_call({
                'call_id': call_id,
                'status': status,
                'timestamp': datetime.now().isoformat()
            })

        except Exception as e:
            self.logger.error(f"Error updating call status: {e}")

    async def log_call(self, call_data: Dict):
        """Log call information"""
        try:
            call_id = call_data.get('call_id')
            log_file = self.voice_logs / f"{call_id}_log.json"

            # Append to existing log or create new
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
                existing.update(call_data)
                call_data = existing

            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(call_data, f, indent=2)

        except Exception as e:
            self.logger.error(f"Error logging call: {e}")

    async def get_call_analytics(self, days: int = 7) -> Dict:
        """
        Get call analytics for the last N days.

        Returns:
            Analytics dict with call statistics
        """
        try:
            # Count calls, duration, cost, etc.
            total_calls = 0
            total_duration = 0
            total_cost = 0.0

            for log_file in self.voice_logs.glob("*_summary.json"):
                with open(log_file, 'r', encoding='utf-8') as f:
                    summary = json.load(f)
                    total_calls += 1
                    total_duration += summary.get('duration', 0)
                    total_cost += summary.get('cost', 0.0)

            analytics = {
                'total_calls': total_calls,
                'total_duration_seconds': total_duration,
                'total_cost': total_cost,
                'average_duration': total_duration / total_calls if total_calls > 0 else 0,
                'average_cost': total_cost / total_calls if total_calls > 0 else 0
            }

            return analytics

        except Exception as e:
            self.logger.error(f"Error getting analytics: {e}")
            return {}

if __name__ == "__main__":
    # Test Vapi integration
    vapi = VapiIntegration()

    # Example: Create assistant
    config = {
        "name": "Appointment Scheduler",
        "system_prompt": "You are a professional appointment scheduler. Be friendly and efficient."
    }

    asyncio.run(vapi.create_assistant(config))
