
const words = new Set();
let score = 0;
let timer = 60;
const $gameOver = $('#game-over');
let intervalID = setInterval(runTimer, 1000);

$('#score').append('Score: 0');

/* remove abilty to submit new words, clear previous in game messages and running score, dsplay gameover message */  
function gameOver() {
    $('form').remove();
    $(".msg").empty();
    $('#score').empty();
    $gameOver.text(`Game Over!`)

    updateServer(score);
}

/* create a countdown timer for the game, append countdown to the HTML, and run gamover function when the timer ends */
function runTimer() {
    if (timer > 0) {
        timer -= 1;
    }
    else if (timer === 0) {
        clearInterval(intervalID);
        gameOver();
    }
    $('#timer').text(timer)
}

/** update displayed score */
function updateScore(word) {
    $('#score').empty();
    val = word.length;
    score += val;
    $('#score').append(`Score: ${score}`)
    
} 

$('form').on('submit', handleSubmit);
/* handle form submit, send request to server and check validity of the user submited word and display message based on request response, start game timer on submit */
async function handleSubmit(evt) {
    evt.preventDefault();

    $('.msg').empty();

    const $word = $('#word');
    let word = $word.val();
    if (!word) return

    const res = await axios.get('/check-word', { params: { word: word } });
   
    if (res.data.result === 'not-on-board') {
        $('.msg').append(`"${word}" is not on the board!`)
    }

    else if (res.data.result === 'not-word') {
        $('.msg').append(`"${word}" is not a valid word!`) 
    }
        
    else if (words.has(word)) {
			$(".msg").append(`${word} has alredy been used.`);
    }
    
    else {
			$(".msg").append(`"${word}" is a valid word and is on the board!`);
			words.add(word);
			updateScore(word);
		}

    $word.val('');
}

/* send request to update server with the final score, handle respose and show message with the updated server info */
async function updateServer(score) {
    const resp = await axios.post("/update-score-plays", { score: score });
    console.log(resp)
    if (resp.data.brokeRecord) {
        showMessage(`New record: ${score}`, "ok");
    } else {
        showMessage(`Final score: ${score}`, "ok");
    }
}

/** display message */
function showMessage(msg) {
    $(".msg").append(msg)
}
