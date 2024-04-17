from typing import List, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sharpy.combat.group_combat_manager import GroupCombatManager
from sharpy.knowledges import SkeletonBot
from sharpy.managers import ManagerBase
from sharpy.managers.core import *
from sharpy.managers.extensions import MemoryManager
from sharpy.plans.terran import *



class BottyMcBotFace(SkeletonBot):
    def __init__(self):
        super().__init__("Terran Template")

    def configure_managers(self) -> Optional[List[ManagerBase]]:
        return [
            MemoryManager(),
            PreviousUnitsManager(),
            LostUnitsManager(),
            EnemyUnitsManager(),
            UnitCacheManager(),
            UnitValue(),
            UnitRoleManager(),
            PathingManager(),
            ZoneManager(),
            BuildingSolver(),
            IncomeCalculator(),
            CooldownManager(),
            GroupCombatManager(),
            GatherPointSolver(),
            ActManager(self.create_plan()),
        ]

    def create_plan(self) -> ActBase:
        return BuildOrder(
            Expand(2),
            AutoWorker(),
            AutoDepot(),
            TerranUnit(UnitTypeId.SIEGETANK, priority=True),
            TerranUnit(UnitTypeId.MARINE, priority=True),
            TerranUnit(UnitTypeId.MEDIVAC, priority=True),
            SequentialList(
                GridBuilding(UnitTypeId.BARRACKS, 1),
                Gas(1),
                TerranUnit(UnitTypeId.REAPER, 1),
                Scout(UnitTypeId.REAPER),
                BuildAddon(UnitTypeId.BARRACKSTECHLAB, UnitTypeId.BARRACKS, 1),
                GridBuilding(UnitTypeId.FACTORY, 1),
                GridBuilding(UnitTypeId.STARPORT, 1),
                GridBuilding(UnitTypeId.ENGINEERINGBAY, 1),
                Tech(UpgradeId.STIMPACK, UnitTypeId.ENGINEERINGBAY),
                Gas(2),
                GridBuilding(UnitTypeId.BARRACKS, 3),
            ),
            DistributeWorkers(),
            LowerDepots(),
            # Have the combat units gather in one place
            PlanZoneGather(),
            # Defend
            PlanZoneDefense(),
            SequentialList(
                # Attack, these 2 should be last in a sequential list in this order
                PlanZoneAttack(50,),
                # Roam the map until last building is found.
                PlanFinishEnemy(),
            )
        )
