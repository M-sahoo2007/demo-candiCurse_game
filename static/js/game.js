const candyTypes = ['candy-0', 'candy-1', 'candy-2', 'candy-3', 'candy-4', 'candy-5'];
const specialTypes = ['bomb', 'rainbow', 'line', 'color'];
const gridSize = 8;
const totalCells = gridSize * gridSize;

let board, scoreValue, levelValue, movesLeftValue, timerValue;
let lifetimeScoreValue, bestScoreValue, leaderboardRankValue;
let pauseButton, restartButton, resumeButton, pauseModal, toggleSound;
let gameArray = [];
let dragSrc = null;
let selectedIndex = null;
let invalidSwapIndices = [];
let score = 0;
let level = 1;
let movesLeft = 30;
let timerSeconds = 120;
let paused = false;
let soundEnabled = true;
let timerInterval;
let saveInProgress = false;
let storageKey = null;

const createCandy = () => {
    const type = candyTypes[Math.floor(Math.random() * candyTypes.length)];
    return { type, special: null };
};

const createSound = (frequency, duration = 0.12, type = 'sine') => {
    const context = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = context.createOscillator();
    const gain = context.createGain();
    oscillator.type = type;
    oscillator.frequency.value = frequency;
    oscillator.connect(gain);
    gain.connect(context.destination);
    gain.gain.value = 0.08;
    oscillator.start();
    oscillator.stop(context.currentTime + duration);
};

const playSoundEffect = (frequency, type = 'sine') => {
    if (!soundEnabled || !window.AudioContext) return;
    createSound(frequency, 0.12, type);
};

const getShowToast = () => {
    return typeof window.showToast === 'function' ? window.showToast : (message) => {
        const toast = document.getElementById('toastMessage');
        if (!toast) return;
        toast.textContent = message;
        toast.classList.remove('hidden');
        setTimeout(() => toast.classList.add('hidden'), 2600);
    };
};

const renderBoard = () => {
    if (!board) return;
    board.innerHTML = '';
    const specialIcons = {
        bomb: '💣',
        rainbow: '🌈',
        line: '➖',
        color: '✨',
    };

    gameArray.forEach((candy, index) => {
        const card = document.createElement('div');
        card.className = `board-card ${candy.special || candy.type}`;
        card.setAttribute('draggable', true);
        card.dataset.index = index;
        card.innerHTML = candy.special ? `<span class="special-label">${specialIcons[candy.special] || candy.special}</span>` : '';
        board.appendChild(card);

        if (index === selectedIndex) {
            card.classList.add('selected');
        }
        if (invalidSwapIndices.includes(index)) {
            card.classList.add('invalid-swap');
        }

        card.addEventListener('click', handleCardClick);
        card.addEventListener('dragstart', dragStart);
        card.addEventListener('dragover', dragOver);
        card.addEventListener('drop', dragDrop);
        card.addEventListener('dragend', dragEnd);
        card.addEventListener('touchstart', touchStart, { passive: false });
        card.addEventListener('touchmove', touchMove, { passive: false });
        card.addEventListener('touchend', touchEnd, { passive: false });
    });
};

const dragStart = (event) => {
    const card = event.target.closest('.board-card');
    if (!card) return;
    dragSrc = card;
    selectedIndex = parseInt(card.dataset.index, 10);
    renderBoard();
};

const dragOver = (event) => {
    event.preventDefault();
};

const dragDrop = (event) => {
    event.preventDefault();
    const cardTarget = event.target.closest('.board-card');
    if (!dragSrc || !cardTarget) return;
    const srcIndex = parseInt(dragSrc.dataset.index, 10);
    const targetIndex = parseInt(cardTarget.dataset.index, 10);
    swapCandies(srcIndex, targetIndex);
};

const dragEnd = () => {
    dragSrc = null;
};

const clearSelection = () => {
    selectedIndex = null;
};

const setInvalidSwap = (srcIndex, targetIndex) => {
    invalidSwapIndices = [srcIndex, targetIndex];
    renderBoard();
    setTimeout(() => {
        invalidSwapIndices = [];
        renderBoard();
    }, 360);
};

