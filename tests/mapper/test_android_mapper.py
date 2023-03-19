import pytest
from mapper import mapper, android_mapper


class TestAndroidMapper:
    def build_node_from_uids(self, uids):
        return [mapper.Node(uid) for uid in uids]

    @pytest.fixture
    def nodes(self):
        return [
            mapper.Node("1"),
            mapper.Node("2"),
            mapper.Node("3"),
            mapper.Node("4"),
            mapper.Node("5"),
            mapper.Node("6"),
            mapper.Node("7"),
            mapper.Node("8"),
            mapper.Node("9"),
        ]

    def test_unique_id(self):
        with pytest.raises(android_mapper.NonUniqueError):
            android_mapper.AndroidMapper(mapper.Node("123"), mapper.Node("123"))

    def test_node_length(self):
        with pytest.raises(ValueError):
            android_mapper.AndroidMapper(mapper.Node("123"))

    @pytest.mark.parametrize(
        "uid, visited, expected",
        [
            pytest.param(
                "1",
                None,
                ["2", "4", "5", "6", "8"],
                id="corner_case",
            ),
            pytest.param(
                "8",
                None,
                ["1", "3", "4", "5", "6", "7", "9"],
                id="edge_case",
            ),
            pytest.param(
                "5",
                None,
                ["1", "2", "3", "4", "6", "7", "8", "9"],
                id="middle_case",
            ),
            pytest.param(
                "1",
                ["5"],
                ["2", "4", "9", "6", "8"],
                id="visited_case",
            ),
        ],
    )
    def test_get_next_uids(self, uid, visited, expected, nodes):
        android_map = android_mapper.AndroidMapper(*nodes)
        observed = list(android_map.get_next_uids(uid, visited))
        assert len(expected) == len(observed) and all([x in expected for x in observed])
