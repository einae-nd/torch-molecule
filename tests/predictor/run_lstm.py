import numpy as np
from torch_molecule import LSTMMolecularPredictor
from torch_molecule.utils.search import ParameterType, ParameterSpec
import torch
def test_lstm_predictor():
    # Test data
    smiles_list = [
        'CNC[C@H]1OCc2cnnn2CCCC(=O)N([C@H](C)CO)C[C@@H]1C',
        'CNC[C@@H]1OCc2cnnn2CCCC(=O)N([C@H](C)CO)C[C@H]1C',
        'C[C@H]1CN([C@@H](C)CO)C(=O)CCCn2cc(nn2)CO[C@@H]1CN(C)C(=O)CCC(F)(F)F',
        'CC1=CC=C(C=C1)C2=CC(=NN2C3=CC=C(C=C3)S(=O)(=O)N)C(F)(F)F'  # Additional molecule
    ]
    properties = np.array([0, 0, 1, 1])  # Binary classification

    # 1. Basic initialization test
    print("\n=== Testing model initialization ===")
    model = LSTMMolecularPredictor(
        task_type="regression",
        output_dim=15,
        LSTMunits=60,
        batch_size=2,
        epochs=2,
        device="cpu",
        verbose=True
    )
    print("Model initialized successfully")

    # 2. Basic fitting test
    print("\n=== Testing model fitting ===")
    model.fit(smiles_list[:3], properties[:3])
    print("Model fitting completed")

    # 3. Prediction test
    print("\n=== Testing model prediction ===")
    predictions = model.predict(smiles_list[3:])
    print(f"Prediction shape: {predictions['prediction'].shape}")
    print(f"Prediction for new molecule: {predictions['prediction']}")

    # 4. Auto-fitting test with custom parameters
    print("\n=== Testing model auto-fitting ===")

    search_parameters = {
        "output_dim": ParameterSpec(ParameterType.INTEGER, (8, 32)),
        "LSTMunits": ParameterSpec(ParameterType.INTEGER, (30, 120)),
        # Float-valued parameters with log scale
        "learning_rate": ParameterSpec(ParameterType.LOG_FLOAT, (1e-4, 1e-2)),
    }
    model_auto = LSTMMolecularPredictor(
        num_task=1,
        task_type="regression",
        epochs=3,  # Small number for testing
        # verbose=True
        verbose=True
    )
    
    model_auto.autofit(
        smiles_list,
        properties,
        search_parameters=search_parameters,
        n_trials=2  # Small number for testing
    )
    print("Model auto-fitting completed")

    # 5. Model saving and loading test
    print("\n=== Testing model saving and loading ===")
    save_path = "test_model.pt"
    model.save_to_local(save_path)
    print(f"Model saved to {save_path}")

    print(f"Device: {torch.device('cuda' if torch.cuda.is_available() else 'cpu')}")
    new_model = LSTMMolecularPredictor(
        task_type="regression",
        output_dim=15,
        LSTMunits=60,
        batch_size=2,
        epochs=2,
        # device="cpu"
        device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
    )
    new_model.load_from_local(save_path)
    print("Model loaded successfully")

    # Clean up
    import os
    if os.path.exists(save_path):
        os.remove(save_path)
        print(f"Cleaned up {save_path}")

if __name__ == "__main__":
    test_lstm_predictor()


