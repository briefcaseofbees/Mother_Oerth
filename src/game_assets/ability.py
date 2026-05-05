"""

"""

from .game_constants import SkillType, SkillProficiencyType


class CreatureSkill:
    def __init__(self, skill_type: SkillType):
        self.name = skill_type.label
        self.type = skill_type
        self.proficiency = SkillProficiencyType.normal

    def increase_proficiency(self):
        if self.proficiency != SkillProficiencyType.expert:  # if creature is already expert, do nothing
            self.proficiency = SkillProficiencyType.expert \
                if self.proficiency == SkillProficiencyType.proficient else SkillProficiencyType.proficient

    def decrease_proficiency(self):
        if self.proficiency != SkillProficiencyType.normal:  # if creature has no proficiency, do nothing
            self.proficiency = SkillProficiencyType.normal \
                if self.proficiency == SkillProficiencyType.proficient else SkillProficiencyType.proficient