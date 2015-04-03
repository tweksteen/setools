"""Type enforcement rule query unit tests."""
# Copyright 2014, Tresys Technology, LLC
#
# This file is part of SETools.
#
# SETools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# SETools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SETools.  If not, see <http://www.gnu.org/licenses/>.
#
# pylint: disable=invalid-name,too-many-public-methods
import unittest

from setools import SELinuxPolicy
from setools.terulequery import TERuleQuery

from . import mixins


class TERuleQueryTest(mixins.ValidateRule, unittest.TestCase):

    """Type enforcement rule query unit tests."""

    @classmethod
    def setUpClass(cls):
        cls.p = SELinuxPolicy("tests/terulequery.conf")

    def test_000_unset(self):
        """TE rule query with no criteria."""
        # query with no parameters gets all TE rules.
        rules = sorted(self.p.terules())

        q = TERuleQuery(self.p)
        q_rules = sorted(q.results())

        self.assertListEqual(rules, q_rules)

    def test_001_source_direct(self):
        """TE rule query with exact, direct, source match."""
        q = TERuleQuery(
            self.p, source="test1a", source_indirect=False, source_regex=False)

        r = sorted(q.results())
        self.assertEqual(len(r), 1)
        self.validate_rule(r[0], "allow", "test1a", "test1t", "infoflow", set(["hi_w"]))

    def test_002_source_indirect(self):
        """TE rule query with exact, indirect, source match."""
        q = TERuleQuery(
            self.p, source="test2s", source_indirect=True, source_regex=False)

        r = sorted(q.results())
        self.assertEqual(len(r), 1)
        self.validate_rule(r[0], "allow", "test2a", "test2t", "infoflow", set(["hi_w"]))

    def test_003_source_direct_regex(self):
        """TE rule query with regex, direct, source match."""
        q = TERuleQuery(
            self.p, source="test3a.*", source_indirect=False, source_regex=True)

        r = sorted(q.results())
        self.assertEqual(len(r), 1)
        self.validate_rule(r[0], "allow", "test3aS", "test3t", "infoflow", set(["low_r"]))

    def test_004_source_indirect_regex(self):
        """TE rule query with regex, indirect, source match."""
        q = TERuleQuery(
            self.p, source="test4(s|t)", source_indirect=True, source_regex=True)

        r = sorted(q.results())
        self.assertEqual(len(r), 2)
        self.validate_rule(r[0], "allow", "test4a1", "test4a1", "infoflow", set(["hi_w"]))
        self.validate_rule(r[1], "allow", "test4a2", "test4a2", "infoflow", set(["low_r"]))

    def test_005_target_direct(self):
        """TE rule query with exact, direct, target match."""
        q = TERuleQuery(
            self.p, target="test5a", target_indirect=False, target_regex=False)

        r = sorted(q.results())
        self.assertEqual(len(r), 1)
        self.validate_rule(r[0], "allow", "test5s", "test5a", "infoflow", set(["hi_w"]))

    def test_006_target_indirect(self):
        """TE rule query with exact, indirect, target match."""
        q = TERuleQuery(
            self.p, target="test6t", target_indirect=True, target_regex=False)

        r = sorted(q.results())
        self.assertEqual(len(r), 2)
        self.validate_rule(r[0], "allow", "test6s", "test6a", "infoflow", set(["hi_w"]))
        self.validate_rule(r[1], "allow", "test6s", "test6t", "infoflow", set(["low_r"]))

    def test_007_target_direct_regex(self):
        """TE rule query with regex, direct, target match."""
        q = TERuleQuery(
            self.p, target="test7a.*", target_indirect=False, target_regex=True)

        r = sorted(q.results())
        self.assertEqual(len(r), 1)
        self.validate_rule(r[0], "allow", "test7s", "test7aPASS", "infoflow", set(["low_r"]))

    def test_008_target_indirect_regex(self):
        """TE rule query with regex, indirect, target match."""
        q = TERuleQuery(
            self.p, target="test8(s|t)", target_indirect=True, target_regex=True)

        r = sorted(q.results())
        self.assertEqual(len(r), 2)
        self.validate_rule(r[0], "allow", "test8a1", "test8a1", "infoflow", set(["hi_w"]))
        self.validate_rule(r[1], "allow", "test8a2", "test8a2", "infoflow", set(["low_r"]))

    def test_009_class(self):
        """TE rule query with exact object class match."""
        q = TERuleQuery(self.p, tclass="infoflow2", tclass_regex=False)

        r = sorted(q.results())
        self.assertEqual(len(r), 1)
        self.validate_rule(r[0], "allow", "test9", "test9", "infoflow2", set(["super_w"]))

    def test_010_class_list(self):
        """TE rule query with object class list match."""
        q = TERuleQuery(
            self.p, tclass=["infoflow3", "infoflow4"], tclass_regex=False)

        r = sorted(q.results())
        self.assertEqual(len(r), 2)
        self.validate_rule(r[0], "allow", "test10", "test10", "infoflow3", set(["null"]))
        self.validate_rule(r[1], "allow", "test10", "test10", "infoflow4", set(["hi_w"]))

    def test_011_class_regex(self):
        """TE rule query with object class regex match."""
        q = TERuleQuery(self.p, tclass="infoflow(5|6)", tclass_regex=True)

        r = sorted(q.results())
        self.assertEqual(len(r), 2)
        self.validate_rule(r[0], "allow", "test11", "test11", "infoflow5", set(["low_w"]))
        self.validate_rule(r[1], "allow", "test11", "test11", "infoflow6", set(["med_r"]))

    def test_012_perms_any(self):
        """TE rule query with permission set intersection."""
        q = TERuleQuery(self.p, perms=["super_r"], perms_equal=False)

        r = sorted(q.results())
        self.assertEqual(len(r), 2)
        self.validate_rule(r[0], "allow", "test12a", "test12a", "infoflow7", set(["super_r"]))
        self.validate_rule(r[1], "allow", "test12b", "test12b", "infoflow7",
                           set(["super_r", "super_none"]))

    def test_013_perms_equal(self):
        """TE rule query with permission set equality."""
        q = TERuleQuery(
            self.p, perms=["super_w", "super_none", "super_both"], perms_equal=True)

        r = sorted(q.results())
        self.assertEqual(len(r), 1)
        self.validate_rule(r[0], "allow", "test13c", "test13c", "infoflow7",
                           set(["super_w", "super_none", "super_both"]))

    def test_014_ruletype(self):
        """TE rule query with rule type match."""
        q = TERuleQuery(self.p, ruletype=["auditallow", "dontaudit"])

        r = sorted(q.results())
        self.assertEqual(len(r), 2)
        self.validate_rule(r[0], "auditallow", "test14", "test14", "infoflow7",
                           set(["super_both"]))
        self.validate_rule(r[1], "dontaudit", "test14", "test14", "infoflow7",
                           set(["super_unmapped"]))

    def test_100_default(self):
        """TE rule query with default type exact match."""
        q = TERuleQuery(self.p, default="test100d", default_regex=False)

        r = sorted(q.results())
        self.assertEqual(len(r), 1)
        self.validate_rule(r[0], "type_transition", "test100", "test100", "infoflow7", "test100d")

    def test_101_default_regex(self):
        """TE rule query with default type regex match."""
        q = TERuleQuery(self.p, default="test101.", default_regex=True)

        r = sorted(q.results())
        self.assertEqual(len(r), 2)
        self.validate_rule(r[0], "type_transition", "test101", "test101d", "infoflow7", "test101e")
        self.validate_rule(r[1], "type_transition", "test101", "test101e", "infoflow7", "test101d")

    def test_200_boolean_intersection(self):
        """TE rule query with intersection Boolean set match."""
        q = TERuleQuery(self.p, boolean=["test200"])

        r = sorted(q.results())
        self.assertEqual(len(r), 2)
        self.validate_rule(r[0], "allow", "test200t1", "test200t1", "infoflow7",
                           set(["super_w"]), cond="test200")
        self.validate_rule(r[1], "allow", "test200t2", "test200t2", "infoflow7",
                           set(["super_w"]), cond="test200a && test200")

    def test_201_boolean_equal(self):
        """TE rule query with equal Boolean set match."""
        q = TERuleQuery(self.p, boolean=["test201a", "test201b"], boolean_equal=True)

        r = sorted(q.results())
        self.assertEqual(len(r), 1)
        self.validate_rule(r[0], "allow", "test201t1", "test201t1", "infoflow7",
                           set(["super_unmapped"]), cond="test201b && test201a")

    def test_202_boolean_regex(self):
        """TE rule query with regex Boolean match."""
        q = TERuleQuery(self.p, boolean="test202(a|b)", boolean_regex=True)

        r = sorted(q.results())
        self.assertEqual(len(r), 2)
        self.validate_rule(r[0], "allow", "test202t1", "test202t1", "infoflow7",
                           set(["super_none"]), cond="test202a")
        self.validate_rule(r[1], "allow", "test202t2", "test202t2", "infoflow7",
                           set(["super_unmapped"]), cond="test202b || test202c")
