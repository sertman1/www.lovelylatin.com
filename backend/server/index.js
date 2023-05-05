const express = require("express");
const cors = require('cors')
const app = express();
app.use(cors())

const port = process.env.PORT || 5000;

app.get("/", (req, res) => {
  res.send("Lovely Latin!");
});

app.get("/output", (req, res) => {
  const { query } = req.query
  res.json({ query })
});

app.listen(port, () => {
  console.log(`Express app listening at port: http://localhost:${port}/`);
});