const handleCardClick = (event) => {
    if (paused) return;
    const card = event.currentTarget.closest('.board-card');
    if (!card) return;

    const index = parseInt(card.dataset.index, 10);
    if (!Number.isFinite(index)) return;

    if (selectedIndex === null) {
        selectedIndex = index;
        renderBoard();
        return;
    }

    if (selectedIndex === index) {
        clearSelection();
        renderBoard();
        return;
    }

    if (isNeighbor(selectedIndex, index)) {
        swapCandies(selectedIndex, index);
        clearSelection();
    } else {
        const toast = getShowToast();
        toast('Select a neighboring candy to swap.');
        selectedIndex = index;
    }
    renderBoard();
};

let touchSource = null;
const touchStart = (event) => {
    event.preventDefault();
    touchSource = event.currentTarget;
};

const touchMove = (event) => {
    event.preventDefault();
};

const touchEnd = (event) => {
    event.preventDefault();
    if (!touchSource) return;
    const touch = event.changedTouches[0];
    const target = document.elementFromPoint(touch.clientX, touch.clientY);
    const cardTarget = target?.closest('.board-card');
    if (cardTarget && cardTarget.dataset.index) {
        const srcIndex = parseInt(touchSource.dataset.index, 10);
        const targetIndex = parseInt(cardTarget.dataset.index, 10);
        swapCandies(srcIndex, targetIndex);
    }
    touchSource = null;
};

const swapCandies = (srcIndex, targetIndex) => {
    if (paused) return;
    if (!isNeighbor(srcIndex, targetIndex)) {
        setInvalidSwap(srcIndex, targetIndex);
        return;
    }

    [gameArray[srcIndex], gameArray[targetIndex]] = [gameArray[targetIndex], gameArray[srcIndex]];
    if (hasMatch()) {
        movesLeft -= 1;
        playSoundEffect(600, 'triangle');
        updateStats();
        resolveBoard();
    } else {
        [gameArray[srcIndex], gameArray[targetIndex]] = [gameArray[targetIndex], gameArray[srcIndex]];
        playSoundEffect(280, 'square');
        const toast = getShowToast();
        toast('No match! Try a different swap.');
        setInvalidSwap(srcIndex, targetIndex);
    }
};

const isNeighbor = (src, target) => {
    const row1 = Math.floor(src / gridSize);
    const col1 = src % gridSize;
    const row2 = Math.floor(target / gridSize);
    const col2 = target % gridSize;
    return Math.abs(row1 - row2) + Math.abs(col1 - col2) === 1;
};

const hasMatch = () => {
    return detectMatches().length > 0;
};

const detectMatches = () => {
    const matches = [];
    for (let row = 0; row < gridSize; row++) {
        let currentStretch = [row * gridSize];
        for (let col = 1; col < gridSize; col++) {
            const index = row * gridSize + col;
            const prevIndex = row * gridSize + col - 1;
            if (gameArray[index].type === gameArray[prevIndex].type) {
                currentStretch.push(index);
            } else {
                if (currentStretch.length >= 3) matches.push([...currentStretch]);
                currentStretch = [index];
            }
        }
        if (currentStretch.length >= 3) matches.push([...currentStretch]);
    }
    for (let col = 0; col < gridSize; col++) {
        let currentStretch = [col];
        for (let row = 1; row < gridSize; row++) {
            const index = row * gridSize + col;
            const prevIndex = (row - 1) * gridSize + col;
            if (gameArray[index].type === gameArray[prevIndex].type) {
                currentStretch.push(index);
            } else {
                if (currentStretch.length >= 3) matches.push([...currentStretch]);
                currentStretch = [index];
            }
        }
        if (currentStretch.length >= 3) matches.push([...currentStretch]);
    }
    return matches;
};

const resolveBoard = () => {
    const matches = detectMatches();
    if (!matches.length) {
        renderBoard();
        return;
    }

    const uniqueMatches = [...new Set(matches.flat())];
    const matchValue = uniqueMatches.length * 50;
    score += matchValue;
    updateStats();
    const specialIndices = createSpecialsFromMatches(matches);

    uniqueMatches.forEach((index) => {
        if (!specialIndices.has(index)) {
            gameArray[index] = { type: null, special: null };
        }
    });

    setTimeout(() => {
        collapseCandies();
        refillBoard();
        renderBoard();
        if (detectMatches().length) {
            score += uniqueMatches.length * 10;
            resolveBoard();
        }
    }, 250);
};

