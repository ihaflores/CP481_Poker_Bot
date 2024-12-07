const players = [
    { id: 0, stack: 10000, status: 'Active', hand: "(7d, 5h)" },
    { id: 1, stack: 10000, status: 'Active', hand: "(7s, Qd)" },
    { id: 2, stack: 10000, status: 'Active', hand: "(Kc, Jd)" },
];
let pot = 600;
let boardCards = {
    'Flop': '(Ah, Kd, 2c)',
    'Turn': '(Ah, Kd, 2c, Js)',
    'River': '(Ah, Kd, 2c, Js, 10h)'
};
const rounds = ["Pre-flop", "Flop", "Turn", "River"];
let currentRoundIndex = 0;
let currentPlayerIndex = 0;
let gameOver = false;

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
    document.getElementById('board').textContent = boardCards[rounds[currentRoundIndex]] || '';
    document.getElementById('current-round').textContent = rounds[currentRoundIndex];
    updateCurrentPlayerUI();
}

function updateCurrentPlayerUI() {
    const player = players[currentPlayerIndex];
    document.getElementById('current-player-id').textContent = `Player ${player.id}`;
    document.getElementById('hand-strength').textContent = (Math.random() * 0.5 + 0.2).toFixed(3);
    document.getElementById('call-amount').textContent = 400;
    document.getElementById('min-bet').textContent = 800;
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
    if (cards) {
        document.getElementById('board').textContent = cards;
    }
}

function updatePot(amount) {
    pot += amount;
    document.getElementById('pot-amount').textContent = pot;
}

function nextPlayer() {
    currentPlayerIndex = (currentPlayerIndex + 1) % players.length;
    if (players[currentPlayerIndex].status === 'Folded') {
        nextPlayer();
    } else {
        updateCurrentPlayerUI();
    }
}

function performAction(action) {
    if (gameOver) return;

    const player = players[currentPlayerIndex];
    addLog(`Player ${player.id} performed: ${action}`);

    const activePlayers = players.filter(p => p.status === 'Active');
    if (activePlayers.length === 1) {
        determineWinner();
        return;
    }

    if (action === 'check') {
        if (currentRoundIndex === rounds.length - 1) {
            determineWinner();
        } else {
            currentRoundIndex++;
            if (rounds[currentRoundIndex] !== 'Pre-flop') {
                updateBoard(boardCards[rounds[currentRoundIndex]]);
            }
            nextPlayer();
        }
    } else if (action === 'fold') {
        player.status = 'Folded';
        addLog(`Player ${player.id} has folded.`);
        const remainingPlayers = players.filter(p => p.status === 'Active');
        if (remainingPlayers.length === 1) {
            determineWinner();
            return;
        }
        nextPlayer();
    } else {
        nextPlayer();
    }
}

function determineWinner() {
    gameOver = true;
    const activePlayers = players.filter(player => player.status === 'Active');
    const winner = activePlayers[0];
    
    winner.stack += pot;
    pot = 0;
    
    addLog(`The winner is Player ${winner.id} with stack ${winner.stack}!`);
    endGame(winner);
}

function endGame(winner) {
    gameOver = true;
    document.getElementById('actions').style.display = 'none';
    document.getElementById('new-game').style.display = 'block';
    addLog(`Game Over! Winning Hand: ${winner.hand}`);
    initializeGame();
}

function startNewGame() {
    location.reload();
}

function openBetUI() {
    document.getElementById('bet-raise-ui').style.display = 'block';
}

function openRaiseUI() {
    document.getElementById('bet-raise-ui').style.display = 'block';
}

function submitBetRaise() {
    const amount = parseInt(document.getElementById('bet-amount').value, 10);
    const player = players[currentPlayerIndex];
    addLog(`Player ${player.id} placed bet/raise: ${amount}`);
    updatePlayerStack(player.id, -amount);
    updatePot(amount);
} 