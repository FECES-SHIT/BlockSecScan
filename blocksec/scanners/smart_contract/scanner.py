from blocksec.models.finding import Finding
from blocksec.models.rule import Rule
from blocksec.models.scan import ScanTarget
from blocksec.scanners.base import BaseScanner
from blocksec.scanners.smart_contract.slither_runner import run_slither


class SmartContractScanner(BaseScanner):
    def can_handle(self, target: ScanTarget) -> bool:
        return target.target_type == "contract"

    def scan(self, target: ScanTarget, rules: list[Rule]) -> list[Finding]:
        return run_slither(target.path)
