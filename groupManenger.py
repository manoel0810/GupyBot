# groupManenger.py
from typing import List, Dict, Any
from database import get_all_groups

class Group:
    def __init__(self, keys: List[str], emails: List[str], groupId: int, remoteOnly: bool, skip: bool):
        self.keys = keys
        self.emails = emails
        self.groupId = groupId
        self.remoteOnly = remoteOnly
        self.skip = skip

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Group':
        return Group(
            keys=data["keys"],
            emails=data["emails"],
            groupId=data["groupId"],
            remoteOnly=data["remoteOnly"],
            skip=data["skip"]
        )

class GroupManager:
    def get_all_groups(self) -> List[Group]:
        groups_data = get_all_groups()
        return [Group.from_dict(g) for g in groups_data]