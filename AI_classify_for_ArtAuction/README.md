AI Module Setup and Usage

1. Create virtual environment (optional)
-------------------------------------
python -m venv venv

Activate virtual environment:
- Windows:
  venv\Scripts\activate
- Linux / macOS:
  source venv/bin/activate


2. Install dependencies
-----------------------
pip install -r requirements.txt


3. Prepare dataset
------------------
Split raw dataset into training and validation sets:
python src/split_dataset.py --raw_dir ./data_raw --out_dir ./data --train_ratio 0.8


4. Train the model
------------------
Train model with default configuration:
python src/train.py --data_dir ./data --epochs 30 --batch_size 32 --num_workers 4 --patience 5

Train model and save outputs:
python src/train.py --out_dir ./outputs

Resume training from a checkpoint:
python src/train.py --data_dir ./data --epochs 30 --resume outputs/checkpoints/best_model.pth


5. Evaluate the model
---------------------
Evaluate using a trained checkpoint:
python src/evaluate.py --data_dir ./data --checkpoint outputs/checkpoints/best_model.pth

Quick evaluation:
python src/evaluate.py


6. Run AI API (Flask)
---------------------
Start the Flask API server:
python flask_api.py


7. Monitor training with TensorBoard
------------------------------------
View training logs and metrics:
venv\Scripts\tensorboard.exe --logdir outputs\logs --bind_all
