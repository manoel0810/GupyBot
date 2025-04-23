import json
import os
from typing import List, Dict, Any

class Group:
    def __init__(self, url: str, emails: List[str], groupId: int, engine: str, dataset: str):
        self.url = url
        self.emails = emails
        self.groupId = groupId
        self.engine = engine
        self.dataset = dataset

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "emails": self.emails,
            "groupId": self.groupId,
            "engine": self.engine,
            "dataset": self.dataset
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Group':
        return Group(
            url=data["url"],
            emails=data["emails"],
            groupId=data["groupId"],
            engine=data["engine"],
            dataset=data["dataset"]
        )


class JsonGroupManager:
    def __init__(self, filename: str = "groups.json"):
        self.filepath = os.path.join(os.getcwd(), filename)
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
