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
  'Ammianus', 'Apuleius', 'Augustus', 'Aurelius Victor', 'Caesar', 'Cato', 'Catullus', 'Cicero', 'Claudian', 'Curtius Rufus', 'Ennius', 'Eutropius', 'Florus', 'Frontinus', 'Gellius', 'Historia Augusta', 'Horace', 'Justin', 'Juvenal', 'Livy', 'Lucan', 'Lucretius', 'Martial', 'Nepos', 'Ovid', 'Persius', 'Petronius', 'Phaedrus', 'Plautus', 'Pliny Maior', 'Pliny Minor', 'Propertius', 'Quintilian', 'Sallust', 'Seneca Maior', 'Seneca Minor', 'Silius Italicus', 'Statius', 'Suetonius', 'Sulpicia', 'Tacitus', 'Terence', 'Tibullus', 'Valerius Flaccus', 'Valerius Maximus', 'Varro', 'Velleius', 'Vergil', 'Vitruvius', 'Ius Romanum', 'Miscellany', 'Christian', 'Medieval', 'Neo-Latin'
]

function Header(props) {
  const {authorsSelected, setAuthorsSelected, hasEntered} = props

  const handleChange = (e) => {
    const {
      target: { value },
    } = e;
    setAuthorsSelected(
      // On autofill we get a stringified value.
      typeof value === 'string' ? value.split(',') : value,
    );
  };

  const handleDelete = (e, value) => {
    e.preventDefault()
    setAuthorsSelected(authorsSelected.filter((name) => name !== value));
  }

  const getMissionStatement = () => {
    if (hasEntered) {
      return
    }
    return (
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >

        <b>Search the works of dozens of Latin authors or explore <i>The Great Beyonds</i>...</b>

      </div>
    )
  }

  const handleReset = () => {
    setAuthorsSelected([])
  }

  const getAuthorForm = () => {
    if (hasEntered) {
      return <div></div>
    }

    return (
      <div style={{marginTop: 30}}>
        <div style={{marginBottom: 5}}>
        <FormControl fullWidth={true}>
          <InputLabel id="authors-label" size="small">Select Latin authors</InputLabel>
          <Select
            size="small"
            labelId="authors-label"
            id="authors"
            multiple
            value={authorsSelected}
            onChange={handleChange}
            input={<OutlinedInput id="select-multiple-chip" label="Select Latin authors"/>}
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
      <div>
        <Button variant="contained" size="small" onClick={handleReset}>
          Reset
        </Button>
      </div>
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
      {getMissionStatement()}
      <p></p>
      {getAuthorForm()}

    </div>
  )
}

export default Header;