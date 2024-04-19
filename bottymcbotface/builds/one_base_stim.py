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



class OneBaseStim(SkeletonBot):
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
            Expand(1, True),
            GridBuilding(UnitTypeId.SUPPLYDEPOT, 1),
            Step(UnitReady(UnitTypeId.BARRACKS), MorphOrbitals(1)),
            Step(UnitReady(UnitTypeId.BARRACKS), BuildAddon(UnitTypeId.BARRACKSTECHLAB, UnitTypeId.BARRACKS, 2)),
            Step(UnitReady(UnitTypeId.BARRACKSTECHLAB), Tech(UpgradeId.STIMPACK, UnitTypeId.BARRACKSTECHLAB)),
            Step(UnitReady(UnitTypeId.BARRACKSTECHLAB), Tech(UpgradeId.SHIELDWALL, UnitTypeId.BARRACKSTECHLAB)),
            Step(UnitReady(UnitTypeId.BARRACKS), TerranUnit(UnitTypeId.MARINE)),
            Step(UnitReady(UnitTypeId.BARRACKS), BuildGas(1)),
            Step(UnitReady(UnitTypeId.SUPPLYDEPOT), GridBuilding(UnitTypeId.BARRACKS, 5)),
            IfElse(
                All([
                    TechReady(UpgradeId.STIMPACK, percentage=0.01),
                    TechReady(UpgradeId.SHIELDWALL, percentage=0.01),
                ]),
                DistributeWorkers(0, 0, False),
                DistributeWorkers(3, 3, True),
            ),
            LowerDepots(),
            Repair(),
            IfElse(
                All(TechReady(UpgradeId.STIMPACK, 0.1), TechReady(UpgradeId.SHIELDWALL, 0.1)),
                Step(
                    All(TechReady(UpgradeId.STIMPACK), TechReady(UpgradeId.SHIELDWALL)),
                    ScanAhead(20),
                ),
                CallMule(50),
            ),
            AutoDepot(),
            AutoWorker(16),

            PlanWorkerOnlyDefense(),
            PlanZoneGather(),
            PlanZoneDefense(),

            Step(
                All(TechReady(UpgradeId.STIMPACK), TechReady(UpgradeId.SHIELDWALL)),
                SequentialList(PlanZoneAttackAllIn(), PlanFinishEnemy())
            )
        )
