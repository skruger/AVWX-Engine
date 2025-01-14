"""
Creates files for end-to-end tests

python util/build_tests.py
"""

# stdlib
import json
from dataclasses import asdict

# module
import avwx


def make_metar_test(station: str) -> dict:
    """
    Builds METAR test file for station
    """
    m = avwx.Metar(station)
    m.update()
    # Clear timestamp due to parse_date limitations
    m.data.time = None
    return {
        "data": asdict(m.data),
        "translations": asdict(m.translations),
        "summary": m.summary,
        "speech": m.speech,
        "station_info": asdict(m.station_info),
    }


def make_taf_test(station: str, report: str = None) -> dict:
    """
    Builds TAF test file for station
    """
    t = avwx.Taf(station)
    t.update(report)
    data = asdict(t.data)
    # Clear timestamp due to parse_date limitations
    for key in ("time", "start_time", "end_time"):
        data[key] = None
    for i in range(len(data["forecast"])):
        for key in ("start_time", "end_time"):
            data["forecast"][i][key] = None
    return {
        "data": data,
        "translations": asdict(t.translations),
        "summary": t.summary,
        "speech": t.speech,
        "station_info": asdict(t.station_info),
    }


def make_pirep_test(station: str) -> [dict]:
    """
    Builds PIREP test file for station
    """
    p = avwx.Pireps(station)
    p.update()
    ret = []
    if not p.data:
        return
    for report in p.data:
        # Clear timestamp due to parse_date limitations
        report.time = None
        ret.append({"data": asdict(report)})
    return {"reports": ret, "station_info": asdict(p.station_info)}


if __name__ == "__main__":
    from pathlib import Path

    for target in ("metar", "taf", "pirep"):
        for station in ("KJFK", "KMCO", "PHNL", "EGLL"):
            data = locals()[f"make_{target}_test"](station)
            if data:
                path = Path("tests", target, station + ".json")
                json.dump(data, path.open("w"), indent=4, sort_keys=True)
