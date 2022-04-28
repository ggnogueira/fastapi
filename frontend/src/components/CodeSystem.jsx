import React, { useState, useContext, useEffect } from "react";
import moment from "moment";
import ErrorMessage from "./ErrorMessage";
import { UserContext } from "../context/UserContext";
import CodeSystemModal from "./CodeSystemModal";
import { useNavigate, Outlet } from "react-router-dom";

const CodeSystem = () => {
    const [token] = useContext(UserContext);
    const [codeSystems, setCodeSystems] = useState(null);
    const [errorMessage, setErrorMessage] = useState("");
    const [loaded, setLoaded] = useState(false);
    const [activeModal, setActiveModal] = useState(false);
    const [id, setId] = useState(null);
    const navigate = useNavigate();

    const handleUpdate = async (id) => {
        setId(id);
        setActiveModal(true);
    }
    
    const handleDelete = async (id) => {
        const requestOptions = {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
        };
        const response = await fetch(`/api/codesystems/${id}`, requestOptions);
        if (!response.ok) {
            setErrorMessage("Something went wrong when deleting code system.");
        }

        getCodeSystems();
    };

    const handleView = async (id) => {
        /*
        const requestOptions = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
        };
        const response = await fetch(`/api/concepts?code_system_id=${id}`, requestOptions);
        if (!response.ok) {
            setErrorMessage("Something went wrong when getting concept list.");
        }
        const data = await response.json();
        console.log(data);
        */
        navigate(`/codesystems/${id}`);
    }
    
    const getCodeSystems = async () => {
        const requestOptions = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
        };

        const response = await fetch("/api/codesystems", requestOptions);
        const data = await response.json();

        if (!response.ok) {
            setErrorMessage("Something went wrong. Could not load code systems.");
        } else {
            setCodeSystems(data);
            setLoaded(true);
        }
    };

    useEffect(() => {
        getCodeSystems();
    }, []);

    const handleModal = () => {
        setActiveModal(!activeModal);
        getCodeSystems();
        setId(null);
    };

    return (
        <div className="columns">
            <div className="column"></div>
            <div className="column m-5 is-two-thirds">          
                <CodeSystemModal 
                    active={activeModal} 
                    handleModal={handleModal} 
                    token={token} 
                    id={id} 
                    setErrorMessage={setErrorMessage}
                />
                <button 
                    className="button is-fullwidth mb-5 is-primary" 
                    onClick={ () => setActiveModal(true)}
                >
                    Create Code System
                </button>
                <ErrorMessage message={errorMessage} />
                { loaded && codeSystems ? (
                    <table className="table is-fullwidth">
                        <thead>
                            <tr>
                                <th>Version</th>
                                <th>System</th>
                                <th>Name</th>
                                <th>Last Updated</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {codeSystems.map((codeSystem) => (
                                <tr key={codeSystem.id}>
                                    <td>{codeSystem.version}</td>
                                    <td>{codeSystem.system}</td>
                                    <td>{codeSystem.name}</td>
                                    <td>{moment(codeSystem.date_last_updated).format("MMMM Do YYYY")}</td>
                                    <td>
                                        <button 
                                            className="button mr-2 is-info is-light"
                                            onClick={() => handleUpdate(codeSystem.id)}
                                        >
                                            Update
                                        </button>
                                        <button 
                                            className="button mr-2 is-danger is-light"
                                            onClick={() => handleDelete(codeSystem.id)}
                                        >
                                            Delete
                                        </button>
                                        <button 
                                            className="button mr-2 is-link is-light"
                                            onClick={() => handleView(codeSystem.id)}
                                        >
                                            View
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ): <p>Loading</p>}
            </div>
            <div className="column"></div>
            <Outlet/>
        </div>            
    );
};

export default CodeSystem;