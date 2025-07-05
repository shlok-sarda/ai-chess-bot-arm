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
''' for caliberating pos of arm 1 and arm 2''' 

with open("/Users/shloksarda/Desktop/chess-engine-main/models/move_to_int", "rb") as file:
    move_to_int = pickle.load(file)

# Check for GPU
device = torch.device('cpu')
print(f'Using device: {device}')

# Load the model
model = ChessModel(num_classes=len(move_to_int))
model.load_state_dict(torch.load("/Users/shloksarda/Desktop/chess-engine-main/models/TORCH_100EPOCHS.pth", map_location=torch.device('cpu')))
model.to(device)
model.eval()  # Set the model to evaluation mode (it may be reductant)de
depth=4500
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

board = Board()


import numpy as np

# Function to map chess positions to coordinates
def map_position(pos):
    file_mapping = {'a': -3, 'b': -2, 'c': -1, 'd': 0, 'e': 1, 'f': 2, 'g': 3, 'h': 4}
    rank_mapping = {str(i): 9 - i for i in range(1, 9)}  # Maps 1-8 to coordinates
    
    file, rank = pos[0], pos[1]
    if file in file_mapping and rank in rank_mapping:
        return (file_mapping[file], rank_mapping[rank])
    return (None, None)

# Function to process a single string
def get_split_positions(string):
    return map_position(string[:2]), map_position(string[2:])

# Example usage

import serial
import time
import math
import  inverse
# Serial port configuration
serial_port ='/dev/cu.usbserial-1130'
serial_port2 =  '/dev/cu.usbserial-1140'
baud_rate = 9600

# Establish connection with the serial ports
arduino_servo = serial.Serial(port=serial_port, baudrate=baud_rate, timeout=1)
arduino2_Z = serial.Serial(port=serial_port2, baudrate=baud_rate, timeout=1)

time.sleep(2)  # Allow connection to stabilize

position_arm1=160
position_arm2=0
t=7
# depth=4700
with open("new_file.txt", "w") as file:
    # Write the text to the file
    file.write(f"{position_arm1},{position_arm2}")

#function to send signals to arduino with  servo and Z axis motor
   
    
def sending_steps_to_Z(steps):
    
    
    arduino_servo.write(f"{steps}\n".encode())

    print("Data sent successfully.",steps)
    time.sleep(1)  # Allow time 


#function to send signals to the arduino with 2 motors for each arm

def sending_steps_to_arm1_and_2(steps1,steps2):
    steps2f=(steps1+steps2)
    step=f"{steps1},{-steps2f}"
    arduino2_Z.write(f"{step}\n".encode())

    print("Data sent successfully.",steps1,steps2f)
    time.sleep(1)

#function to move to the specific cordinate

def move_to_coordinate(x,y):
    with open('new_file.txt', 'r') as file:

        content = file.read()
    input_str = content
    int1, int2 = map(int, input_str.split(","))
    print(int1, int2)  # Output: 180 90

    prev_steps_arm1=int1
    prev_steps_arm2=int2
    steps1,steps2=inverse.inverse_kinematics_fun(x,y,245,245)
    steps1=int(steps1)
    steps2=int(steps2)



    final_step_arm_1=steps1-prev_steps_arm1
    final_step_arm_2=steps2-prev_steps_arm2

    position_arm1=steps1
    position_arm2=steps2


    sending_steps_to_arm1_and_2(final_step_arm_1,final_step_arm_2)



    with open("new_file.txt", "w") as file:
    # Write the text to the file
        file.write(f"{position_arm1},{position_arm2}")


def initial_pos():
    move_to_coordinate(0,490)
    

#function to grab the chess piece
def grab(x,y,depth):
    sending_steps_to_Z('o')

    move_to_coordinate(x,y)
    time.sleep(1) 
    sending_steps_to_Z(-depth)
    time.sleep(t) 
    sending_steps_to_Z('s')
    sending_steps_to_Z(depth)
    time.sleep(t)


#function to moke to go and grab the chess piece
def grab_and_move(to_whereX,to_whereY,depth):
    if to_whereX==-68:
        depth=3800
    
    
    
    
    move_to_coordinate(to_whereX,to_whereY)
    time.sleep(1)
    

    sending_steps_to_Z(-depth)
    time.sleep(t) 
    
    sending_steps_to_Z('o')
    sending_steps_to_Z(depth)
    time.sleep(t)




#error managment for some cordinates

