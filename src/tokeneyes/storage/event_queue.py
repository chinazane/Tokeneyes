"""
Event queue for storing token events locally before sync
"""

from pathlib import Path
from datetime import datetime
from typing import List
import json
import uuid


class EventQueue:
    """
    Local queue for token events before upload to server
    Provides durability and retry capability
    """

    def __init__(self, state_dir: Path):
        """
        Initialize event queue

        Args:
            state_dir: Directory to store queue file
        """
        self.queue_file = state_dir / 'event_queue.jsonl'
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)

    def add(self, event) -> str:
        """
        Add an event to the queue

        Args:
            event: TokenEvent object

        Returns:
            Event ID
        """
        event_id = str(uuid.uuid4())

        queue_entry = {
            'id': event_id,
            'event': event.to_dict() if hasattr(event, 'to_dict') else event,
            'queued_at': datetime.utcnow().isoformat(),
            'synced': False
        }

        # Append to queue file (JSONL format)
        try:
            with open(self.queue_file, 'a') as f:
                f.write(json.dumps(queue_entry) + '\n')
        except Exception as e:
            print(f"Error adding event to queue: {e}")

        return event_id

    def add_all(self, events: List) -> List[str]:
        """
        Add multiple events to queue

        Args:
            events: List of TokenEvent objects

        Returns:
            List of event IDs
        """
        event_ids = []

        for event in events:
            event_id = self.add(event)
            event_ids.append(event_id)

        return event_ids

    def get_unsynced(self, limit: int = 100) -> List:
        """
        Get unsynced events from queue

        Args:
            limit: Maximum number of events to return

        Returns:
            List of event dictionaries with id and event data
        """
        unsynced = []

        if not self.queue_file.exists():
            return unsynced

        try:
            with open(self.queue_file, 'r') as f:
                for line in f:
                    if len(unsynced) >= limit:
                        break

                    try:
                        entry = json.loads(line.strip())

                        if not entry.get('synced', False):
                            unsynced.append(entry)

                    except json.JSONDecodeError:
                        continue

        except Exception as e:
            print(f"Error reading queue: {e}")

        return unsynced

    def mark_synced(self, event_ids: List[str]):
        """
        Mark events as synced

        Args:
            event_ids: List of event IDs to mark as synced
        """
        if not self.queue_file.exists():
            return

        # Read all entries
        entries = []

        try:
            with open(self.queue_file, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        entries.append(entry)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"Error reading queue: {e}")
            return

        # Update synced status
        event_ids_set = set(event_ids)

        for entry in entries:
            if entry['id'] in event_ids_set:
                entry['synced'] = True
                entry['synced_at'] = datetime.utcnow().isoformat()

        # Write back
        try:
            with open(self.queue_file, 'w') as f:
                for entry in entries:
                    f.write(json.dumps(entry) + '\n')
        except Exception as e:
            print(f"Error updating queue: {e}")

    def cleanup_synced(self, older_than_days: int = 7):
        """
        Remove synced events older than specified days

        Args:
            older_than_days: Remove synced events older than this many days
        """
        if not self.queue_file.exists():
            return

        cutoff = datetime.utcnow().timestamp() - (older_than_days * 86400)
        kept_entries = []

        try:
            with open(self.queue_file, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())

                        # Keep if not synced
                        if not entry.get('synced', False):
                            kept_entries.append(entry)
                            continue

                        # Keep if synced recently
                        synced_at = entry.get('synced_at')
                        if synced_at:
                            synced_timestamp = datetime.fromisoformat(synced_at).timestamp()
                            if synced_timestamp > cutoff:
                                kept_entries.append(entry)

                    except (json.JSONDecodeError, ValueError):
                        continue

            # Write back kept entries
            with open(self.queue_file, 'w') as f:
                for entry in kept_entries:
                    f.write(json.dumps(entry) + '\n')

        except Exception as e:
            print(f"Error cleaning up queue: {e}")

    def count(self) -> dict:
        """
        Count events in queue

        Returns:
            Dictionary with total, synced, unsynced counts
        """
        total = 0
        synced = 0
        unsynced = 0

        if not self.queue_file.exists():
            return {'total': 0, 'synced': 0, 'unsynced': 0}

        try:
            with open(self.queue_file, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        total += 1

                        if entry.get('synced', False):
                            synced += 1
                        else:
                            unsynced += 1

                    except json.JSONDecodeError:
                        continue

        except Exception as e:
            print(f"Error counting queue: {e}")

        return {
            'total': total,
            'synced': synced,
            'unsynced': unsynced
        }
