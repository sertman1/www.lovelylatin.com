const express = require("express");
const cors = require('cors')
const app = express();
app.use(cors())

const port = process.env.PORT || 5000;

async function process_text(req,res) {
  const { userInput } = req.query

  try {
    var spawn = require("child_process").spawn;

    var executor = spawn('python', ["./latin_processor.py",
      userInput]);

    executor.stdout.on('data', (data) => {
      res.send(data)
    });

    executor.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
    });

    executor.on('close', (code) => {
      console.log(`child process exited with code ${code}`)
    });

  } catch (err) {
    console.log(err)
  }
}

app.get("/", (req, res) => {
  res.send("Lovely Latin!");
});

app.get("/output", (req,res) => {
  process_text(req,res)
});

app.listen(port, () => {
  console.log(`Express app listening at port: http://localhost:${port}/`);
});

