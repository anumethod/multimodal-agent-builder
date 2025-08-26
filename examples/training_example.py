"""Example usage of the training API with recursive loop closure."""

import asyncio
import requests
import json
from typing import Dict, Any


class TrainingAPIClient:
    """Client for interacting with the training API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the training client.
        
        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url
        self.training_url = f"{base_url}/training"
    
    def start_training(
        self,
        agent_name: str,
        dataset_type: str = "open_images",
        epochs: int = 3
    ) -> Dict[str, Any]:
        """Start training for an agent.
        
        Args:
            agent_name: Name of the agent to train
            dataset_type: Type of dataset to use
            epochs: Number of training epochs
            
        Returns:
            Training status
        """
        response = requests.post(
            f"{self.training_url}/start",
            json={
                "agent_name": agent_name,
                "dataset_type": dataset_type,
                "epochs": epochs,
                "enable_closure": True
            }
        )
        response.raise_for_status()
        return response.json()
    
    def check_training_status(self, agent_name: str) -> Dict[str, Any]:
        """Check training status for an agent.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Current training status
        """
        response = requests.get(f"{self.training_url}/status/{agent_name}")
        response.raise_for_status()
        return response.json()
    
    def log_closure(
        self,
        hypothesis: str,
        pattern: str,
        structure: str,
        explanation: str,
        topic: str = ""
    ) -> Dict[str, Any]:
        """Log a recursive loop closure.
        
        Args:
            hypothesis: Hypothesis being tested
            pattern: Pattern identified
            structure: Structure used
            explanation: Why the loop was closed
            topic: Optional topic
            
        Returns:
            Closure confirmation
        """
        response = requests.post(
            f"{self.training_url}/closure",
            json={
                "hypothesis": hypothesis,
                "pattern": pattern,
                "structure": structure,
                "explanation": explanation,
                "topic": topic
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_ledger(self, agent_name: str) -> Dict[str, Any]:
        """Get the recursive loop closure ledger.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Ledger information
        """
        response = requests.get(f"{self.training_url}/ledger/{agent_name}")
        response.raise_for_status()
        return response.json()
    
    def get_summary(self, agent_name: str) -> Dict[str, Any]:
        """Get comprehensive training summary.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Training summary
        """
        response = requests.get(f"{self.training_url}/summary/{agent_name}")
        response.raise_for_status()
        return response.json()
    
    def create_pipeline(
        self,
        agent_name: str,
        dataset_type: str = "open_images"
    ) -> Dict[str, Any]:
        """Create and run a complete training pipeline.
        
        Args:
            agent_name: Name of the agent
            dataset_type: Type of dataset
            
        Returns:
            Pipeline results
        """
        response = requests.post(
            f"{self.training_url}/pipeline/{agent_name}",
            params={"dataset_type": dataset_type}
        )
        response.raise_for_status()
        return response.json()
    
    def list_datasets(self) -> Dict[str, Any]:
        """List available training datasets.
        
        Returns:
            Available datasets
        """
        response = requests.get(f"{self.training_url}/datasets")
        response.raise_for_status()
        return response.json()
    
    def reset_training(self, agent_name: str) -> Dict[str, Any]:
        """Reset training for an agent.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Confirmation message
        """
        response = requests.delete(f"{self.training_url}/reset/{agent_name}")
        response.raise_for_status()
        return response.json()


async def demo_training_workflow():
    """Demonstrate the complete training workflow."""
    
    client = TrainingAPIClient()
    agent_name = "vision_agent_v1"
    
    print("🚀 Training API Demo")
    print("=" * 50)
    
    try:
        # 1. List available datasets
        print("\n📊 Available Datasets:")
        datasets = client.list_datasets()
        for dataset_name, info in datasets["datasets"].items():
            print(f"  - {dataset_name}: {info['description']}")
            print(f"    Training files: {len(info['training_files'])}")
            print(f"    Validation files: {len(info['validation_files'])}")
        
        # 2. Start training
        print(f"\n🎯 Starting training for {agent_name}...")
        result = client.start_training(
            agent_name=agent_name,
            dataset_type="open_images",
            epochs=3
        )
        print(f"  Status: {result['status']}")
        print(f"  Message: {result['message']}")
        
        # 3. Monitor training progress
        print("\n📈 Monitoring training progress...")
        for i in range(5):
            await asyncio.sleep(2)  # Wait 2 seconds
            status = client.check_training_status(agent_name)
            print(f"  [{i+1}/5] Status: {status['status']}")
            print(f"    - Loops closed: {status['loops_closed']}")
            print(f"    - Patterns found: {status['patterns_found']}")
            
            if status['status'] == 'completed':
                print(f"    - Accuracy: {status['accuracy']:.2%}")
                break
        
        # 4. Log a manual closure
        print("\n🔒 Logging manual loop closure...")
        closure_result = client.log_closure(
            hypothesis="Manual testing confirms pattern recognition",
            pattern="Consistent object detection in images",
            structure="CNN-based vision model",
            explanation="Pattern recognition achieved 95% accuracy threshold",
            topic="Manual Vision Test"
        )
        print(f"  Loop ID: {closure_result['loop_id']}")
        print(f"  Total loops: {closure_result['total_loops']}")
        
        # 5. Get training ledger
        print("\n📜 Training Ledger:")
        ledger = client.get_ledger(agent_name)
        print(f"  Total loops closed: {ledger['total_loops']}")
        print(f"  Closure rate: {ledger['closure_rate']:.2%}")
        
        if ledger['recent_loops']:
            print("  Recent loops:")
            for loop in ledger['recent_loops'][:3]:
                print(f"    - {loop['Loop ID']}: {loop['Topic']}")
        
        # 6. Get comprehensive summary
        print("\n📋 Training Summary:")
        summary = client.get_summary(agent_name)
        print(f"  Total iterations: {summary['total_iterations']}")
        print(f"  Loops closed: {summary['loops_closed']}")
        print(f"  Patterns discovered: {summary['patterns_discovered']}")
        
        # 7. Create a pipeline (alternative workflow)
        print("\n🔧 Creating training pipeline for new agent...")
        pipeline_agent = "vision_agent_v2"
        pipeline_result = client.create_pipeline(
            agent_name=pipeline_agent,
            dataset_type="open_images"
        )
        print(f"  Success: {pipeline_result['success']}")
        print(f"  Message: {pipeline_result['message']}")
        
        # Clean up
        print("\n🧹 Cleaning up...")
        client.reset_training(agent_name)
        client.reset_training(pipeline_agent)
        print("  Training reset complete")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ API Error: {e}")
        print("Make sure the API server is running!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n✅ Training demo complete!")


def demo_closure_tracking():
    """Demonstrate recursive loop closure tracking."""
    
    client = TrainingAPIClient()
    
    print("🔄 Recursive Loop Closure Demo")
    print("=" * 50)
    
    # Define test closures
    test_closures = [
        {
            "hypothesis": "Agent learns spatial relationships in images",
            "pattern": "Consistent bounding box predictions",
            "structure": "Object detection network",
            "explanation": "Spatial accuracy > 90% on validation set",
            "topic": "Spatial Learning"
        },
        {
            "hypothesis": "Audio transcription improves with context",
            "pattern": "Context-aware speech recognition",
            "structure": "Transformer-based ASR model",
            "explanation": "WER reduced by 15% with context",
            "topic": "Audio Context Learning"
        },
        {
            "hypothesis": "Multimodal fusion enhances understanding",
            "pattern": "Cross-modal attention patterns",
            "structure": "Multimodal transformer",
            "explanation": "Combined accuracy exceeds individual modalities",
            "topic": "Multimodal Fusion"
        }
    ]
    
    print("\n📝 Logging test closures...")
    for closure in test_closures:
        result = client.log_closure(**closure)
        print(f"  ✓ {closure['topic']}: {result['loop_id']}")
    
    print("\n🎯 Closures logged successfully!")


if __name__ == "__main__":
    print("Choose demo:")
    print("1. Full training workflow (async)")
    print("2. Closure tracking demo")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        asyncio.run(demo_training_workflow())
    elif choice == "2":
        demo_closure_tracking()
    else:
        print("Invalid choice. Running closure tracking demo...")
        demo_closure_tracking()
