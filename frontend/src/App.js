import { useState } from "react"
import axios from "axios"
import { TextField, Button, Container, Box, Grid } from "@material-ui/core"
import { Stack} from "@mui/material";
import Header from "./components/Header.js"
import Footer from "./components/Footer.js"
import RetrievedText from "./components/RetreivedText.js";

const API = "http://localhost:5757"

function App() {
  const [userInput, setUserInput] = useState("")
  const [output, setOutput] = useState("")
  const [hasEntered, setHasEntered] = useState(false)
  const [authorsSelected, setAuthorsSelected] = useState([])
  const [retrievedTexts, setRetrievedTexts] = useState([])
  const [docsRetrieved, setDocsRetrieved] = useState(false)

  const resetValues = () => {
    setHasEntered(false); 
    setUserInput(""); 
    setOutput("");
    setDocsRetrieved(false)
    setRetrievedTexts([])
  }

  const process_data = (data) => {
    let rank = 0
    let ranks = []

    let name_of_work = ""
    let count = 0
    for (let i = 0; i < data.length; i++) {
      if (data[i] !== "\n") { // backend returns works separated by newlines
        name_of_work += data[i]
      } else {
        let url = ""
        while (i < data.length && data[i] !== "\n") {
          url += data[i]
          i += 1
        }
        url.trim()
        if (name_of_work.trim() !== "") {
          ranks[rank] = name_of_work.trim() + url
          name_of_work = ""
          rank += 1
        }
      }
    }
    return ranks
  }

  const enter = async () => {
    if (authorsSelected.length === 0) {
      alert('Please select an author!')
      return
    }
    else if (userInput === "") {
      alert('Please enter text!')
      return
    }
    setHasEntered(true)
    let output = "Processing results, please be patient"
    if (authorsSelected.length === 0) {
      output += " (full corpus searches take much, much longer...)"
    }

    setOutput(output)
    try {
      const response = await axios.get(`${API}/output`, 
      {   params: {
            userInput: userInput, 
            authorsSelected: authorsSelected
        } 
      })

      const data = process_data(response.data)

      setRetrievedTexts(
        [
          ...data
        ]
      )

      setDocsRetrieved(true)
      
    } catch (err) {
      alert('Eheu! All apologies, our sever is down...')
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

  const showRetrievedTexts = () => {
    if (!docsRetrieved) {
      return (<Container maxWidth={false}>
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
            borderColor: 'grey.800',
          }}>
          {output}
        </Box>
      </Container>)
    }
    
    if (retrievedTexts.length === 0) {
      return (<Container maxWidth={false}>
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
            borderColor: 'grey.800',
          }}>
          {"Unfortunately, no appropriate documents were found"}
        </Box>
      </Container>);
    }
 
    return (
    <Container maxWidth={false}>
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
          borderColor: 'grey.800',
        }}>
        <Grid>
          {retrievedTexts.map((text, index) => {
            if (text !== "The Latin Library")
              return (
                <RetrievedText rank={index + 1} text={text}></RetrievedText>
              )
          })}
        </Grid>
      </Box>
    </Container>)
  }

  const showOptions = () => {
    if (hasEntered) {
      return (
        <div>
          <Grid
          container
          >
            {showRetrievedTexts()}
          </Grid>
          <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
        >
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

      <Stack spacing={2}>
          <Header authorsSelected={authorsSelected} setAuthorsSelected={setAuthorsSelected} hasEntered={hasEntered}></Header>
            {showOptions()}
          <Footer/>
        </Stack>
    </Container>
  );

}

export default App;
