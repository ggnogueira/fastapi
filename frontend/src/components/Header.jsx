import React, { useContext } from "react";
import { UserContext } from "../context/UserContext";
import { useNavigate  } from "react-router-dom";

const Header = ( { title }) => {
    const [token, setToken] = useContext(UserContext);
    const navigate = useNavigate ();

    const handleLogout = () => {
        setToken(null);
        navigate('/')
    };

    return (
        <div className="has-text-centered">
            <nav className="navbar is-primary" role="navigation" aria-label="main navigation">
                <div id="navbarBasicExample" className="navbar-menu">
                    <div className="navbar-start">
                    <a className="navbar-item" {...!token ? {href: "/"} : {href: "/codesystems"}}>
                        Home
                    </a>

                    <a className="navbar-item" href="https://github.com/ggnogueira/fastapi">
                        Documentation
                    </a>

                    <div className="navbar-item has-dropdown is-hoverable">
                        <a className="navbar-link" href="/">
                            More
                        </a>

                        <div className="navbar-dropdown">
                            <a className="navbar-item" href="https://br.linkedin.com/in/ggnogueira">
                                Contact
                            </a>
                            <hr className="navbar-divider"/>
                            <a className="navbar-item" href="https://github.com/ggnogueira/fastapi/issues">
                                Report an issue
                            </a>
                        </div>
                    </div>
                    </div>

                    <div className="navbar-end">
                    <div className="navbar-item">
                        <div className="buttons">
                            {token && (
                                <button className="button" onClick={handleLogout}>
                                    Logout
                                </button>
                            )}
                        </div>
                    </div>
                    </div>
                </div>
            </nav>
            <div className="has-text-centered m-6">
                <h1 className="title">{ title }</h1>
            </div>
        </div>
    );
};

export default Header;