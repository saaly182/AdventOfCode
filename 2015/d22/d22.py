#!/usr/bin/python3 -u

import dataclasses

# global
mana_min = None


@dataclasses.dataclass
class Boss:
    hp: int
    damage: int


class Wizard:
    """
    * Magic Missile costs 53 mana. It instantly does 4 damage.
    * Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit
    points.
    * Shield costs 113 mana. It starts an effect that lasts for 6 turns.
    While it is active, your armor is increased by 7.
    * Poison costs 173 mana. It starts an effect that lasts for 6 turns. At
    the start of each turn while it is active, it deals the boss 3 damage.
    * Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At
    the start of each turn while it is active, it gives you 101 new mana.
    """
    # class vars
    spell_cost = {'missile': 53, 'drain': 73, 'shield': 113, 'poison': 173,
                  'recharge': 229}
    spells = tuple(spell_cost)
    min_spell_cost = min(spell_cost.values())

    def __init__(self, hp, mana, armor=0, effects_ttl=None, spent_mana=0):
        self.hp = hp
        self.mana = mana
        self.armor = armor
        if effects_ttl is None:
            self.effects_ttl = {spell: 0 for spell in Wizard.spell_cost}
        else:
            self.effects_ttl = effects_ttl.copy()
        self.spent_mana = spent_mana

    def clone(self):
        return Wizard(self.hp, self.mana, self.armor, self.effects_ttl,
                      self.spent_mana)

    def process_effects(self):
        """Process all the active effects and return opponent damage value."""
        damage = 0
        for spell, ttl in tuple(self.effects_ttl.items()):
            if ttl == 0:
                if spell == 'shield':
                    self.armor = 0
                continue
            match spell:
                case 'shield':
                    self.armor = 7
                case 'poison':
                    damage += 3
                case 'recharge':
                    self.mana += 101
            self.effects_ttl[spell] -= 1
        return damage

    def can_cast(self, spell):
        if self.mana < Wizard.spell_cost[spell]:
            return False
        if self.effects_ttl[spell] > 1:
            return False
        return True

    def cast(self, spell):
        """Cast the spell and return the opponent damage value."""
        cost = Wizard.spell_cost[spell]
        self.mana -= cost
        self.spent_mana += cost

        damage = 0
        match spell:
            case 'missile':
                damage += 4
            case 'drain':
                damage += 2
                self.hp += 2
            case 'shield':
                self.effects_ttl[spell] = 6
            case 'poison':
                self.effects_ttl[spell] = 6
            case 'recharge':
                self.effects_ttl[spell] = 5

        return damage

    def __str__(self):
        return (f'Wizard({self.hp=} {self.mana=} {self.spent_mana=} '
                f'{self.armor=} {self.effects_ttl=}')


def do_turns(boss, wizard, spell, hard_mode):
    boss_dead = False

    def update_boss(damage):
        global mana_min
        nonlocal boss_dead
        boss.hp -= damage
        if boss.hp <= 0:
            if wizard.spent_mana < mana_min:
                mana_min = wizard.spent_mana
            boss_dead = True

    # wizard's turn
    if hard_mode:
        wizard.hp -= 1
        if wizard.hp <= 0:
            return
    wdamage = wizard.process_effects()
    update_boss(wdamage)
    if boss_dead:
        return
    wdamage = wizard.cast(spell)
    update_boss(wdamage)
    if boss_dead:
        return

    # boss's turn
    wdamage = wizard.process_effects()
    update_boss(wdamage)
    if boss_dead:
        return
    bdamage = max(1, boss.damage - wizard.armor)
    wizard.hp -= bdamage


def dfs(boss, wizard, hard_mode=False):
    """
    Exhaustive DFS for the least amount of spent mana that defeats the boss.
    After running this function, mana_min will have the answer.
    """

    # If you cannot afford to cast any spell, you lose.
    if wizard.mana < Wizard.min_spell_cost:
        return

    # Prune if this is already at least the current min
    if wizard.spent_mana >= mana_min:
        return

    for spell in Wizard.spells:
        if wizard.can_cast(spell):
            w = wizard.clone()
            b = dataclasses.replace(boss)
            do_turns(b, w, spell, hard_mode)

            if w.hp > 0 and b.hp > 0:
                dfs(b, w, hard_mode)


def part1(boss, wizard):
    global mana_min
    mana_min = float('inf')
    dfs(boss, wizard)
    return mana_min


def part2(boss, wizard):
    global mana_min
    mana_min = float('inf')
    dfs(boss, wizard, hard_mode=True)
    return mana_min


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    boss = Boss(58, 9)
    wizard = Wizard(50, 500)
    print("Part 1 answer =", part1(boss, wizard))
    print("Part 2 answer =", part2(boss, wizard))
    print()


if __name__ == '__main__':
    main()