const createSpecialsFromMatches = (matches) => {
    const specialIndices = new Set();
    matches.forEach((match) => {
        if (match.length >= 4) {
            const specialIndex = match[Math.floor(match.length / 2)];
            const candyType = gameArray[specialIndex]?.type || createCandy().type;
            gameArray[specialIndex] = {
                type: candyType,
                special: specialTypes[Math.floor(Math.random() * specialTypes.length)],
            };
            specialIndices.add(specialIndex);
        }
    });

    return specialIndices;
};

const collapseCandies = () => {
    for (let col = 0; col < gridSize; col++) {
        let emptySpaces = 0;
        for (let row = gridSize - 1; row >= 0; row--) {
            const index = row * gridSize + col;
            if (!gameArray[index].type) {
                emptySpaces++;
            } else if (emptySpaces) {
                gameArray[(row + emptySpaces) * gridSize + col] = gameArray[index];
                gameArray[index] = { type: null, special: null };
            }
        }
        for (let row = 0; row < emptySpaces; row++) {
            gameArray[row * gridSize + col] = createCandy();
        }
    }
};

const refillBoard = () => {
    gameArray = gameArray.map((candy) => candy.type ? candy : createCandy());
};

const updateStats = () => {
    if (scoreValue) scoreValue.textContent = score;
    if (levelValue) levelValue.textContent = level;
    if (movesLeftValue) movesLeftValue.textContent = movesLeft;
    if (timerValue) {
        const minutes = String(Math.floor(timerSeconds / 60)).padStart(2, '0');
        const seconds = String(timerSeconds % 60).padStart(2, '0');
        timerValue.textContent = `${minutes}:${seconds}`;
    }
    if (movesLeft <= 0 || timerSeconds <= 0) {
        void endGame(false);
    }
    saveGameState();
};

const updateSavedStats = ({ total_score, best_score, rank } = {}) => {
    if (lifetimeScoreValue && typeof total_score !== 'undefined') {
        lifetimeScoreValue.textContent = total_score;
    }
    if (bestScoreValue && typeof best_score !== 'undefined') {
        bestScoreValue.textContent = best_score;
    }
    if (leaderboardRankValue) {
        leaderboardRankValue.textContent = typeof rank !== 'undefined' && rank > 0 ? `#${rank}` : leaderboardRankValue.textContent;
    }
};

const getCsrfToken = () => {
    const cookieValue = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='));
    return cookieValue ? cookieValue.split('=')[1] : null;
};

const getStorageKey = () => storageKey || 'candyverse_game_state';

const saveGameState = () => {
    if (!storageKey) return;
    const state = {
        gameArray,
        score,
        level,
        movesLeft,
        timerSeconds,
        selectedIndex,
        invalidSwapIndices,
        paused,
        updatedAt: Date.now(),
    };
    localStorage.setItem(getStorageKey(), JSON.stringify(state));
};

const clearSavedGameState = () => {
    if (!storageKey) return;
    localStorage.removeItem(getStorageKey());
};

const loadSavedGameState = () => {
    if (!storageKey) return false;
    const saved = localStorage.getItem(getStorageKey());
    if (!saved) return false;
    try {
        const state = JSON.parse(saved);
        if (!state || typeof state !== 'object') return false;
        gameArray = Array.isArray(state.gameArray) && state.gameArray.length === totalCells
            ? state.gameArray
            : gameArray;
        score = Number.isFinite(state.score) ? state.score : score;
        level = Number.isFinite(state.level) ? state.level : level;
        movesLeft = Number.isFinite(state.movesLeft) ? state.movesLeft : movesLeft;
        timerSeconds = Number.isFinite(state.timerSeconds) ? state.timerSeconds : timerSeconds;
        selectedIndex = Number.isFinite(state.selectedIndex) ? state.selectedIndex : null;
        invalidSwapIndices = Array.isArray(state.invalidSwapIndices) ? state.invalidSwapIndices : [];
        paused = !!state.paused;
        return true;
    } catch {
        return false;
    }
};

