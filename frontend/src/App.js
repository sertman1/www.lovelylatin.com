import { useState } from "react"
import axios from "axios"
import { TextField, Button, Container, Box } from "@material-ui/core"

const API = "http://localhost:5000"

function App() {
  const [userInput, setUserInput] = useState("")
  const [output, setOutput] = useState("")
  const [hasEntered, setHasEntered] = useState(false)

  const enter = async () => {
    if (userInput === "") {
      alert('please enter text!')
      return
    }

    setHasEntered(true)

    try {
      const response = await axios.get(`${API}/output`, { params: {userInput} })
      const data = response.data
      setOutput(data)
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

  const showOptions = () => {
    if (hasEntered) {
      return (
        <div>
          <Box 
          component="span" 
          sx={{ 
            whiteSpace: 'normal',
            display: 'block',
            p: 1,
            m: 1,
            bgcolor: 'white',
            color: 'grey.300',
            border: '1px solid',
            borderColor:'grey.800',
          }}>
            {output}
          </Box>
          <Button variant="contained" onClick={() => {setHasEntered(false); setUserInput("")} }>
            Enter more text
          </Button>
        </div>
      );
    } else {
      return (
        <div>
          <TextField fullWidth label="Enter your Latin text here"
            id="fullWidth"
            margin="normal"
            onKeyDown={keyPress}
            onChange={(e) => setUserInput(e.target.value)}
          />
          <Button variant="contained" onClick={enter}>
            Go!
          </Button>
        </div>
      );
    }
  }

  return (
      <Container>
        <h1>The Lovely Latin Language</h1>
        {showOptions()}
      </Container>
  );

}

export default App;
