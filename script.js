document.getElementById("solve-button").addEventListener("click", function() {
    const table = [];
    for (let row = 0; row < 9; row++) {
        const rowValues = [];
        for (let col = 0; col < 9; col++) {
            const cellValue = document.getElementById(`cell-${row}-${col}`).value;
            rowValues.push(cellValue === "" ? 0 : parseInt(cellValue));
        }
        table.push(rowValues);
    }
    console.log("Sending the following Sudoku to the server:");
    console.log(table);
    fetch(`http://localhost:5000/solve/123`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({table}),
    })
        .then(response => response.json())
        .then(data => {
            const solved = data.solved;
            if (solved && solved.length > 0) {
                for (let row = 0; row < 9; row++) {
                    for (let col = 0; col < 9; col++) {
                        document.getElementById(`cell-${row}-${col}`).value = solved[row][col];
                    }
                }
            } else {
                alert("Sudoku couldn't be solved.");
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});