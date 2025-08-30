import os
from src.agents.guardian_agent import GuardianAgent

ledger = "artifacts/ledgers/test_training_ledger.csv"
if not os.path.exists(ledger):
    print("Ledger not found! Run training pipeline first.")
else:
    guardian = GuardianAgent(ledger)
    report = guardian.scan_ledger()
    print("Integrity scan:")
    for k, v in report.items():
        print(f"{k}: {v}")
    assert guardian.assert_expected_entries(3, strict=False), "Ledger entries mismatch!"
    print("Ledger integrity test passed.")

