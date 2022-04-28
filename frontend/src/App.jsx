import React, { useEffect, useState, useContext } from "react"
import { BrowserRouter, BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/Header";
import Welcome from "./components/Welcome";
import { UserContext } from "./context/UserContext";
import CodeSystem from "./components/CodeSystem";
import CodeSystemDetails from "./components/CodeSystemDetails";

const App = () => {
  const [message, setMessage] = useState("");
  const [token] = useContext(UserContext);

  const getWelcomeMessage = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Accept": "application/json",
      },
    };
    const response = await fetch("/api", requestOptions);
    const data = await response.json();

    if (!response.ok) {
      console.log("Something went wrong");
    } else {
      setMessage(data.message);
    }
  };

  useEffect(() => {
    getWelcomeMessage();
  }, []);
  return (
    <BrowserRouter>
      <Header title={message}/>
        <Routes>
          <Route path="/" element={<Welcome/>}/>
          <Route path="/codesystems" element={<CodeSystem/>}>
            <Route path=":id" element={<CodeSystemDetails/>}/>
          </Route>
        </Routes>
    </BrowserRouter>
  );
}

export default App;
