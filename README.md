# Project Name: Mother Oerth
## Project Description:
This is an ongoing Dungeons and Dragons (D&D) project that is aiming to take the mechanical aspects of the tabletop game 
and put it to code, with later intentions to utilize a LLM to act as a DM that will work alongside this system. As this 
is based on the SRD 5e open-source material, this will not be a propriety project, and will likewise be kept open 
according to the Creative Commons license on the SRD, all rights and credits given to the source material owners. 

I do not own any of the SRD-related concepts/mechanics; ownership of new elements are maintained by the contributor who 
puts it forth.

Should be noted that this is very much a WIP and is still under heavy and active development.
Should also be noted that there will be certain elements of earlier versions of DND that I will be encorporating as I 
see fit (with reasonable cause!)

Finally, the endgoal of this project is to create an open-source platform which is freely available to enable people to 
play campaigns that are either prebuilt, or completely custom. 
The setting I'm planning to focus on (initially) is the Greyhawk DND setting, as it is storied and interesting!

## Current Work:
Currently working on converting the various TTRPG elements listed in the open-source SRD for 5th edition DND to 
formatted data structures that are robust enough for use in a flexible system.

## Future Work:
In addition to the aforementioned "pulling from earlier editions of dnd" I will also be making choice modifications to
aspects of the game (classes, items, mechanics, etc.) that are in line with making the game more fun, balanced, and 
enjoyable. If I make a change that is inspired by another source, I will cite it.

## Major Changes to Ruleset

### Alignment
Alignment is no longer a cosmic universal concept, but rather a faction-by-faction alignment/reputation system. This
does away with the 'moral absolutism' that has been inherent in the design of D&D (but mostly rectified in 5e by 
lessening its importance in the mechanics of play) since AD&D. The impact of this change will be significant to the flow
of your session, as the concept of a 'faction' will be much broader a concept, and will make being a part of a setting a
much more complex: " political intrigue/diplomacy" lovers rejoice!

Each faction will have a set of characteristics that is a subset of the closed set of all possible characteristics that 
a faction can engender; relationships between factions will fall somewhere on the scale of opposing, neutral, or 
supportive depending on how their characteristics and end-goals align. 

For instance, the Thieves Guild of a city will have the characteristics of ["stealth", "unlawful", "organized"], whereas 
the City Guard will have the characteristics of ["militaristic", "lawful", "organized"]. There are opposing characteristics
when considering their relationship (lawful, unlawful), shared characteristics (organized), and unrelated characteristics
between them (stealth, militaristic). When considering these characteristics it will dictate their resultant interactions.

Additionally, certain factions will have initial dispositions, and floors/ceilings to their disposition towards those 
that interact with them. e.g. a Beholder (being its own faction) in D&D 5e is described as 'aggressive', 'hateful', and 
'greedy', leading it to have an initial disposition of aggression and distrust. While a party if given the chance may 
succeed at parlaying with these aberrations, due to the inherent nature of the creature its disposition will never rise 
above indifference. 

Overall, this makes the process of faction selection/interaction more impactful to the flow of play e.g. Clerics who 
worship Lady Selûne will naturally be at odds with factions that align themselves with Lady Shar. Equally so: the 
openness by which you align/assist certain factions may percolate and impact future/current relationships with factions.
If you become known as a bounty-hunter that seeks and hunts down unlawful individuals, you may find your future 
interactions with city guards more palatable, but you may also find your interactions with unlawful factions less 
favorable. The spread of information will not be instantaneous, and players if they find themselves on the wrong side of
the law may find themselves traveling to outrun their errant and unlawful reputation (Reputation-spread rules to come).

Reputation with factions will also be a currency that players may find useful, say you have a close-knit relationship
with a mercantile faction like the Zhentarim... you may find that merchants from this faction recognize you on sight and
have more powerful offerings than to an outsider to the family. Alternatively, say you become close to a member of royalty
you may find yourself able to request a detachment of soldiers to assist you in a quest. This additionally makes 
alignment ***valuable*** to players, and not just a marker of where ones moral compass lies.

## Major Features of Project

### Reduction of Metagaming
TTRPGs typically have a metagaming problem when played at a table. A DM that reveals skill-obtained information verbally 
to one player must contend with the fact that all other players at the table now have the exact same information for 
free without the required skill-check; there is also the possibility that a player may want to keep certain information 
gained in this way to themselves for one reason or another. Additionally, in the case that all players **failed** a 
particular skill check (say a 'perception' check) this in some ways also reveals something to players on the meta-level
of play ("Oh, there was *something* to perceive here?", etc.) A good example of these 'failed' skill-checks leading to a
breaking of immersion would be in the game Baldur's Gate 3, where buried chests are scattered across the map and require
either a nature/perception check, and when failed: this failure is not silent, leading to players pulling characters to
and from their camp to succeed at the check.

This project deals with these two metagaming issues in the following ways:
- Player-specific Information: the architecture of this project is a server-client structure, this enables client-specific
messages to be transmitted, meaning that **only** the player that passes a particular check will be made aware of the 
information gained from it. This adds an extra layer of interest to play, as players may choose to not reveal information
to their party for their character's benefit. This enables some interesting roleplay aspects that players may quite enjoy.
- Silent Skill Checks: skill checks that are passive (read: 'passive perception') will be done automatically without 
prompts from players, failures will not be broadcast to the party, only successes will be given to specific players. 
Additionally, skills that a player is proficient/an-expert in will likewise be done automatically (e.g. a cleric who is 
proficient in religion-checks, etc.), failures at these automatic checks will not lock a player out of prompting for a 
particular skill check should it occur to them: this may make up for any grievances regarding the 'silent' nature of 
failures, as it in essence allows a player to roll twice (once automatically, once manually) for the same check.

These two changes not only create more player agency during play regarding the control of information they've gained, 
but also creates unique roleplaying situations e.g. rogue detects a trap, but chooses not to disclose that to their 
party.

### More Roleplay, Less Mechanics
Dice-rolling, math, and understanding mechanics is something that comes with the territory of D&D. This (sometimes) gets
in the way of roleplaying and breaks the flow of play. Baldur's Gate 3 did away with some of these issues by having 
equipment, ability-scores, skill bonuses/proficiencies baked into how the game functioned and was for the most part 
automatic. This project does something nearly identical by having most of the mechanics automated, with choice mechanics 
still left in the hands of the player.

This will be put into more detail as the project progresses, but the underlying design principle is that if a mechanic 
or process is superfluous and detracts from the roleplaying experience, then it will be automated in some way. This will
be a hard balance to strike and will be iterated upon over the course of the project's development.