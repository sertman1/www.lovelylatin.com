import * as React from 'react';
import Box from '@mui/material/Box';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Chip from '@mui/material/Chip';
import CloseIcon from '@mui/icons-material/Close';
import { Button } from '@material-ui/core';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

const names = [
  'Ammianus',
  'Apuleius',
  'Augustus',
  'Aurelius Victor',
  'Caesar',
  'Cato',
  'Catullus',
  'Cicero',
  'Catullus',
]

function Header(props) {
  const [personName, setPersonName] = React.useState([]);

  const handleChange = (e) => {
    const {
      target: { value },
    } = e;
    setPersonName(
      // On autofill we get a stringified value.
      typeof value === 'string' ? value.split(',') : value,
    );
  };

  const handleDelete = (e, value) => {
    e.preventDefault()
    setPersonName(personName.filter((name) => name !== value));
  }

  const handleReset = () => {
    setPersonName([])
  }

  const getAuthorForm = () => {
    return (
      <div>
        <FormControl fullWidth={true}>
          <InputLabel id="authors-label" size="small">Your Latin authors here</InputLabel>
          <Select
            
            labelId="authors-label"
            id="authors"
            multiple
            value={personName}
            onChange={handleChange}
            input={<OutlinedInput id="select-multiple-chip" label="Your Latin authors here"/>}
            renderValue={(selected) => (
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                {selected.map((value) => (
                  <Chip
                    key={value}
                    label={value}
                    clickable
                    deleteIcon={
                      <CloseIcon onMouseDown={(e) => e.stopPropagation()}></CloseIcon>
                    }
                    onDelete={(e) => handleDelete(e, value)}
                  />
                ))}
              </Box>
            )}
            MenuProps={MenuProps}
          >
            {names.map((name) => (
              <MenuItem
                key={name}
                value={name}
              >
                {name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </div>
    )
  }

  return (
    <div>

      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',

        }}
      >
        <h1>Traverse the Lovely Latin Catalogue</h1>
      </div>

      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',

        }}
      >

        <p>Search the works of dozens of Latin authors or explore the Great Beyonds...</p>

      </div>

      {getAuthorForm()}

      <Button variant="contained" size="small" onClick={handleReset}>
        Reset
      </Button>

    </div>
  )
}

export default Header;