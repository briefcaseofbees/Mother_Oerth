"""

"""

import math
from .game_constants import SkillType, SkillProficiencyType, AbilityType


class Skill:
    def __init__(self,
                 skill_type: SkillType,
                 ability_score_modifier: int = None,
                 proficiency_bonus: int = None):

        self.type = skill_type
        self.name = self.type.label
        self.score = 0
        self.score_modifiers = []                           # non-ability-score modifiers
        self.total_score = 0                                # final tally for score
        self.proficiency = SkillProficiencyType.normal      # whether the skill has proficiency

        if ability_score_modifier:
            self.set_score(ability_score_modifier)

        self.calculate_total_score(proficiency_bonus)

    def set_score(self, ability_score_modifier:int):
        self.score = ability_score_modifier

    def add_score_modifier(self, modifier:int):
        self.score_modifiers.append(modifier)

    def remove_score_modifier(self, modifier:int):
        self.score_modifiers.remove(modifier)

    def calculate_total_score(self, prof_bonus:int):
        self.total_score = self.score + sum(self.score_modifiers)

        if self.proficiency == SkillProficiencyType.proficient:
            self.total_score += prof_bonus
        elif self.proficiency == SkillProficiencyType.expert:
            self.total_score += (2 * prof_bonus)

    def set_proficiency(self, proficiency:SkillProficiencyType):
        self.proficiency = proficiency

    def increase_proficiency(self):
        if self.proficiency != SkillProficiencyType.expert:  # if creature is already expert, do nothing
            self.proficiency = SkillProficiencyType.expert \
                if self.proficiency == SkillProficiencyType.proficient else SkillProficiencyType.proficient

    def decrease_proficiency(self):
        if self.proficiency != SkillProficiencyType.normal:  # if creature has no proficiency, do nothing
            self.proficiency = SkillProficiencyType.normal \
                if self.proficiency == SkillProficiencyType.proficient else SkillProficiencyType.proficient


class Ability:
    def __init__(self,
                 ability_type: AbilityType,
                 ability_score: int = None):

        self.type = ability_type
        self.name = self.type.label
        self.base_score = 10
        self.score_modifiers = []  # non-base score ability increases (equipment, conditions, etc.)
        self.total_score = 0
        self.modifier = 0

        if ability_score:
            self.set_base_score(ability_score)

        self.calculate_modifier()

        self.associated_skills = [Skill(skill_type=associated_skill,
                                        ability_score_modifier=self.modifier)
                                  for associated_skill in self.type.associated_skills]

    def set_base_score(self, score:int):
        """
        sets the ability's base score
        """
        self.base_score = score
        self.calculate_modifier()

    def calculate_total_score(self):
        """
        calculates the total score of the ability (base + score increases)
        """
        self.total_score = self.base_score + sum(self.score_modifiers)

    def calculate_modifier(self):
        """
        recalculates the ability's total score, then recalculates the ability modifier, then recalculates the skill
        scores associated with the ability
        """
        self.calculate_total_score()
        self.modifier = math.floor(float(self.total_score) - 10 / 2)
        self.recalculate_associated_skill_scores(self.modifier)

    def add_score_modifier(self, modifier:int):
        """
        adds a specific bonus to the ability's total score, and recalculates the ability modifier
        """
        self.score_modifiers.append(modifier)
        self.calculate_modifier()

    def remove_score_modifier(self, modifier:int):
        """
        removes a specific bonus to the ability's total score, and recalculates the ability modifier
        """
        self.score_modifiers.remove(modifier)
        self.calculate_modifier()

    def increase_score(self):
        """
        increases the ability's base score by 1 (provided it's not currently greater than 20), and then recalculates the
        ability modifier
        """
        if self.base_score < 20:  # stats cannot be increased by ability score increases beyond 20
            self.base_score += 1

        self.calculate_modifier()

    def decrease_score(self):
        """
        decreases the ability's base score by 1 (provided it's not currently less than 4), and then recalculates the
        ability modifier
        """
        if self.base_score > 3:
            self.base_score -= 1

        self.calculate_modifier()

    def recalculate_associated_skill_scores(self, proficiency_bonus:int):
        """
        for each skill associated with an ability:
            > sets the skill's score (based on associated ability modifier), and,
            > calculates the total score of the skill (based on proficiency, and skill score modifiers)
        """
        for skill in self.associated_skills:
            skill.set_score(ability_score_modifier=self.modifier)
            skill.calculate_total_score(proficiency_bonus)
