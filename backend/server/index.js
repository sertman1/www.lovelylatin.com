const express = require("express");
const app = express();
const port = process.env.PORT || 5000;

app.get("/", (req, res) => {
  res.send("Lovely Latin!");
});

app.get("/output", (req, res) => {
  res.send("here is your output...");
})

app.listen(port, () => {
  console.log(`Express app listening at port: http://localhost:${port}/`);
});