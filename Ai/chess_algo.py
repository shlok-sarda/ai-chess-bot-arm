from chess import Board, pgn
from auxiliary_func import board_to_matrix
import torch
from model import ChessModel
import pickle
import numpy as np


def prepare_input(board: Board):
    matrix = board_to_matrix(board)
    X_tensor = torch.tensor(matrix, dtype=torch.float32).unsqueeze(0)
    return X_tensor

with open("/Users/shloksarda/Desktop/chess-engine-main/models/move_to_int", "rb") as file:
    move_to_int = pickle.load(file)

# Check for GPU
device = torch.device('cpu')
print(f'Using device: {device}')

# Load the model
model = ChessModel(num_classes=len(move_to_int))
model.load_state_dict(torch.load("/Users/shloksarda/Desktop/chess-engine-main/models/TORCH_100EPOCHS.pth", map_location=torch.device('cpu')))
model.to(device)
model.eval()  # Set the model to evaluation mode (it may be reductant)

int_to_move = {v: k for k, v in move_to_int.items()}
# Function to make predictions
def predict_move(board: Board):
    X_tensor = prepare_input(board).to(device)
    
    with torch.no_grad():
        logits = model(X_tensor)
    
    logits = logits.squeeze(0)  # Remove batch dimension
    
    probabilities = torch.softmax(logits, dim=0).cpu().numpy()  # Convert to probabilities
    legal_moves = list(board.legal_moves)
    legal_moves_uci = [move.uci() for move in legal_moves]
    sorted_indices = np.argsort(probabilities)[::-1]
    for move_index in sorted_indices:
        move = int_to_move[move_index]
        if move in legal_moves_uci:
            return move
    
    return None

def play():
    board = Board()
    checkmate=True
    while checkmate:
        playermove=input('input your move shlok')
        board.push_uci(playermove)

        best_move = predict_move(board)
        print(best_move)
        board.push_uci(best_move)
        board

play()