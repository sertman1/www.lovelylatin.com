import { useState } from "react"
import axios from "axios"
import { TextField, Button, Container, Box } from "@material-ui/core"
import Header from "./components/Header.js"
import Footer from "./components/Footer.js"

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

    try {
      const response = await axios.get(`${API}/output`, { params: {userInput} })
      const data = response.data
      console.log(data)
      setOutput(data)
    } catch (err) {
      alert('err')
      console.log(err)
    }

    setHasEntered(true)
    return
  }

  const keyPress = (e) => {
    if (e.keyCode === 13) {
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
            mb: 1,
            bgcolor: 'white',
            color: 'grey.300',
            border: '1px solid',
            borderColor:'grey.800',
          }}>
            {output}
          </Box>
          <div>
            <Button variant="contained" onClick={() => {setHasEntered(false); setUserInput("")} }>
              Enter more text
            </Button>
          </div>
        </div>
      );
    } else {
      return (
        <div>
          <TextField fullWidth label="Enter your Latin text or keywords here (e.g., Pythagoras faba)"
            id="fullWidth"
            margin="normal"
            onKeyDown={keyPress}
            onChange={(e) => setUserInput(e.target.value)}
            multiline={true}
          />
          <Button variant="contained" onClick={enter}>
            Go!
          </Button>
        </div>
      );
    }
  }

  return (
    <Container style={{ background: '#e1bee7' }} maxWidth={false}>

      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',

        }}
      >
        <h1>The Lovely Latin Language</h1>
      </div>

      {showOptions()}

      <Footer></Footer>

    </Container>
  );

}

export default App;
