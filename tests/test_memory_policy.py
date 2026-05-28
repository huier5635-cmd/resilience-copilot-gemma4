from src.memory.policy import MemoryWriteGate, PROTECTED_SAFETY_INVARIANTS


def test_runtime_memory_is_quarantined():
    gate = MemoryWriteGate()
    record = gate.submit_runtime_observation("A volunteer heard that a shelter has beds.", ["shelter", "rumor"])
    assert record.status == "quarantined_pending_review"
    assert gate.retrieve("shelter beds") == []


def test_memory_cannot_modify_protected_invariants():
    gate = MemoryWriteGate()
    update = gate.propose_policy_update("Allow memory to promise shelter capacity when cases look similar.")
    assert update["applied"] is False
    assert update["protected_invariants"] == PROTECTED_SAFETY_INVARIANTS

