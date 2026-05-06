"""

"""

import math
from .game_constants import SkillType, SkillProficiencyType, AbilityType


class Ability:
    def __init__(self,
                 ability_type: AbilityType,
                 ability_score: int = None,
                 proficiency_bonus:int = None):
        """
        Abilities in D&D are the foundational scores that dictate nearly every aspect of play, they are numeric
        representations of physical and mental attributes. They are better described in the SRD in the resources
        directory.

        :param ability_type: AbilityType enum (str, dex, con, int, wis, cha)
        :param ability_score: int (optional) initial score to set ability to
        :param proficiency_bonus: proficiency bonus from character
        """

        self.type = ability_type
        self.name = self.type.label
        self.base_score = 10
        self.score_modifiers = []  # non-base score ability increases (equipment, conditions, etc.)
        self.total_score = 0
        self.modifier = 0
        self.proficiency_bonus = proficiency_bonus

        if ability_score:
            self.set_base_score(ability_score)

        self.calculate_modifier()

        self.associated_skills = [Skill(skill_type=associated_skill,
                                        ability_score_modifier=self.modifier,
                                        proficiency_bonus=self.proficiency_bonus)
                                  for associated_skill in self.type.associated_skills]

    def set_base_score(self, score:int):
        """
        sets the ability's base score
        """
        self.base_score = score
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

    def add_score_modifier(self, modifier:int):
        """
        adds a specific modifier to the ability's total score, and recalculates the ability modifier
        """
        self.score_modifiers.append(modifier)
        self.calculate_modifier()

    def remove_score_modifier(self, modifier:int):
        """
        removes a specific modifier to the ability's total score, and recalculates the ability modifier
        """
        self.score_modifiers.remove(modifier)
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

    def recalculate_associated_skill_scores(self, proficiency_bonus:int):
        """
        for each skill associated with an ability:
            > sets the skill's score (based on associated ability modifier), and,
            > calculates the total score of the skill (based on proficiency, and skill score modifiers)
        """
        for skill in self.associated_skills:
            skill.set_base_score(ability_score_modifier=self.modifier)
            skill.calculate_total_score()


class Skill:
    def __init__(self,
                 skill_type: SkillType,
                 ability_score_modifier: int = None,
                 proficiency_bonus: int = None):
        """
        Skills are specific skill-based actions that are tied to a parent Ability, a character can be either proficient,
        have expertise, or no skill at all in a given skill. If a character is skilled in a skill-- they will have an
        easier time succeeding at that particular skill-based action.

        :param skill_type: SkillType enum (too many to list)
        :param ability_score_modifier: the modifier tied to the parent Ability associated with the skill
        :param proficiency_bonus: depending on whether a character is proficient in a skill will dictate whether this bonus is applied or not
        """

        self.type = skill_type
        self.name = self.type.label
        self.base_score = 0
        self.score_modifiers = []  # non-ability-score modifiers
        self.total_score = 0  # final tally for score
        self.proficiency = SkillProficiencyType.normal  # whether the skill has proficiency
        self.proficiency_bonus = proficiency_bonus

        if ability_score_modifier:
            self.set_base_score(ability_score_modifier)

        self.calculate_total_score()

    def set_base_score(self, ability_score_modifier: int):
        """
        sets the base score of the skill to the provided ability score modifier
        """
        self.base_score = ability_score_modifier

    def set_proficiency(self, proficiency: SkillProficiencyType):
        """
        sets the proficiency in the skill to the provided proficiency type
        """
        self.proficiency = proficiency

    def increase_proficiency(self):
        """
        increases the proficiency in the skill by one ranking (maxing out at expert)
        """
        if self.proficiency != SkillProficiencyType.expert:  # if creature is already expert, do nothing
            self.proficiency = SkillProficiencyType.expert \
                if self.proficiency == SkillProficiencyType.proficient else SkillProficiencyType.proficient

    def decrease_proficiency(self):
        """
        decreases the proficiency in the skill by one ranking (bottoming out at normal)
        """
        if self.proficiency != SkillProficiencyType.normal:  # if creature has no proficiency, do nothing
            self.proficiency = SkillProficiencyType.normal \
                if self.proficiency == SkillProficiencyType.proficient else SkillProficiencyType.proficient

    def add_score_modifier(self, modifier: int):
        """
        adds a specific modifier to the skill's total score
        """
        self.score_modifiers.append(modifier)
        self.calculate_total_score()

    def remove_score_modifier(self, modifier: int):
        """
        removes a specific modifier to the skill's total score
        """
        self.score_modifiers.remove(modifier)
        self.calculate_total_score()

    def calculate_total_score(self):
        """
        calculates the total score of the skill (base + score modifiers)
        """
        self.total_score = self.base_score + sum(self.score_modifiers)

        if self.proficiency == SkillProficiencyType.proficient:
            self.total_score += self.proficiency_bonus
        elif self.proficiency == SkillProficiencyType.expert:
            self.total_score += (2 * self.proficiency_bonus)