import React from "react";
import Register from "./Register";
import Login from "./Login";

const Welcome = () => {
    
    return (
        <div className="columns">
        <div className="column"></div>
        <div className="column m-5 is-two-thirds">          
            <div className="columns">
              <Register/><Login/>
            </div>
        </div>
        <div className="column"></div>
      </div>
    );
};

export default Welcome;