import json

from blocksec.scanners.smart_contract.owasp_map import DETECTOR_TO_SWC, map_detector_to_owasp
from blocksec.scanners.smart_contract.slither_runner import parse_slither_output


def test_owasp_map_reentrancy():
    result = map_detector_to_owasp("reentrancy-eth")
    assert result["swc"] == "SWC-107"
    assert "Reentrancy" in result["title"]


def test_owasp_map_tx_origin():
    result = map_detector_to_owasp("tx-origin")
    assert result["swc"] == "SWC-115"


def test_owasp_map_unknown():
    result = map_detector_to_owasp("some-unknown-detector")
    assert result["swc"] == "N/A"
    assert result["title"] == "Other"


def test_owasp_map_coverage():
    for key in DETECTOR_TO_SWC:
        result = map_detector_to_owasp(key)
        assert result["swc"] != "N/A" or key == ""


def test_parse_empty_stdout():
    findings = parse_slither_output("", "/tmp")
    assert findings == []


def test_parse_invalid_json():
    findings = parse_slither_output("not json", "/tmp")
    assert findings == []


def test_parse_no_detectors():
    data = json.dumps({"results": {"detectors": []}})
    findings = parse_slither_output(data, "/tmp")
    assert findings == []


def test_parse_single_detector():
    slither_output = {
        "results": {
            "detectors": [
                {
                    "check": "reentrancy-eth",
                    "description": "Reentrancy vulnerability found",
                    "impact": "High",
                    "confidence": "High",
                    "recommendation": "Use ReentrancyGuard",
                    "elements": [
                        {
                            "source_mapping": {
                                "filename_relative": "contracts/Vuln.sol",
                                "lines": [42],
                            },
                            "additional_fields": {"signature": "withdraw(uint256)"},
                        }
                    ],
                }
            ]
        }
    }
    findings = parse_slither_output(json.dumps(slither_output), "/project")
    assert len(findings) == 1
    f = findings[0]
    assert f.severity.value == "HIGH"
    assert f.category.value == "CONTRACT"
    assert "SWC-107" in f.title
    assert f.line_start == 42
    assert "contracts/Vuln.sol" in f.file_path


def test_parse_multiple_elements():
    slither_output = {
        "results": {
            "detectors": [
                {
                    "check": "unprotected-upgrade",
                    "description": "Unprotected upgradeable",
                    "impact": "Medium",
                    "confidence": "High",
                    "elements": [
                        {"source_mapping": {"filename_relative": "a.sol", "lines": [10]}, "additional_fields": {}},
                        {"source_mapping": {"filename_relative": "b.sol", "lines": [20]}, "additional_fields": {}},
                    ],
                }
            ]
        }
    }
    findings = parse_slither_output(json.dumps(slither_output), "/project")
    assert len(findings) == 2
