import json
import os
from typing import List, Dict, Any

# Diretório onde este script está localizado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Group:
    # ATUALIZADO: 'key: str' foi alterado para 'keys: List[str]'
    def __init__(self, keys: List[str], emails: List[str], groupId: int, remoteOnly: bool, skip: bool):
        self.keys = keys
        self.emails = emails
        self.groupId = groupId
        self.remoteOnly = remoteOnly
        self.skip = skip

    def to_dict(self) -> Dict[str, Any]:
        # ATUALIZADO: 'key' agora é 'keys'
        return {
            "keys": self.keys,
            "emails": self.emails,
            "groupId": self.groupId,
            "remoteOnly": self.remoteOnly,
            "skip": self.skip
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Group':
        # ATUALIZADO: 'key' agora é 'keys'
        return Group(
            keys=data["keys"],
            emails=data["emails"],
            groupId=data["groupId"],
            remoteOnly=data["remoteOnly"],
            skip=data["skip"]
        )


class JsonGroupManager:
    def __init__(self, filename: str = "groups.json"):
        self.filepath = os.path.join(BASE_DIR, filename)
        self.groups: List[Group] = []
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.groups = [Group.from_dict(g) for g in data.get("groups", [])]

    def save(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump({"groups": [g.to_dict() for g in self.groups]}, f, indent=4, ensure_ascii=False)

    def add_group(self, group: Group):
        self.groups.append(group)
        self.save()

    def remove_group_by_id(self, group_id: int):
        self.groups = [g for g in self.groups if g.groupId != group_id]
        self.save()

    def update_group(self, group_id: int, updated_data: Dict[str, Any]):
        for g in self.groups:
            if g.groupId == group_id:
                for key, value in updated_data.items():
                    if hasattr(g, key):
                        setattr(g, key, value)
                break
        self.save()

    def get_all_groups(self) -> List[Group]:
        return self.groups

    def get_group_by_id(self, group_id: int) -> Group | None:
        for g in self.groups:
            if g.groupId == group_id:
                return g
        return None