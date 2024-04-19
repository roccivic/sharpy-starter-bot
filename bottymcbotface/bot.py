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
from bottymcbotface.scan_ahead import ScanAhead


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
            GameAnalyzer(),

        ]

    def create_plan(self) -> ActBase:
        return BuildOrder(
            GridBuilding(UnitTypeId.SUPPLYDEPOT, 1),
            Step(UnitReady(UnitTypeId.SUPPLYDEPOT), GridBuilding(UnitTypeId.BARRACKS, 1)),
            Step(UnitExists(UnitTypeId.BARRACKS), BuildGas(1)),
            Step(UnitReady(UnitTypeId.BARRACKS), MorphOrbitals(2)),
            Step(UnitExists(UnitTypeId.BARRACKS), TerranUnit(UnitTypeId.REAPER, 1, True, True)),

            Expand(2),

            Step(UnitReady(UnitTypeId.BARRACKS), GridBuilding(UnitTypeId.FACTORY, 1)),
            Step(UnitReady(UnitTypeId.FACTORY), GridBuilding(UnitTypeId.STARPORT, 1)),
            Step(UnitExists(UnitTypeId.FACTORY), BuildGas(2)),
            Step(UnitReady(UnitTypeId.FACTORY), BuildAddon(UnitTypeId.FACTORYTECHLAB, UnitTypeId.FACTORY, 1)),
            Step(UnitReady(UnitTypeId.BARRACKS), BuildAddon(UnitTypeId.BARRACKSTECHLAB, UnitTypeId.BARRACKS, 1)),
            Step(UnitReady(UnitTypeId.BARRACKS), BuildAddon(UnitTypeId.BARRACKSREACTOR, UnitTypeId.BARRACKS, 1)),
            Step(UnitReady(UnitTypeId.BARRACKSTECHLAB), Tech(UpgradeId.STIMPACK, UnitTypeId.BARRACKSTECHLAB)),
            Step(UnitReady(UnitTypeId.BARRACKSTECHLAB), Tech(UpgradeId.SHIELDWALL, UnitTypeId.BARRACKSTECHLAB)),
            Step(UnitReady(UnitTypeId.BARRACKSTECHLAB), Tech(UpgradeId.PUNISHERGRENADES, UnitTypeId.BARRACKSTECHLAB)),

            Step(UnitReady(UnitTypeId.STARPORT), TerranUnit(UnitTypeId.MEDIVAC, 1, priority=True)),
            Step(UnitReady(UnitTypeId.FACTORYTECHLAB), TerranUnit(UnitTypeId.SIEGETANK, 1, priority=True)),
            Step(UnitReady(UnitTypeId.STARPORT), TerranUnit(UnitTypeId.MEDIVAC, 2)),
            Step(UnitReady(UnitTypeId.STARPORT), TerranUnit(UnitTypeId.VIKINGFIGHTER, 2)),
            Step(UnitReady(UnitTypeId.FACTORYTECHLAB), TerranUnit(UnitTypeId.SIEGETANK)),
            Step(UnitReady(UnitTypeId.BARRACKS), TerranUnit(UnitTypeId.MARAUDER)),
            Step(UnitReady(UnitTypeId.BARRACKS), TerranUnit(UnitTypeId.MARINE)),

            Step(UnitExists(UnitTypeId.STARPORT), GridBuilding(UnitTypeId.BARRACKS, 6)),
            Step(UnitExists(UnitTypeId.STARPORT), GridBuilding(UnitTypeId.ENGINEERINGBAY)),
            Step(UnitReady(UnitTypeId.ENGINEERINGBAY), Tech(UpgradeId.TERRANINFANTRYWEAPONSLEVEL1)),
            Step(TechReady(UpgradeId.TERRANINFANTRYWEAPONSLEVEL1), Tech(UpgradeId.TERRANINFANTRYARMORSLEVEL1)),

            AutoDepot(),
            AutoWorker(36),
            DistributeWorkers(aggressive_gas_fill=True),
            LowerDepots(),
            Repair(),

            PlanZoneGather(),
            PlanZoneDefense(),
            PlanWorkerOnlyDefense(),

            IfElse(
                TechReady(UpgradeId.TERRANINFANTRYARMORSLEVEL1),
                SequentialList(
                    ScanAhead(20),
                    PlanZoneAttack(),
                    PlanFinishEnemy(),
                ),
                CallMule(50),
            )
        )
