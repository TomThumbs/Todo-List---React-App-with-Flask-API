import React from "react";
// import logo from "./logo.svg";
import "./App.css";
import { TodoPage } from "./Pages/TodoPage";
import { Box } from "@material-ui/core";

function App() {
  return (
    <Box className="App" padding={5}>
      <TodoPage />
    </Box>
  );
}

export default App;
