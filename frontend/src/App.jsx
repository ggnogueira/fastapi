import React, { useEffect, useState, useContext } from "react"
import Register from "./components/Register";
import Header from "./components/Header";
import Login from "./components/Login";
import Table from "./components/Table";
import LeadModal from "./components/LeadModal";
import { UserContext } from "./context/UserContext";
import CodeSystem from "./components/CodeSystem";

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
    <>
      <Header title={message}/>
      <div className="columns">
        <div className="column"></div>
        <div className="column m-5 is-two-thirds">
          {!token ? (
            <div className="columns">
              <Register/><Login/>
            </div>
          ) : (
            <CodeSystem />
            //<Table />
          )}
        </div>
        <div className="column"></div>
      </div>
    </>
  );
}

export default App;
