Chess AI ♟️
This project is a chess AI developed for my A-level computer science coursework. While the code has been refined since the final submission, the core functionality remains the same. The AI is a demonstration of game theory and search algorithms in a practical application.

Features
Minimax Algorithm: The AI uses a minimax algorithm to determine the optimal move by exploring potential game states.

Game Engine: A custom game engine handles all the standard rules of chess, including piece movements, captures, and check detection.

Modularity: The project is divided into logical components, making it easier to understand and extend.

How to Run
Clone the repository:

git clone https://github.com/Adu-Kwame/Chess.git
cd chess

Run the main script:

python chess.py

Code Structure
chess.py: The main program that orchestrates the game. It imports and uses the aicode.py and engine.py modules to run the chess game.

aicode.py: Contains the core AI logic, including the minimax algorithm and future plans for alpha-beta pruning. This is where the "brain" of the AI resides.

engine.py: Manages the rules of the game. It handles board state, piece movements, and determines valid moves.

Future Improvements
Alpha-Beta Pruning: Implement this optimization to significantly improve the AI's search efficiency.

GUI: Add a graphical user interface to make the game more interactive.

Evaluation Function: Refine the heuristic evaluation function to make the AI a stronger player.