const saveScore = async (scoreToSave, currentLevel) => {
    if (saveInProgress || scoreToSave <= 0) return;
    saveInProgress = true;
    const csrfToken = getCsrfToken();
    if (!csrfToken) {
        console.warn('CSRF token missing; score not saved.');
        saveInProgress = false;
        return;
    }

    try {
        const response = await fetch('/api/save-score/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ score: scoreToSave, level: currentLevel }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => null);
            console.warn('Score save failed', errorData || response.statusText);
            return;
        }

        const data = await response.json();
        updateSavedStats({
            total_score: data.total_score,
            best_score: data.best_score,
            rank: data.rank,
        });
        const toast = getShowToast();
        toast('Score saved! Leaderboard updated.');
    } catch (error) {
        console.error('Could not save score:', error);
    } finally {
        saveInProgress = false;
    }
};

const tickTimer = () => {
    if (paused) return;
    timerSeconds -= 1;
    if (timerSeconds <= 0) {
        timerSeconds = 0;
        endGame(false);
    }
    updateStats();
};

const startTimer = () => {
    clearInterval(timerInterval);
    timerInterval = setInterval(tickTimer, 1000);
};

const endGame = async (won) => {
    paused = true;
    clearInterval(timerInterval);
    const toast = getShowToast();

    if (score > 0) {
        await saveScore(score, level);
    }

    clearSavedGameState();
    toast(won ? 'Level completed! Score saved.' : 'Game over. Try again!');
    if (won) playSoundEffect(900, 'sine');
    else playSoundEffect(220, 'sawtooth');
};

const resetGame = () => {
    score = 0;
    level = 1;
    movesLeft = 30;
    timerSeconds = 120;
    paused = false;

    const generateBoard = () => Array.from({ length: totalCells }, createCandy);
    do {
        gameArray = generateBoard();
    } while (detectMatches().length);

    renderBoard();
    updateStats();
    saveGameState();
    startTimer();
};

const initGame = () => {
    board = document.getElementById('gameBoard');
    scoreValue = document.getElementById('scoreValue');
    levelValue = document.getElementById('levelValue');
    movesLeftValue = document.getElementById('movesLeftValue');
    timerValue = document.getElementById('timerValue');
    lifetimeScoreValue = document.getElementById('lifetimeScoreValue');
    bestScoreValue = document.getElementById('bestScoreValue');
    leaderboardRankValue = document.getElementById('leaderboardRankValue');
    pauseButton = document.getElementById('pauseButton');
    restartButton = document.getElementById('restartButton');
    resumeButton = document.getElementById('resumeButton');
    pauseModal = document.getElementById('pauseModal');
    toggleSound = document.getElementById('toggleSound');
    const gameData = document.getElementById('gameData');
    if (gameData) {
        const username = gameData.dataset.username;
        if (username) {
            storageKey = `candyverse_game_state_${username}`;
        }
    }

    if (!board) {
        console.error('Game board element not found');
        return;
    }

    if (!loadSavedGameState()) {
        resetGame();
    } else {
        renderBoard();
        updateStats();
        if (!paused) {
            startTimer();
        }
    }

    pauseButton?.addEventListener('click', () => {
        paused = true;
        pauseModal?.classList.remove('hidden');
    });

    resumeButton?.addEventListener('click', () => {
        paused = false;
        pauseModal?.classList.add('hidden');
    });

    restartButton?.addEventListener('click', () => {
        pauseModal?.classList.add('hidden');
        resetGame();
    });

    toggleSound?.addEventListener('click', () => {
        soundEnabled = !soundEnabled;
        toggleSound.textContent = soundEnabled ? '🔊' : '🔇';
        getShowToast()(soundEnabled ? 'Sound enabled' : 'Sound muted');
    });

    const leaderboardPopup = document.getElementById('leaderboardPopup');
    if (leaderboardPopup) {
        leaderboardPopup.addEventListener('click', () => {
            getShowToast()('Leaderboard is available on the Leaderboard page.');
        });
    }

    getShowToast()('Welcome to CandyVerse!');
};

const onReady = (callback) => {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', callback);
    } else {
        callback();
    }
};

onReady(initGame);
