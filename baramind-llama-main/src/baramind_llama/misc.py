style = """
body {
  margin: 0;
  font-family: sans-serif;
  background: #1e1e2f;
  color: #eee;
  display: flex;
  justify-content: center;
  align-items: stretch;
  height: 100vh;
}

.chat-container {
  display: grid;
  grid-template-rows: 1fr auto;
  background: #2c2c3c;
  width: 100%;
  max-width: 700px;
}

.messages {
  display: flex;
  /* flex-direction: column-reverse; */
  flex-direction: column;
  gap: 1rem;
  overflow-y: auto;
  padding: 1rem;
  justify-content: flex-end;
}

.message {
  max-width: 70%;
  padding: 0.8rem 1rem;
  border-radius: 1rem;
  line-height: 1.4;
  word-wrap: break-word;
}

.user {
  align-self: flex-end;
  background: #4e9a51;
  color: white;
}

.bot {
  align-self: flex-start;
  background: #444c5e;
  color: #ddd;
}

.input-bar {
  display: flex;
  padding: 0.75rem;
  background: #1a1a28;
  gap: 0.5rem;
}

.input-bar input {
  flex: 1;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  border: none;
  background: #2a2a3a;
  color: #eee;
  font-size: 1rem;
}

.input-bar button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 1rem;
  background: #4e9a51;
  color: white;
  font-size: 1rem;
  cursor: pointer;
}

.input-bar input:focus,
.input-bar button:focus {
  outline: none;
}
"""

greeting = "Hi, I'm your friendly neighbourhood budgeting llama. What's up?"
