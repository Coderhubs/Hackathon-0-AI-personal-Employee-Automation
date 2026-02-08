#!/usr/bin/env python3
"""
Security Module - Platinum Tier
Encryption and secrets management for cloud deployment
"""

import os
import base64
import json
from pathlib import Path
from typing import Dict, Optional
import logging
from datetime import datetime

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend

class SecretsManager:
    """
    Manages encrypted credentials and secrets.

    Features:
    - Encrypt/decrypt .env files
    - Secure credential storage
    - Key rotation support
    - Audit logging
    """

    def __init__(self, base_dir="Platinum_Tier"):
        self.base_dir = Path(base_dir)
        self.security_dir = self.base_dir / "Security"
        self.security_dir.mkdir(parents=True, exist_ok=True)

        self.key_file = self.security_dir / ".encryption_key"
        self.encrypted_env = self.security_dir / ".env.encrypted"
        self.audit_log = self.security_dir / "audit.log"

        self.cipher = None
        self.setup_logging()
        self.initialize_encryption()

    def setup_logging(self):
        """Setup audit logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.audit_log),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('SecretsManager')

    def generate_key(self, password: str, salt: bytes = None) -> bytes:
        """
        Generate encryption key from password.

        Args:
            password: Master password
            salt: Salt for key derivation (generated if None)

        Returns:
            Encryption key
        """
        if salt is None:
            salt = os.urandom(16)

        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    def initialize_encryption(self):
        """Initialize encryption with existing or new key"""
        try:
            # Check for existing key
            if self.key_file.exists():
                with open(self.key_file, 'rb') as f:
                    key = f.read()
                self.cipher = Fernet(key)
                self.logger.info("Loaded existing encryption key")
            else:
                # Generate new key
                master_password = os.getenv('MASTER_PASSWORD')
                if not master_password:
                    # Generate random key if no master password
                    key = Fernet.generate_key()
                    self.logger.warning("No MASTER_PASSWORD set, using random key")
                else:
                    key, salt = self.generate_key(master_password)
                    # Save salt for future use
                    salt_file = self.security_dir / ".salt"
                    with open(salt_file, 'wb') as f:
                        f.write(salt)

                # Save key
                with open(self.key_file, 'wb') as f:
                    f.write(key)

                # Secure permissions (Unix-like systems)
                try:
                    os.chmod(self.key_file, 0o600)
                except:
                    pass

                self.cipher = Fernet(key)
                self.logger.info("Generated new encryption key")

                self.audit_log_event("KEY_GENERATED", "New encryption key created")

        except Exception as e:
            self.logger.error(f"Error initializing encryption: {e}")
            raise

    def encrypt_env_file(self, env_file_path: str) -> bool:
        """
        Encrypt .env file.

        Args:
            env_file_path: Path to .env file

        Returns:
            True if successful
        """
        try:
            env_path = Path(env_file_path)

            if not env_path.exists():
                self.logger.error(f"File not found: {env_file_path}")
                return False

            # Read .env file
            with open(env_path, 'rb') as f:
                plaintext = f.read()

            # Encrypt
            encrypted = self.cipher.encrypt(plaintext)

            # Save encrypted version
            with open(self.encrypted_env, 'wb') as f:
                f.write(encrypted)

            self.logger.info(f"Encrypted {env_file_path}")
            self.audit_log_event("ENV_ENCRYPTED", f"Encrypted {env_file_path}")

            # Optionally delete original (commented out for safety)
            # env_path.unlink()

            return True

        except Exception as e:
            self.logger.error(f"Error encrypting env file: {e}")
            return False

    def decrypt_env_file(self, output_path: str = None) -> bool:
        """
        Decrypt .env file.

        Args:
            output_path: Where to save decrypted file (default: .env)

        Returns:
            True if successful
        """
        try:
            if not self.encrypted_env.exists():
                self.logger.error("No encrypted env file found")
                return False

            # Read encrypted file
            with open(self.encrypted_env, 'rb') as f:
                encrypted = f.read()

            # Decrypt
            plaintext = self.cipher.decrypt(encrypted)

            # Save decrypted version
            if output_path is None:
                output_path = self.base_dir / ".env"

            with open(output_path, 'wb') as f:
                f.write(plaintext)

            # Secure permissions
            try:
                os.chmod(output_path, 0o600)
            except:
                pass

            self.logger.info(f"Decrypted to {output_path}")
            self.audit_log_event("ENV_DECRYPTED", f"Decrypted to {output_path}")

            return True

        except Exception as e:
            self.logger.error(f"Error decrypting env file: {e}")
            return False

    def encrypt_string(self, plaintext: str) -> str:
        """
        Encrypt a string.

        Args:
            plaintext: String to encrypt

        Returns:
            Base64-encoded encrypted string
        """
        try:
            encrypted = self.cipher.encrypt(plaintext.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            self.logger.error(f"Error encrypting string: {e}")
            return None

    def decrypt_string(self, encrypted_str: str) -> str:
        """
        Decrypt a string.

        Args:
            encrypted_str: Base64-encoded encrypted string

        Returns:
            Decrypted plaintext
        """
        try:
            encrypted = base64.urlsafe_b64decode(encrypted_str.encode())
            plaintext = self.cipher.decrypt(encrypted)
            return plaintext.decode()
        except Exception as e:
            self.logger.error(f"Error decrypting string: {e}")
            return None

    def encrypt_credentials(self, credentials: Dict) -> str:
        """
        Encrypt credentials dictionary.

        Args:
            credentials: Dict of credentials

        Returns:
            Encrypted JSON string
        """
        try:
            json_str = json.dumps(credentials)
            return self.encrypt_string(json_str)
        except Exception as e:
            self.logger.error(f"Error encrypting credentials: {e}")
            return None

    def decrypt_credentials(self, encrypted_json: str) -> Dict:
        """
        Decrypt credentials dictionary.

        Args:
            encrypted_json: Encrypted JSON string

        Returns:
            Credentials dict
        """
        try:
            json_str = self.decrypt_string(encrypted_json)
            return json.loads(json_str)
        except Exception as e:
            self.logger.error(f"Error decrypting credentials: {e}")
            return None

    def rotate_key(self, new_password: str) -> bool:
        """
        Rotate encryption key.

        Args:
            new_password: New master password

        Returns:
            True if successful
        """
        try:
            # Decrypt with old key
            if self.encrypted_env.exists():
                with open(self.encrypted_env, 'rb') as f:
                    encrypted = f.read()
                plaintext = self.cipher.decrypt(encrypted)
            else:
                plaintext = None

            # Generate new key
            new_key, new_salt = self.generate_key(new_password)

            # Save new key
            with open(self.key_file, 'wb') as f:
                f.write(new_key)

            # Save new salt
            salt_file = self.security_dir / ".salt"
            with open(salt_file, 'wb') as f:
                f.write(new_salt)

            # Re-encrypt with new key
            self.cipher = Fernet(new_key)

            if plaintext:
                encrypted = self.cipher.encrypt(plaintext)
                with open(self.encrypted_env, 'wb') as f:
                    f.write(encrypted)

            self.logger.info("Key rotated successfully")
            self.audit_log_event("KEY_ROTATED", "Encryption key rotated")

            return True

        except Exception as e:
            self.logger.error(f"Error rotating key: {e}")
            return False

    def audit_log_event(self, event_type: str, description: str):
        """Log security event to audit log"""
        try:
            event = {
                'timestamp': datetime.now().isoformat(),
                'event_type': event_type,
                'description': description,
                'user': os.getenv('USER', 'unknown')
            }

            with open(self.audit_log, 'a') as f:
                f.write(json.dumps(event) + '\n')

        except Exception as e:
            self.logger.error(f"Error logging audit event: {e}")

    def get_audit_log(self, limit: int = 100) -> list:
        """
        Get recent audit log entries.

        Args:
            limit: Number of entries to return

        Returns:
            List of audit events
        """
        try:
            if not self.audit_log.exists():
                return []

            events = []
            with open(self.audit_log, 'r') as f:
                for line in f:
                    events.append(json.loads(line.strip()))

            return events[-limit:]

        except Exception as e:
            self.logger.error(f"Error reading audit log: {e}")
            return []

if __name__ == "__main__":
    # Test secrets manager
    manager = SecretsManager()

    # Encrypt test credentials
    creds = {
        'api_key': 'test_key_12345',
        'secret': 'super_secret_value'
    }

    encrypted = manager.encrypt_credentials(creds)
    print(f"Encrypted: {encrypted[:50]}...")

    decrypted = manager.decrypt_credentials(encrypted)
    print(f"Decrypted: {decrypted}")

    # Get audit log
    audit = manager.get_audit_log(limit=5)
    print(f"Audit log: {len(audit)} events")
