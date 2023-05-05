import { useState } from "react"
import axios from "axios"
import { TextField, Button, Container } from "@material-ui/core"

const API = "https://lovelylatin.herokuapp.com/"

function App() {
  const [userInput, setUserInput] = useState("")

  const enter = async (e) => {
    e.preventDefault()
    try {
      const response = await axios.get(`${API}`)
      const data = response.data
      alert(data)
    } catch (err) {
      console.log(err)
    }
    return
  }

  const keyPress = (e) => {
    if (e.keyCode == 13) {
      enter()
    }
  }

  return (
      <Container>
        <h1>The Lovely Latin Language</h1>
        <TextField fullWidth label="Enter your Latin text here" 
          id="fullWidth" 
          margin="normal"
          onKeyDown={keyPress}
          onChange={(e) => setUserInput(e.target.value)}
        />
        <Button variant="contained" onClick={enter}>
          Go!
        </Button>
      </Container>
  );

}

export default App;
