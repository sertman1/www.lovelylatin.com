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
  const [authorsSelected, setAuthorsSelected] = useState([])

  const resetValues = () => {
    setHasEntered(false); 
    setUserInput(""); 
    setOutput("");
  }

  const enter = async () => {
    if (userInput === "") {
      alert('please enter text!')
      return
    }
    setHasEntered(true)
    let output = "Processing results, please be patient"
    if (authorsSelected.length === 0) {
      output += " (full corpus searches take much longer...)"
    }

    setOutput(output)
    try {
      const response = await axios.get(`${API}/output`, 
      {   params: {
            userInput: userInput, 
            authorsSelected: authorsSelected
        } 
      })
      const data = response.data
      setOutput(data)
    } catch (err) {
      alert('err')
      console.log(err)
    }
    return
  }

  const handelOnChange = (e) => {
    if (e.key !== 'Enter') {
      setUserInput(e.target.value)
    } 
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
            <Button variant="contained" onClick={() => {resetValues()} }>
              Enter more text
            </Button>
          </div>
        </div>
      );
    } else {
      return (
        <div>
          <TextField fullWidth label="Enter your Latin text or keywords (e.g. faba pythagoras)"
            id="fullWidth"
            margin="normal"
            onChange={handelOnChange}
            onKeyDown={keyPress}
            multiline={true}
            size="medium"
          />
          <div
            style={{
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',

            }}
          >

            <Button variant="contained" onClick={enter} size="medium">
              Go!
            </Button>

          </div>
        </div>
      );
    }
  }

  return (
    <Container style={{ background: '#e1bee7' }} maxWidth={false}>

        <Header authorsSelected={authorsSelected} setAuthorsSelected={setAuthorsSelected} hasEntered={hasEntered}></Header>
      <div style={{ height: "25vh" }}>
          {showOptions()}
        </div>

        <Footer></Footer>

    </Container>
  );

}

export default App;
