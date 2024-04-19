from typing import List, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.unit import Unit
from sharpy.combat.group_combat_manager import GroupCombatManager
from sharpy.knowledges import SkeletonBot
from sharpy.managers import ManagerBase
from sharpy.managers.core import *
from sharpy.managers.extensions import MemoryManager
from sharpy.plans.terran import *
from sharpy.plans.tactics.scouting import *
from sharpy.knowledges.knowledge_bot import GameAnalyzer
from sharpy.plans.tactics.speed_mining import SpeedMining
from bottymcbotface.scan_ahead import ScanAhead



class OneBaseReaper(SkeletonBot):
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
            GameAnalyzer(),
        ]
    
    async def on_building_construction_complete(self, unit: Unit):
        await super().on_building_construction_complete(unit)
        unit(AbilityId.RALLY_BUILDING, self.game_info.map_center)


    def create_plan(self) -> ActBase:
        return BuildOrder(
            SpeedMining(),
            AutoDepot(),
            AutoWorker(19),

            Expand(1, True),
            GridBuilding(UnitTypeId.SUPPLYDEPOT, 1),
            Step(UnitReady(UnitTypeId.BARRACKS), MorphOrbitals()),
            Step(UnitReady(UnitTypeId.BARRACKS), TerranUnit(UnitTypeId.REAPER)),
            Step(UnitExists(UnitTypeId.BARRACKS), BuildGas(2)),
            Step(UnitReady(UnitTypeId.SUPPLYDEPOT), GridBuilding(UnitTypeId.BARRACKS, 4)),
            
            DistributeWorkers(6, 6, True),
            LowerDepots(),
            Repair(),
            IfElse(
                UnitReady(UnitTypeId.REAPER),
                ScanAhead(20),
                CallMule(50),
            ),

            PlanWorkerOnlyDefense(),
            PlanZoneDefense(),
            PlanZoneAttackAllIn(2),
            PlanFinishEnemy(),
        )
