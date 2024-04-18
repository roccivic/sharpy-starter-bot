from typing import List, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sharpy.combat.group_combat_manager import GroupCombatManager
from sharpy.knowledges import SkeletonBot
from sharpy.managers import ManagerBase
from sharpy.managers.core import *
from sharpy.managers.extensions import MemoryManager, HeatMapManager
from sharpy.plans.terran import *
from sharpy.plans.tactics.scouting import *
from sharpy.knowledges.knowledge_bot import GameAnalyzer



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
            HeatMapManager(),
            GameAnalyzer(),
        ]

    def create_plan(self) -> ActBase:
        return BuildOrder(
            GridBuilding(UnitTypeId.SUPPLYDEPOT, 1),
            Step(UnitReady(UnitTypeId.BARRACKS), MorphOrbitals(1)),
            Step(UnitReady(UnitTypeId.BARRACKS), BuildAddon(UnitTypeId.BARRACKSTECHLAB, UnitTypeId.BARRACKS, 1)),
            Step(UnitReady(UnitTypeId.BARRACKSTECHLAB), Tech(UpgradeId.STIMPACK, UnitTypeId.BARRACKSTECHLAB)),
            Step(UnitReady(UnitTypeId.BARRACKS), TerranUnit(UnitTypeId.MARINE)),
            Step(UnitReady(UnitTypeId.BARRACKS), BuildGas(1)),
            Step(UnitReady(UnitTypeId.SUPPLYDEPOT), GridBuilding(UnitTypeId.BARRACKS, 5)),
            IfElse(
                TechReady(UpgradeId.STIMPACK, percentage=0.01),
                DistributeWorkers(0, 0, False),
                DistributeWorkers(3, 3, True),
            ),
            LowerDepots(),
            Repair(),
            IfElse(
                TechReady(UpgradeId.STIMPACK, 0.5),
                CallMule(100),
                CallMule(50),
            ),
            AutoDepot(),
            AutoWorker(16),

            PlanWorkerOnlyDefense(),
            PlanZoneGather(),
            PlanZoneDefense(),

            Step(
                TechReady(UpgradeId.STIMPACK), SequentialList(
                    ScanEnemy(20),
                    PlanZoneAttack(),
                    PlanFinishEnemy(),
                )
            )
        )
