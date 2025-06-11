import { useState } from "react";
import ReactMarkdown from "react-markdown";
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  TextField,
  Button,
  Box,
  Paper,
  CircularProgress,
  CssBaseline,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";

function App() {
  const [question, setQuestion] = useState("");
  const [conversation, setConversation] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;

    const userMessage = { sender: "user", text: question };
    setConversation((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();

      const botMessage = {
        sender: "bot",
        text: data.answer,
        sources: data.sources || [],
      };
      setConversation((prev) => [...prev, botMessage]);
    } catch (err) {
      const errorMsg = {
        sender: "bot",
        text: "❌ Internal Server Error",
        sources: [],
      };
      setConversation((prev) => [...prev, errorMsg]);
    }

    setQuestion("");
    setLoading(false);
  };

  return (
    <>
      <CssBaseline />
      <AppBar position="static" sx={{ backgroundColor: "#a6192e" }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            AskMQ++ – Macquarie Student Assistant
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="md" sx={{ mt: 2, mb: 10 }}>
        {conversation.map((msg, index) => (
          <Box key={index} mb={2}>
            <Paper
              elevation={1}
              sx={{
                p: 2,
                backgroundColor: msg.sender === "user" ? "#e3f2fd" : "#FFFFC5",
              }}
            >
              <Typography
                variant="subtitle2"
                color="textSecondary"
                gutterBottom
              >
                {msg.sender === "user" ? "You" : "AskMQ++"}
              </Typography>
              <ReactMarkdown>{msg.text}</ReactMarkdown>
              {msg.sources && msg.sources.length > 0 && (
                <Box mt={1}>
                  <Typography variant="caption" color="textSecondary">
                    📚 Sources:
                  </Typography>
                  <ul>
                    {msg.sources.map((src, i) => (
                      <li key={i}>
                        <ReactMarkdown>{`[${src}](${src})`}</ReactMarkdown>
                      </li>
                    ))}
                  </ul>
                </Box>
              )}
            </Paper>
          </Box>
        ))}

        {loading && (
          <Box display="flex" justifyContent="center" my={3}>
            <CircularProgress />
          </Box>
        )}
      </Container>

      <Box
        sx={{
          position: "fixed",
          bottom: 0,
          left: 0,
          width: "100%",
          backgroundColor: "#ffffff",
          p: 2,
          boxShadow: "0 -1px 6px rgba(0,0,0,0.1)",
        }}
      >
        <Container maxWidth="md">
          <Box display="flex" gap={1}>
            <TextField
              fullWidth
              variant="outlined"
              label="Ask a question..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleAsk()}
            />
            <Button
              variant="contained"
              onClick={handleAsk}
              disabled={loading}
              endIcon={<SendIcon />}
              sx={{ minWidth: 120 }}
            >
              Ask
            </Button>
          </Box>
        </Container>
      </Box>
    </>
  );
}

export default App;