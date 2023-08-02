/* eslint-disable @typescript-eslint/no-var-requires */
const express = require("express");
const { google } = require("googleapis");
const { getTeamFromPlayerTag } = require("../../dist/commons/functions/utils");
const {
	addLinesInSheet,
	getPlayers,
	clearPlayersLines,
} = require("../../dist/commons/functions/googlespreadsheet-operations");

const router = express.Router();

// const { request, name } = req.body;
// const getLines = await getDataInSheetArea(googleSheets, auth);
// const playersInSheet = transformTwoDimensionalArrayToListOfPlayers(getLines.data.values);
// console.log(playersInSheet);
router.post("/", async (_req, res) => {
	const { googleSheets, auth } = await prepareCredentials();
	await clearPlayersLines(googleSheets, auth);

	const playersInFile = getPlayers();
	console.log("playersInFile------------------------------------");
	console.log(playersInFile);

	const playerToAdd = [];
	playersInFile.forEach((player) => {
		const columnsData = [
			player.tag,
			player.expLevel,
			player.name,
			player.trophies,
			`=HIPERLINK("https://brawlstats.com/profile/${player.tag.substring(
				1,
			)}"; "${player.tag}")`,
			player["3vs3Victories"],
			player.highestTrophies,
			player.isQualifiedFromChampionshipChallenge,
			getTeamFromPlayerTag(player.tag),
		];
		playerToAdd.push(columnsData);
	});

	console.log("playerToAdd---------------------------------------");
	console.log(playerToAdd);

	setTimeout(() => {
		addLinesInSheet(googleSheets, auth, playerToAdd);
	}, 5000);

	res.send("Data has been updated! Thank you!");
});

async function prepareCredentials() {
	const auth = new google.auth.GoogleAuth({
		keyFile: "src/commons/files/credentials.json",
		scopes: "https://www.googleapis.com/auth/spreadsheets",
	});
	const client = await auth.getClient();
	const googleSheets = google.sheets({ version: "v4", auth: client });
	return { googleSheets, auth };
}

module.exports = router;
