from sc2.ids.ability_id import AbilityId
from sharpy.plans.acts import ActBase
from sharpy.knowledges import Knowledge
from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit


class ScanAhead(ActBase):

    def __init__(self, interval_seconds=60):
        super().__init__()
        self.interval_seconds = interval_seconds
        self.last_scan = 0

    async def start(self, knowledge: Knowledge):
        await super().start(knowledge)

    async def execute(self) -> bool:
        if self.ai.time < self.last_scan + self.interval_seconds:
            # Normal scan on timer
            return True  # No block

        enemies = self.ai.enemy_units(set([
            UnitTypeId.MARINE,
            UnitTypeId.MARAUDER,
            UnitTypeId.REAPER,
            UnitTypeId.HELLION,
            UnitTypeId.SIEGETANK,
            UnitTypeId.SIEGETANKSIEGED,
            UnitTypeId.MEDIVAC,
            UnitTypeId.VIKINGASSAULT,
            UnitTypeId.VIKINGFIGHTER,
        ]))

        if enemies.visible.exists and enemies.visible.amount > 1:        
            await self.scan_location(self.ai, enemies.center)

        return True  # No block

    async def scan_location(self, ai, scan_target):
        building: Unit
        buildings = ai.structures(UnitTypeId.ORBITALCOMMAND).ready
        for building in buildings:
            if building.energy > 50:
                if scan_target is not None:
                    building(AbilityId.SCANNERSWEEP_SCAN, scan_target)
                    self.last_scan = ai.time
                    return  # only one orbital should scan
