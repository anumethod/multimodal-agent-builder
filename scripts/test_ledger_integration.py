import os
from src.utils.training_utils import AdaptiveTrainingManager

# Test output folder for ledgers
os.makedirs("artifacts/ledgers", exist_ok=True)

manager = AdaptiveTrainingManager(ledger_file="artifacts/ledgers/test_training_ledger.csv")
training_data = [{"caption": "pattern test"}] * 3
results = manager.create_training_loop(model_name="TestModel", training_data=training_data, epochs=3)

print("Ledger path:", manager.ledger.ledger_file)
print("Training results:", results)
print("Ledger DF:")
print(manager.ledger.get_ledger_df())

