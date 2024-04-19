from typing import List, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
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


class ThreeBaseMarineViking(SkeletonBot):
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

    def create_plan(self) -> ActBase:
        return BuildOrder(
            SpeedMining(),
            AutoDepot(),
            AutoWorker(66),
            MorphOrbitals(3),

            SequentialList(
                Expand(2, priority_base_index=1),
                GridBuilding(UnitTypeId.SUPPLYDEPOT, 1),
                GridBuilding(UnitTypeId.BARRACKS, 1),
                BuildGas(2),
                MorphOrbitals(1),
                BuildOrder(
                    Expand(3, priority_base_index=3, priority=True),
                    BuildAddon(UnitTypeId.STARPORTREACTOR, UnitTypeId.STARPORT, 5),
                    GridBuilding(UnitTypeId.STARPORT, 5),
                    GridBuilding(UnitTypeId.FACTORY, 1),
                ),
                BuildGas(6),
            ),

            Step(UnitReady(UnitTypeId.STARPORT), TerranUnit(UnitTypeId.VIKINGFIGHTER, priority=True)),
            Step(UnitReady(UnitTypeId.FACTORY), TerranUnit(UnitTypeId.HELLION)),
            Step(UnitReady(UnitTypeId.BARRACKS), TerranUnit(UnitTypeId.MARINE)),

            DistributeWorkers(),
            LowerDepots(),
            Repair(),

            PlanZoneGather(),
            PlanZoneDefense(),
            PlanWorkerOnlyDefense(),

            IfElse(
                Time(500),
                SequentialList(
                    ScanAhead(20),
                    PlanZoneAttackAllIn(),
                    PlanFinishEnemy(),
                ),
                CallMule(50),
            )
        )
