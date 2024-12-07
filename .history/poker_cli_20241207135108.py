<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Poker Game UI</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #2b2b2b;
            color: #ffffff;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        #game-board {
            width: 80%;
            margin: 20px;
            padding: 20px;
            background-color: #333;
            border-radius: 10px;
        }
        .player {
            margin: 10px 0;
            display: flex;
            justify-content: space-between;
            padding: 10px;
            background: #444;
            border-radius: 5px;
        }
        #actions {
            margin-top: 20px;
        }
        button {
            background-color: #4caf50;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 5px;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        #logs {
            margin-top: 20px;
            background-color: #222;
            padding: 10px;
            border-radius: 5px;
            height: 150px;
            overflow-y: scroll;
        }
    </style>
</head>
<body>
    <h1>Poker Game</h1>
    <div id="game-board">
        <div id="players">
            <!-- Player info will be dynamically added here -->
        </div>
        <div id="board-cards">
            <!-- Board cards will be shown here -->
            <h2>Board Cards: <span id="board"></span></h2>
        </div>
        <div id="pot">
            <h3>Pot: <span id="pot-amount">0</span></h3>
        </div>
    </div>
    <div id="actions">
        <button onclick="performAction('check')">Check</button>
        <button onclick="performAction('call')">Call</button>
        <button onclick="openBetUI()">Bet</button>
        <button onclick="openRaiseUI()">Raise</button>
        <button onclick="performAction('fold')">Fold</button>
        <div id="bet-raise-ui" style="display:none;">
            <input type="number" id="bet-amount" placeholder="Enter amount" />
            <button onclick="submitBetRaise()">Submit</button>
        </div>
    </div>
    <div id="logs">
        <!-- Game logs will be dynamically added here -->
    </div>

    <script>
        // Example dynamic data
        const players = [
            { id: 0, stack: 10000, status: 'Active', hand: "(7d, 5h)" },
            { id: 1, stack: 10000, status: 'Active', hand: "(7s, Qd)" },
            { id: 2, stack: 10000, status: 'Active', hand: "(Kc, Jd)" },
        ];
        let pot = 0;
        let boardCards = "";

        function initializeGame() {
            const playersDiv = document.getElementById('players');
            playersDiv.innerHTML = '';

            players.forEach(player => {
                const playerDiv = document.createElement('div');
                playerDiv.className = 'player';
                playerDiv.innerHTML = `
                    <span>Player ${player.id}</span>
                    <span>Stack: ${player.stack}</span>
                    <span>Status: ${player.status}</span>
                    <span>Hand: ${player.hand}</span>
                `;
                playersDiv.appendChild(playerDiv);
            });

            document.getElementById('pot-amount').textContent = pot;
            document.getElementById('board').textContent = boardCards;
        }

        function updatePlayerStack(playerId, amount) {
            const player = players.find(p => p.id === playerId);
            if (player) {
                player.stack += amount;
                pot -= amount;
                initializeGame();
            }
        }

        function updateBoard(cards) {
            boardCards = cards;
            document.getElementById('board').textContent = boardCards;
        }

        function updatePot(amount) {
            pot += amount;
            document.getElementById('pot-amount').textContent = pot;
        }

        function performAction(action) {
            addLog(`Player ${players[0].id} performed: ${action}`);
            if (action === 'call') {
                updatePlayerStack(0, -200);
                updatePot(200);
            } else if (action === 'bet') {
                updatePlayerStack(1, -500);
                updatePot(500);
            } else if (action === 'fold') {
                players[2].status = 'Folded';
                initializeGame();
            }
        }

        function openBetUI() {
            document.getElementById('bet-raise-ui').style.display = 'block';
        }

        function openRaiseUI() {
            document.getElementById('bet-raise-ui').style.display = 'block';
        }

        function submitBetRaise() {
            const amount = parseInt(document.getElementById('bet-amount').value, 10);
            addLog(`Player ${players[2].id} placed bet/raise: ${amount}`);
            updatePlayerStack(2, -amount);
            updatePot(amount);
            document.getElementById('bet-raise-ui').style.display = 'none';
            document.getElementById('bet-amount').value = '';
        }

        function addLog(message) {
            const logsDiv = document.getElementById('logs');
            const logEntry = document.createElement('div');
            logEntry.textContent = message;
            logsDiv.appendChild(logEntry);
            logsDiv.scrollTop = logsDiv.scrollHeight;
        }

        // Initialize the UI
        initializeGame();
    </script>
</body>
</html>
