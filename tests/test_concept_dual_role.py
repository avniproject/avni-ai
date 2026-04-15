"""
Tests for dual-role concept conflict resolution.

When a concept name (e.g., "Eye Drop") is used both as a Coded question field
AND as an NA answer option in another field, the ConceptGenerator must produce
exactly one concept entry with a consistent UUID — not two entries with
different UUIDs and data types.
"""


from src.bundle.concepts import ConceptGenerator


class TestDualRoleConceptResolution:
    """Ensure no duplicate concepts when a name is both a question and an answer."""

    def test_answer_first_then_coded_question(self):
        """Eye Drop appears as NA answer first, then as Coded question."""
        cg = ConceptGenerator()

        uid_answer = cg.generate_answer_concept("Eye Drop")
        uid_coded = cg.generate_coded_concept(
            {"name": "Eye Drop", "options": ["Yes", "No"]}
        )

        assert uid_answer == uid_coded, "UUIDs must match for dual-role concept"

        eye_drops = [
            c for c in cg.generated_concepts if c["name"].lower() == "eye drop"
        ]
        assert len(eye_drops) == 1, f"Expected 1 entry, got {len(eye_drops)}"
        assert eye_drops[0]["dataType"] == "Coded", "Should be upgraded to Coded"

    def test_coded_question_first_then_answer(self):
        """Medicine appears as Coded question first, then as NA answer."""
        cg = ConceptGenerator()

        uid_coded = cg.generate_coded_concept(
            {"name": "Medicine", "options": ["Tablet", "Syrup"]}
        )
        uid_answer = cg.generate_answer_concept("Medicine")

        assert uid_coded == uid_answer, "UUIDs must match for dual-role concept"

        medicines = [
            c for c in cg.generated_concepts if c["name"].lower() == "medicine"
        ]
        assert len(medicines) == 1, f"Expected 1 entry, got {len(medicines)}"
        assert medicines[0]["dataType"] == "Coded", "Should remain Coded"

    def test_multiple_dual_role_concepts(self):
        """Multiple concepts used as both questions and answers."""
        cg = ConceptGenerator()

        dual_names = ["Eye Drop", "Medicine", "Nutri Kit", "Spectacles"]

        # All appear as answers first (in a coded field's options)
        answer_uids = {}
        for name in dual_names:
            answer_uids[name] = cg.generate_answer_concept(name)

        # Then all appear as coded questions
        coded_uids = {}
        for name in dual_names:
            coded_uids[name] = cg.generate_coded_concept(
                {"name": name, "options": ["Yes", "No"]}
            )

        # UUIDs must match
        for name in dual_names:
            assert answer_uids[name] == coded_uids[name], f"UUID mismatch for {name}"

        # Each should appear exactly once
        for name in dual_names:
            entries = [
                c for c in cg.generated_concepts if c["name"].lower() == name.lower()
            ]
            assert len(entries) == 1, f"{name}: expected 1 entry, got {len(entries)}"
            assert entries[0]["dataType"] == "Coded"

    def test_case_insensitive_dual_role(self):
        """Dual-role detection is case-insensitive."""
        cg = ConceptGenerator()

        uid1 = cg.generate_answer_concept("eye drop")
        uid2 = cg.generate_coded_concept({"name": "Eye Drop", "options": ["Yes", "No"]})

        assert uid1 == uid2
        entries = [c for c in cg.generated_concepts if c["name"].lower() == "eye drop"]
        assert len(entries) == 1

    def test_pure_answer_not_affected(self):
        """A concept that is ONLY an answer (never a question) stays as NA."""
        cg = ConceptGenerator()

        cg.generate_answer_concept("Yes")
        cg.generate_answer_concept("No")

        yes_entries = [c for c in cg.generated_concepts if c["name"] == "Yes"]
        assert len(yes_entries) == 1
        assert yes_entries[0]["dataType"] == "NA"

    def test_pure_coded_not_affected(self):
        """A concept that is ONLY a question (never an answer) stays as Coded."""
        cg = ConceptGenerator()

        cg.generate_coded_concept(
            {"name": "Blood Group", "options": ["A+", "B+", "O+"]}
        )

        bg_entries = [c for c in cg.generated_concepts if c["name"] == "Blood Group"]
        assert len(bg_entries) == 1
        assert bg_entries[0]["dataType"] == "Coded"
        assert len(bg_entries[0]["answers"]) == 3

    def test_answer_concepts_in_coded_field_reference_correct_uuid(self):
        """When Eye Drop is upgraded from NA to Coded, the answer references
        in other coded fields that list Eye Drop as an option should use
        the same UUID."""
        cg = ConceptGenerator()

        # "Material Distributed" has "Eye Drop" as an option
        cg.generate_coded_concept(
            {
                "name": "Material Distributed",
                "options": ["Eye Drop", "Medicine", "Nutri Kit"],
            }
        )

        # Then "Eye Drop" appears as its own coded question
        uid_coded = cg.generate_coded_concept(
            {"name": "Eye Drop", "options": ["Given", "Not Given"]}
        )

        # The UUID used in Material Distributed's answers should match
        mat = next(
            c for c in cg.generated_concepts if c["name"] == "Material Distributed"
        )
        eye_drop_answer = next(a for a in mat["answers"] if a["name"] == "Eye Drop")

        # The answer UUID in Material Distributed should equal the
        # standalone Eye Drop concept UUID
        assert eye_drop_answer["uuid"] == uid_coded
