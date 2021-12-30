from grblogtools.helpers import parse_block
from grblogtools.norel import NoRelParser

norel_section_test_data = """
Variable types: 19 continuous, 297 integer (297 binary)
Found heuristic solution: objective 3.133356e+09
Starting NoRel heuristic
Elapsed time for NoRel heuristic: 5s
Found heuristic solution: objective 3.033354e+09
Found heuristic solution: objective 1.450014e+09
Elapsed time for NoRel heuristic: 10s (best bound 8.00002e+08)
Found heuristic solution: objective 1.400013e+09
Elapsed time for NoRel heuristic: 16s (best bound 8.00002e+08)
Found heuristic solution: objective 1.200013e+09
Elapsed time for NoRel heuristic: 21s (best bound 8.00002e+08)
Elapsed time for NoRel heuristic: 27s (best bound 8.00002e+08)
Elapsed time for NoRel heuristic: 93s (best bound 8.00002e+08)

Root simplex log...
"""

norel_section_test_data_nobound = """
Starting NoRel heuristic
Elapsed time for NoRel heuristic: 5s
Found heuristic solution: objective 1.450014e+09
Elapsed time for NoRel heuristic: 10s
"""

norel_section_test_data_nosol = """
Starting NoRel heuristic
Elapsed time for NoRel heuristic: 5s
"""


def test_empty():
    """To check that timeline to summary conversion is sane."""
    parser = NoRelParser()
    assert parser.timeline == []
    assert parser.summary == {}


def test_norel_parser():
    """Pass all test lines in sequence and test summary/timeline."""
    parser = NoRelParser()
    parse_block(parser, norel_section_test_data)
    # only the 'Root simplex log...' line was passed but not parsed.
    assert parser.ignored_lines == 1
    assert parser.summary == {
        "NoRelBestSol": 1.200013e9,
        "NoRelTime": 93.0,
        "NoRelBestBd": 8.00002e8,
    }
    assert parser.timeline == [
        {"Time": 5.0},
        {"Time": 10.0, "BestBd": 8.00002e8, "Incumbent": 1.450014e9},
        {"Time": 16.0, "BestBd": 8.00002e8, "Incumbent": 1.400013e9},
        {"Time": 21.0, "BestBd": 8.00002e8, "Incumbent": 1.200013e9},
        {"Time": 27.0, "BestBd": 8.00002e8, "Incumbent": 1.200013e9},
        {"Time": 93.0, "BestBd": 8.00002e8, "Incumbent": 1.200013e9},
    ]


def test_nobound():
    parser = NoRelParser()
    parse_block(parser, norel_section_test_data_nobound)
    assert parser.summary == {"NoRelTime": 10.0, "NoRelBestSol": 1.450014e9}


def test_nosol():
    parser = NoRelParser()
    parse_block(parser, norel_section_test_data_nosol)
    assert parser.summary == {"NoRelTime": 5.0}
