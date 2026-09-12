import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Manual Ludo Game",
    page_icon="🎲",
    layout="wide"
)

# Inline responsive HTML, CSS, and JS bundle
LUDO_HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Ludo Game</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background-color: #1a233a;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 12px;
        }

        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 16px;
            max-width: 600px;
            width: 100%;
            background-color: #24304d;
            padding: 16px;
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        }

        @media (min-width: 850px) {
            .container {
                flex-direction: row;
                max-width: 1000px;
                align-items: flex-start;
                padding: 24px;
            }
        }

        #board-wrapper {
            position: relative;
            width: 100%;
            aspect-ratio: 1 / 1;
            max-width: 500px;
            background-color: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            flex-shrink: 0;
            border: 4px solid #111827;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }

        .board-bg {
            width: 100%;
            height: 100%;
            display: block;
        }

        .pawn-svg {
            position: absolute;
            width: 7.5%;
            height: 7.5%;
            transform: translate(-50%, -50%);
            transition: left 0.22s ease-out, top 0.22s ease-out;
            z-index: 10;
            cursor: pointer;
            filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.5));
            touch-action: manipulation;
        }

        .pawn-svg.selected {
            filter: drop-shadow(0 0 8px #ffff00) drop-shadow(0 0 3px #ffff00);
            transform: translate(-50%, -50%) scale(1.3);
            z-index: 20;
        }

        .rank-badge {
            position: absolute;
            width: 40%;
            height: 40%;
            display: none;
            justify-content: center;
            align-items: center;
            font-size: clamp(28px, 8vw, 48px);
            font-weight: 900;
            color: #ffffff;
            text-shadow: 0px 3px 8px rgba(0,0,0,0.8);
            border-radius: 12px;
            background: rgba(0, 0, 0, 0.65);
            backdrop-filter: blur(2px);
            z-index: 30;
            border: 3px solid #ffffff;
            animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        @keyframes popIn {
            0% { transform: scale(0.5); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }

        #rank-G { left: 0; top: 0; }
        #rank-Y { right: 0; top: 0; }
        #rank-R { left: 0; bottom: 0; }
        #rank-B { right: 0; bottom: 0; }

        .controls {
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .section-title {
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 8px;
            color: #d1d5db;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .btn-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 6px;
        }

        .btn-grid-pawns {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
        }

        button {
            padding: 12px 6px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
            cursor: pointer;
            background-color: #ffffff;
            color: #333333;
            transition: background 0.15s, transform 0.1s;
            touch-action: manipulation;
            user-select: none;
        }

        button:active {
            transform: scale(0.96);
        }

        button.active {
            background-color: #ff9800;
            color: #ffffff;
            box-shadow: 0 0 10px rgba(255, 152, 0, 0.6);
        }

        .btn-dice {
            background-color: #ff9800;
            color: #ffffff;
            font-size: 16px;
        }

        .btn-pawn-r { background-color: #db4437; color: white; }
        .btn-pawn-g { background-color: #0f9d58; color: white; }
        .btn-pawn-y { background-color: #f4b400; color: black; }
        .btn-pawn-b { background-color: #4285f4; color: white; }

        .btn-action {
            background-color: #8e24aa;
            color: white;
            padding: 14px;
            font-size: 15px;
            width: 100%;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }

        .log-box {
            background-color: #111827;
            border-radius: 8px;
            padding: 10px 12px;
            height: 140px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 12px;
            color: #10b981;
            line-height: 1.5;
            border: 1px solid #374151;
        }
    </style>
</head>
<body>

<div class="container">
    <div id="board-wrapper">
        <svg class="board-bg" viewBox="0 0 1500 1500">
            <rect x="0" y="0" width="1500" height="1500" fill="#ffffff" stroke="#000000" stroke-width="10"/>

            <!-- Green Base -->
            <rect x="0" y="0" width="600" height="600" fill="#0f9d58" stroke="#000000" stroke-width="8"/>
            <rect x="100" y="100" width="400" height="400" fill="#ffffff" stroke="#000000" stroke-width="6"/>
            <circle cx="200" cy="200" r="60" fill="#0f9d58"/>
            <circle cx="400" cy="200" r="60" fill="#0f9d58"/>
            <circle cx="200" cy="400" r="60" fill="#0f9d58"/>
            <circle cx="400" cy="400" r="60" fill="#0f9d58"/>

            <!-- Yellow Base -->
            <rect x="900" y="0" width="600" height="600" fill="#f4b400" stroke="#000000" stroke-width="8"/>
            <rect x="1000" y="100" width="400" height="400" fill="#ffffff" stroke="#000000" stroke-width="6"/>
            <circle cx="1100" cy="200" r="60" fill="#f4b400"/>
            <circle cx="1300" cy="200" r="60" fill="#f4b400"/>
            <circle cx="1100" cy="400" r="60" fill="#f4b400"/>
            <circle cx="1300" cy="400" r="60" fill="#f4b400"/>

            <!-- Red Base -->
            <rect x="0" y="900" width="600" height="600" fill="#db4437" stroke="#000000" stroke-width="8"/>
            <rect x="100" y="1000" width="400" height="400" fill="#ffffff" stroke="#000000" stroke-width="6"/>
            <circle cx="200" cy="1100" r="60" fill="#db4437"/>
            <circle cx="400" cy="1100" r="60" fill="#db4437"/>
            <circle cx="200" cy="1300" r="60" fill="#db4437"/>
            <circle cx="400" cy="1300" r="60" fill="#db4437"/>

            <!-- Blue Base -->
            <rect x="900" y="900" width="600" height="600" fill="#4285f4" stroke="#000000" stroke-width="8"/>
            <rect x="1000" y="1000" width="400" height="400" fill="#ffffff" stroke="#000000" stroke-width="6"/>
            <circle cx="1100" cy="1100" r="60" fill="#4285f4"/>
            <circle cx="1300" cy="1100" r="60" fill="#4285f4"/>
            <circle cx="1100" cy="1300" r="60" fill="#4285f4"/>
            <circle cx="1300" cy="1300" r="60" fill="#4285f4"/>

            <!-- Grid Lines -->
            <line x1="0" y1="700" x2="600" y2="700" stroke="#000000" stroke-width="5"/>
            <line x1="0" y1="800" x2="600" y2="800" stroke="#000000" stroke-width="5"/>
            <line x1="900" y1="700" x2="1500" y2="700" stroke="#000000" stroke-width="5"/>
            <line x1="900" y1="800" x2="1500" y2="800" stroke="#000000" stroke-width="5"/>
            
            <line x1="700" y1="0" x2="700" y2="600" stroke="#000000" stroke-width="5"/>
            <line x1="800" y1="0" x2="800" y2="600" stroke="#000000" stroke-width="5"/>
            <line x1="700" y1="900" x2="700" y2="1500" stroke="#000000" stroke-width="5"/>
            <line x1="800" y1="900" x2="800" y2="1500" stroke="#000000" stroke-width="5"/>

            <line x1="100" y1="600" x2="100" y2="900" stroke="#000" stroke-width="4"/><line x1="200" y1="600" x2="200" y2="900" stroke="#000" stroke-width="4"/><line x1="300" y1="600" x2="300" y2="900" stroke="#000" stroke-width="4"/><line x1="400" y1="600" x2="400" y2="900" stroke="#000" stroke-width="4"/><line x1="500" y1="600" x2="500" y2="900" stroke="#000" stroke-width="4"/>
            <line x1="1000" y1="600" x2="1000" y2="900" stroke="#000" stroke-width="4"/><line x1="1100" y1="600" x2="1100" y2="900" stroke="#000" stroke-width="4"/><line x1="1200" y1="600" x2="1200" y2="900" stroke="#000" stroke-width="4"/><line x1="1300" y1="600" x2="1300" y2="900" stroke="#000" stroke-width="4"/><line x1="1400" y1="600" x2="1400" y2="900" stroke="#000" stroke-width="4"/>

            <line x1="600" y1="100" x2="900" y2="100" stroke="#000" stroke-width="4"/><line x1="600" y1="200" x2="900" y2="200" stroke="#000" stroke-width="4"/><line x1="600" y1="300" x2="900" y2="300" stroke="#000" stroke-width="4"/><line x1="600" y1="400" x2="900" y2="400" stroke="#000" stroke-width="4"/><line x1="600" y1="500" x2="900" y2="500" stroke="#000" stroke-width="4"/>
            <line x1="600" y1="1000" x2="900" y2="1000" stroke="#000" stroke-width="4"/><line x1="600" y1="1100" x2="900" y2="1100" stroke="#000" stroke-width="4"/><line x1="600" y1="1200" x2="900" y2="1200" stroke="#000" stroke-width="4"/><line x1="600" y1="1300" x2="900" y2="1300" stroke="#000" stroke-width="4"/><line x1="600" y1="1400" x2="900" y2="1400" stroke="#000" stroke-width="4"/>

            <!-- Colored Entry Tiles and Safe Home Runs -->
            <rect x="600" y="1300" width="100" height="100" fill="#db4437" stroke="#000" stroke-width="4"/>
            <rect x="700" y="900" width="100" height="500" fill="#db4437" stroke="#000" stroke-width="4"/>

            <rect x="100" y="600" width="100" height="100" fill="#0f9d58" stroke="#000" stroke-width="4"/>
            <rect x="100" y="700" width="500" height="100" fill="#0f9d58" stroke="#000" stroke-width="4"/>

            <rect x="800" y="100" width="100" height="100" fill="#f4b400" stroke="#000" stroke-width="4"/>
            <rect x="700" y="100" width="100" height="500" fill="#f4b400" stroke="#000" stroke-width="4"/>

            <rect x="1300" y="800" width="100" height="100" fill="#4285f4" stroke="#000" stroke-width="4"/>
            <rect x="900" y="700" width="500" height="100" fill="#4285f4" stroke="#000" stroke-width="4"/>

            <!-- Center Triangle Sections -->
            <polygon points="600,600 750,750 600,900" fill="#0f9d58" stroke="#000" stroke-width="4"/>
            <polygon points="600,600 750,750 900,600" fill="#f4b400" stroke="#000" stroke-width="4"/>
            <polygon points="900,600 750,750 900,900" fill="#4285f4" stroke="#000" stroke-width="4"/>
            <polygon points="600,900 750,750 900,900" fill="#db4437" stroke="#000" stroke-width="4"/>
        </svg>

        <!-- Ranking Overlay Badges -->
        <div id="rank-G" class="rank-badge"></div>
        <div id="rank-Y" class="rank-badge"></div>
        <div id="rank-R" class="rank-badge"></div>
        <div id="rank-B" class="rank-badge"></div>
        
        <!-- Pawns -->
        <svg id="R1" class="pawn-svg" viewBox="0 0 100 100" onclick="selectPawn('R1')"><circle cx="50" cy="50" r="42" fill="#db4437" stroke="#ffffff" stroke-width="12"/><text x="50" y="62" font-size="34" font-weight="bold" fill="#ffffff" text-anchor="middle">R1</text></svg>
        <svg id="R2" class="pawn-svg" viewBox="0 0 100 100" onclick="selectPawn('R2')"><circle cx="50" cy="50" r="42" fill="#db4437" stroke="#ffffff" stroke-width="12"/><text x="50" y="62" font-size="34" font-weight="bold" fill="#ffffff" text-anchor="middle">R2</text></svg>
        <svg id="G1" class="pawn-svg" viewBox="0 0 100 100" onclick="selectPawn('G1')"><circle cx="50" cy="50" r="42" fill="#0f9d58" stroke="#ffffff" stroke-width="12"/><text x="50" y="62" font-size="34" font-weight="bold" fill="#ffffff" text-anchor="middle">G1</text></svg>
        <svg id="G2" class="pawn-svg" viewBox="0 0 100 100" onclick="selectPawn('G2')"><circle cx="50" cy="50" r="42" fill="#0f9d58" stroke="#ffffff" stroke-width="12"/><text x="50" y="62" font-size="34" font-weight="bold" fill="#ffffff" text-anchor="middle">G2</text></svg>
        <svg id="Y1" class="pawn-svg" viewBox="0 0 100 100" onclick="selectPawn('Y1')"><circle cx="50" cy="50" r="42" fill="#f4b400" stroke="#ffffff" stroke-width="12"/><text x="50" y="62" font-size="34" font-weight="bold" fill="#000000" text-anchor="middle">Y1</text></svg>
        <svg id="Y2" class="pawn-svg" viewBox="0 0 100 100" onclick="selectPawn('Y2')"><circle cx="50" cy="50" r="42" fill="#f4b400" stroke="#ffffff" stroke-width="12"/><text x="50" y="62" font-size="34" font-weight="bold" fill="#000000" text-anchor="middle">Y2</text></svg>
        <svg id="B1" class="pawn-svg" viewBox="0 0 100 100" onclick="selectPawn('B1')"><circle cx="50" cy="50" r="42" fill="#4285f4" stroke="#ffffff" stroke-width="12"/><text x="50" y="62" font-size="34" font-weight="bold" fill="#ffffff" text-anchor="middle">B1</text></svg>
        <svg id="B2" class="pawn-svg" viewBox="0 0 100 100" onclick="selectPawn('B2')"><circle cx="50" cy="50" r="42" fill="#4285f4" stroke="#ffffff" stroke-width="12"/><text x="50" y="62" font-size="34" font-weight="bold" fill="#ffffff" text-anchor="middle">B2</text></svg>
    </div>

    <div class="controls">
        <div>
            <div class="section-title">1. Select Roll Value:</div>
            <div class="btn-grid">
                <button class="btn-dice" onclick="selectDice(1, this)">1</button>
                <button class="btn-dice" onclick="selectDice(2, this)">2</button>
                <button class="btn-dice" onclick="selectDice(3, this)">3</button>
                <button class="btn-dice" onclick="selectDice(4, this)">4</button>
                <button class="btn-dice" onclick="selectDice(5, this)">5</button>
                <button class="btn-dice" onclick="selectDice(6, this)">6</button>
            </div>
        </div>

        <div>
            <div class="section-title">2. Select Pawn:</div>
            <div class="btn-grid-pawns">
                <button class="btn-pawn btn-pawn-r" onclick="selectPawn('R1', this)">R1</button>
                <button class="btn-pawn btn-pawn-r" onclick="selectPawn('R2', this)">R2</button>
                <button class="btn-pawn btn-pawn-g" onclick="selectPawn('G1', this)">G1</button>
                <button class="btn-pawn btn-pawn-g" onclick="selectPawn('G2', this)">G2</button>
                <button class="btn-pawn btn-pawn-y" onclick="selectPawn('Y1', this)">Y1</button>
                <button class="btn-pawn btn-pawn-y" onclick="selectPawn('Y2', this)">Y2</button>
                <button class="btn-pawn btn-pawn-b" onclick="selectPawn('B1', this)">B1</button>
                <button class="btn-pawn btn-pawn-b" onclick="selectPawn('B2', this)">B2</button>
            </div>
        </div>

        <button class="btn-action" onclick="captureBoard()">📷 Capture Board (Download)</button>

        <div>
            <div class="section-title">Move Log:</div>
            <div id="log" class="log-box"></div>
        </div>
    </div>
</div>

<script>
function getGridPos(col, row) {
    const cellSize = 100 / 15;
    return {
        col: col,
        row: row,
        x: ((col + 0.5) * cellSize).toFixed(2) + '%',
        y: ((row + 0.5) * cellSize).toFixed(2) + '%'
    };
}

const HOME_POSITIONS = {
    'G1': getGridPos(1.5, 1.5), 'G2': getGridPos(3.5, 3.5),
    'Y1': getGridPos(10.5, 1.5), 'Y2': getGridPos(12.5, 3.5),
    'R1': getGridPos(1.5, 10.5), 'R2': getGridPos(3.5, 12.5),
    'B1': getGridPos(10.5, 10.5), 'B2': getGridPos(12.5, 12.5)
};

const MAIN_TRACK_GRID = [
    [6, 13], [6, 12], [6, 11], [6, 10], [6, 9],
    [5, 8], [4, 8], [3, 8], [2, 8], [1, 8], [0, 8], [0, 7], [0, 6],
    [1, 6], [2, 6], [3, 6], [4, 6], [5, 6],
    [6, 5], [6, 4], [6, 3], [6, 2], [6, 1], [6, 0], [7, 0], [8, 0],
    [8, 1], [8, 2], [8, 3], [8, 4], [8, 5],
    [9, 6], [10, 6], [11, 6], [12, 6], [13, 6], [14, 6], [14, 7], [14, 8],
    [13, 8], [12, 8], [11, 8], [10, 8], [9, 8],
    [8, 9], [8, 10], [8, 11], [8, 12], [8, 13], [8, 14], [7, 14], [6, 14]
];

const HOME_PATHS_GRID = {
    'R': [[7, 13], [7, 12], [7, 11], [7, 10], [7, 9], [7, 7]],
    'G': [[1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [7, 7]],
    'Y': [[7, 1], [7, 2], [7, 3], [7, 4], [7, 5], [7, 7]],
    'B': [[13, 7], [12, 7], [11, 7], [10, 7], [9, 7], [7, 7]]
};

const SAFE_START_TILES = [
    [6, 13], [1, 6], [8, 1], [13, 8]
];

function buildFullColorTrack(startOffset, homePathCoords) {
    let track = [];
    for (let i = 0; i < 51; i++) {
        let gridIdx = (startOffset + i) % MAIN_TRACK_GRID.length;
        let coord = MAIN_TRACK_GRID[gridIdx];
        track.push(getGridPos(coord[0], coord[1]));
    }
    homePathCoords.forEach(coord => {
        track.push(getGridPos(coord[0], coord[1]));
    });
    return track;
}

const COLOR_TRACKS = {
    'R': buildFullColorTrack(0, HOME_PATHS_GRID['R']),
    'G': buildFullColorTrack(13, HOME_PATHS_GRID['G']),
    'Y': buildFullColorTrack(26, HOME_PATHS_GRID['Y']),
    'B': buildFullColorTrack(39, HOME_PATHS_GRID['B'])
};

let pawnStates = {
    'R1': -1, 'R2': -1, 'G1': -1, 'G2': -1,
    'Y1': -1, 'Y2': -1, 'B1': -1, 'B2': -1
};

let rankingOrder = [];
let rankSuffixes = ["1st", "2nd", "3rd", "4th"];

let selectedDice = null;
let selectedPawn = null;
let isAnimating = false;

function logMsg(msg) {
    const logBox = document.getElementById('log');
    if (logBox) {
        logBox.innerHTML = `> ${msg}<br>` + logBox.innerHTML;
    }
}

function setPawnPos(pawnId, pos) {
    const el = document.getElementById(pawnId);
    if (el) {
        let pNum = pawnId[1];
        let tileIdx = pawnStates[pawnId];
        let offsetX = (pNum === '2' && tileIdx !== -1) ? 'calc(' + pos.x + ' + 0.8%)' : pos.x;
        el.style.left = offsetX;
        el.style.top = pos.y;
    }
}

function resetBoardPositions() {
    Object.keys(HOME_POSITIONS).forEach(pawnId => {
        setPawnPos(pawnId, HOME_POSITIONS[pawnId]);
    });
}

function selectDice(val, btnElement) {
    if (isAnimating) return;
    selectedDice = val;
    document.querySelectorAll('.btn-dice').forEach(btn => btn.classList.remove('active'));
    if (btnElement) btnElement.classList.add('active');
    logMsg(`Selected Roll: ${val}`);
    
    if (selectedPawn) {
        triggerAutoMove();
    }
}

function selectPawn(pawnId, btnElement) {
    if (isAnimating) return;
    selectedPawn = pawnId;
    document.querySelectorAll('.pawn-svg').forEach(p => p.classList.remove('selected'));
    document.querySelectorAll('.btn-pawn').forEach(btn => btn.classList.remove('active'));

    const activePawnEl = document.getElementById(pawnId);
    if (activePawnEl) activePawnEl.classList.add('selected');

    if (!btnElement) {
        btnElement = Array.from(document.querySelectorAll('.btn-pawn')).find(b => b.innerText.trim() === pawnId);
    }
    if (btnElement) btnElement.classList.add('active');

    logMsg(`Selected Pawn: ${pawnId}`);

    if (selectedDice) {
        triggerAutoMove();
    }
}

async function animatePawnStepByStep(pawnId, colorTrack, fromIdx, steps) {
    isAnimating = true;

    for (let i = 1; i <= steps; i++) {
        let currentStepIdx = fromIdx + i;
        let nextPos = colorTrack[currentStepIdx];
        
        setPawnPos(pawnId, nextPos);
        await new Promise(resolve => setTimeout(resolve, 220));
    }
    
    isAnimating = false;
}

async function triggerAutoMove() {
    if (isAnimating || !selectedDice || !selectedPawn) return;

    const currentPawn = selectedPawn;
    const currentRoll = selectedDice;
    
    selectedDice = null;
    document.querySelectorAll('.btn-dice').forEach(btn => btn.classList.remove('active'));

    const color = currentPawn[0];
    const colorTrack = COLOR_TRACKS[color];
    let currentTrackIdx = pawnStates[currentPawn];

    if (currentTrackIdx === -1) {
        if (currentRoll === 6) {
            pawnStates[currentPawn] = 0;
            setPawnPos(currentPawn, colorTrack[0]);
            logMsg(`✨ ${currentPawn} rolled a 6 and entered the board!`);
            checkCaptures(currentPawn, color, 0);
        } else {
            logMsg(`⚠️ ${currentPawn} is in Home. Must roll a 6 to enter!`);
        }
    } else {
        let targetIdx = currentTrackIdx + currentRoll;
        
        if (targetIdx >= colorTrack.length) {
            logMsg(`⚠️ ${currentPawn} needs an exact roll to enter Home Center!`);
            return;
        }

        pawnStates[currentPawn] = targetIdx;
        logMsg(`${currentPawn} moving ${currentRoll} steps...`);
        
        await animatePawnStepByStep(currentPawn, colorTrack, currentTrackIdx, currentRoll);
        
        if (targetIdx === colorTrack.length - 1) {
            logMsg(`🏆 ${currentPawn} reached Home Center!`);
            checkPlayerCompletion(color);
        } else {
            checkCaptures(currentPawn, color, targetIdx);
        }
    }
}

function checkPlayerCompletion(color) {
    const pawn1 = color + '1';
    const pawn2 = color + '2';
    const colorTrackLength = COLOR_TRACKS[color].length;

    if (pawnStates[pawn1] === colorTrackLength - 1 && pawnStates[pawn2] === colorTrackLength - 1) {
        if (!rankingOrder.includes(color)) {
            rankingOrder.push(color);
            let rankIndex = rankingOrder.length - 1;
            let rankText = rankSuffixes[rankIndex];

            const rankBadge = document.getElementById(`rank-${color}`);
            if (rankBadge) {
                rankBadge.innerText = rankText;
                rankBadge.style.display = 'flex';
            }

            logMsg(`🎉 COLOR ${color} HAS FINISHED BOTH PAWNS AND GAINED ${rankText} PLACE!`);
        }
    }
}

function checkCaptures(activePawn, activeColor, activeTrackIdx) {
    if (activeTrackIdx >= 51) return;

    const activePos = COLOR_TRACKS[activeColor][activeTrackIdx];
    const isSafeTile = SAFE_START_TILES.some(
        tile => tile[0] === activePos.col && tile[1] === activePos.row
    );

    if (isSafeTile) {
        logMsg(`🛡️ ${activePawn} landed on a safe start box. Safe from captures!`);
        return;
    }

    Object.keys(pawnStates).forEach(otherPawn => {
        const otherColor = otherPawn[0];
        const otherTrackIdx = pawnStates[otherPawn];
        
        if (otherPawn !== activePawn && otherColor !== activeColor && otherTrackIdx >= 0 && otherTrackIdx < 51) {
            const otherPos = COLOR_TRACKS[otherColor][otherTrackIdx];
            
            if (activePos.col === otherPos.col && activePos.row === otherPos.row) {
                pawnStates[otherPawn] = -1;
                setPawnPos(otherPawn, HOME_POSITIONS[otherPawn]);
                logMsg(`💥 ${activePawn} captured ${otherPawn}! ${otherPawn} sent Home.`);
            }
        }
    });
}

function captureBoard() {
    const wrapper = document.getElementById('board-wrapper');
    
    html2canvas(wrapper).then(canvas => {
        const link = document.createElement('a');
        link.download = `ludo-board-${Date.now()}.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();
        logMsg("📷 Board screenshot downloaded!");
    });
}

window.addEventListener('DOMContentLoaded', () => {
    resetBoardPositions();
});
</script>

</body>
</html>
"""

st.title("🎲 Manual Ludo Game")

# Render embedded HTML component with responsive scrolling disabled
components.html(LUDO_HTML_CODE, height=850, scrolling=True)