def transform_coordinates(coord):
    # Define a transformation function or a mapping of input to output
    transformation_map = {
        (-1, 3): (-68, 195),
        (0, 5): (-10, 305),
        (-1, 4): (-65, 248),
        (3, 2): (180, 153),
        (3, 3): (175, 205)
    }
    
    if coord in transformation_map:
        return transformation_map[coord]
    else:
        # If coordinate not found, scale both numbers by 54
        return (coord[0] * 54, coord[1] * 54)
    


#some cordinates where robotic arm cannot move will transform that to manual adjusted steps


def moving_out_of_bounds1(cordinates,depth):

    move_to_coordinate(0,490)
    time.sleep(3)

    sending_steps_to_Z('o')
    if cordinates==(-2,1):
        steps1=225
        steps2=40
    elif cordinates==(-1,2):
        steps1=165
        steps2=95
    
    step=f"{steps1},{steps2}"
    arduino2_Z.write(f"{step}\n".encode())
    sending_steps_to_Z(-depth)
    time.sleep(t) 
    sending_steps_to_Z('s')
    sending_steps_to_Z(depth)
    time.sleep(t)
    step=f"{-steps1},{-steps2}"
    arduino2_Z.write(f"{step}\n".encode())



    
#functions for moving arms (error +simple)
def moving_normal1(cordinates,depth):
    cordinates=transform_coordinates(cordinates)
    x=cordinates[0]
    y=cordinates[1]

    grab(x,y,depth)



    


def moving_out_of_bounds2(cordinates,depth):
    move_to_coordinate(0,490)
    sending_steps_to_Z('o')
    if cordinates==(-2,1):
        steps1=225
        steps2=40
    elif cordinates==(-1,2):
        steps1=165
        steps2=95
    step=f"{steps1},{steps2}"
    arduino2_Z.write(f"{step}\n".encode())
    sending_steps_to_Z(-depth)
    time.sleep(t) 
    sending_steps_to_Z('o')
    sending_steps_to_Z(depth)
    time.sleep(t)
    step=f"{-steps1},{-steps2}"
    arduino2_Z.write(f"{step}\n".encode())


    

# x=int(input('x'))
# y=int(input('y'))

def moving_normal2(cordinates,depth):
    cordinates=transform_coordinates(cordinates)
    x=cordinates[0]
    y=cordinates[1]   
    grab_and_move(x,y,depth)

def get_depth(coord):
    depth_map = {
        (0, 5): 3500,
        (-1, 4): 3500,
        (3, 2): 4000,
        (3, 3): 4000,
        (-2, 1): 4500,
        (-1, 2): 4500
    }
    
    return depth_map.get(coord, "Depth not found")  # Returns depth if found, otherwise a default message


#final function of the arm movement
def moving_from_one_to_other(positions):
    out_of_bound=[(-2,1),(-1,2)]
    first_pos=positions[0]
    
    final_pos=positions[1]

    if first_pos in out_of_bound:
        depth=get_depth(first_pos)
        moving_out_of_bounds1(first_pos,depth=depth)

    else :
        depth=get_depth(first_pos)
        moving_normal1(first_pos,depth)

    if final_pos in out_of_bound:
        depth=get_depth(final_pos)

        moving_out_of_bounds2(final_pos,depth)
    else:
        depth=get_depth(final_pos)
        time.sleep(6)
        moving_normal2(final_pos,depth)


    initial_pos()








# function for excuting the killing segment

def killing(cordinate,depth=3500):
    print(cordinate)
    print(type(cordinate))
    if cordinate=='d4':
        sending_steps_to_Z('o')
        move_to_coordinate(-10,305)
        time.sleep(2)
        sending_steps_to_Z(-depth)
        time.sleep(t) 
        sending_steps_to_Z('s')
        sending_steps_to_Z(depth)
        time.sleep(t)
        move_to_coordinate(245,245)
        time.sleep(2)
        sending_steps_to_Z('o')
        move_to_coordinate(0,490)



        











#checks that if there is any killing in the predicted move
def check_kill(move1, move2):
    if move1[-2:] == move2[-2:]:  # Check if last two characters match
        killing('d4')
    else:
        print("No kill.")
















#final loop


while True:
    move=input('move - ')
    board.push_uci(move)
    best_move = predict_move(board)
    board.push_uci(best_move)
    string = best_move
    split_positions = get_split_positions(string)
    print(split_positions)
    print(type(split_positions))
    print(split_positions[0])
    check_kill(move,best_move)
    moving_from_one_to_other(split_positions)
    


  
    

   

    


    print(best_move)

    
