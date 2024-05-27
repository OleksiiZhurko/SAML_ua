import {useState} from 'react';
import {
  Box,
  Button,
  Container,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Typography
} from '@mui/material';
import {fetchGraphQL, modelsQuery, processTextsQuery} from './api';

export default function App() {
  const [selectedQuery, setSelectedQuery] = useState('processTexts');
  const [model, setModel] = useState('SVM');
  const [texts, setTexts] = useState([]);
  const [inputText, setInputText] = useState('');
  const [response, setResponse] = useState(null);

  const handleQueryChange = (event) => {
    setSelectedQuery(event.target.value);
    setTexts([]);
    setResponse(null);
  };

  const handleModelChange = (event) => {
    setModel(event.target.value);
  };

  const handleInputTextChange = (event) => {
    setInputText(event.target.value);
  };

  const handleAddText = (event) => {
    if (event.key === 'Enter' && inputText.trim() !== '') {
      setTexts([...texts, inputText.trim()]);
      setInputText('');
    }
  };

  const handleDeleteText = (index) => {
    const newTexts = texts.filter((_, idx) => idx !== index);
    setTexts(newTexts);
  };

  const handleSubmit = async () => {
    if (selectedQuery === 'processTexts') {
      const result = await fetchGraphQL(processTextsQuery, {
        input: {
          model,
          isInModel: true,
          texts
        }
      });
      setResponse(result);
    } else if (selectedQuery === 'models') {
      const result = await fetchGraphQL(modelsQuery);
      setResponse(result);
    }
  };

  return (
    <Container maxWidth="sm" sx={{
      display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      height: '100vh', padding: 2, backgroundColor: '#f8f9fa'
    }}>
      <Box sx={{
        width: '100%',
        maxWidth: 400,
        bgcolor: 'background.paper',
        borderRadius: 1,
        padding: 3,
        boxShadow: 3,
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: '#ffffff'
      }}>
        <FormControl fullWidth variant="filled" sx={{mb: 2}}>
          <InputLabel>Виберіть запит</InputLabel>
          <Select value={selectedQuery} onChange={handleQueryChange}
                  sx={{background: 'white', borderRadius: 1}}>
            <MenuItem value="processTexts">Process Texts</MenuItem>
            <MenuItem value="models">Models</MenuItem>
          </Select>
        </FormControl>

        {selectedQuery === 'processTexts' && (
          <>
            <FormControl fullWidth variant="filled" sx={{mb: 2}}>
              <InputLabel>Виберіть модель</InputLabel>
              <Select value={model} onChange={handleModelChange}
                      sx={{background: 'white', borderRadius: 1}}>
                <MenuItem value="RNN">RNN</MenuItem>
                <MenuItem value="NB">NB</MenuItem>
                <MenuItem value="SVM">SVM</MenuItem>
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="Введіть текст"
              value={inputText}
              onChange={handleInputTextChange}
              onKeyDown={handleAddText}
              variant="filled"
              sx={{background: 'white', borderRadius: 1, color: 'black'}}
            />
            <Box sx={{width: '100%', mt: 2, display: 'flex', flexDirection: 'column', gap: 1}}>
              {texts.map((text, index) => (
                <Box key={index} sx={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  bgcolor: '#ffffff',
                  p: 1,
                  borderRadius: 1
                }}>
                  <Typography
                    sx={{flexGrow: 1, mr: 2, p: 2, backgroundColor: '#f6f6f6'}}>{text}</Typography>
                  <Button variant="contained" color="error" onClick={() => handleDeleteText(index)}
                          sx={{borderRadius: 1}}>Видалити</Button>
                </Box>
              ))}
            </Box>
          </>
        )}

        <Button variant="contained" onClick={handleSubmit} fullWidth sx={{borderRadius: 1, mt: 2}}>
          Відправити запит
        </Button>

        {response && (
          <Box sx={{
            width: '100%',
            mt: 2,
            overflow: 'auto',
            bgcolor: '#ffffff',
            p: 2,
            borderRadius: 1,
            maxHeight: 500
          }}>
            <Typography component="pre" sx={{whiteSpace: 'pre-wrap', color: 'black'}}>
              {JSON.stringify(response, null, 2)}
            </Typography>
          </Box>
        )}
      </Box>
    </Container>
  );
}
