const games = [
    { name: "Game A", odds: "1 in 10", description: "Skill-based game with high engagement." },
    { name: "Game B", odds: "1 in 5", description: "Luck-based game with random outcomes." },
];

const gameList = document.getElementById('gameList');

games.forEach(game => {
    const listItem = document.createElement('li');
    listItem.innerHTML = `<strong>${game.name}</strong>: Odds - ${game.odds}. ${game.description}`;
    gameList.appendChild(listItem);
});
