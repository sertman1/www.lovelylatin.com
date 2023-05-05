import { useState } from "react";
import { TextField, Button, Container } from "@material-ui/core"

function App() {
  const [userInput, setUserInput] = useState("")



  return (
      <Container>
        <h1>The Lovely Latin Language</h1>
        <TextField fullWidth label="Enter your Latin text here" id="fullWidth" margin="normal"/>
        <Button variant="contained">Go!</Button>
      </Container>
  );

}

export default App;
