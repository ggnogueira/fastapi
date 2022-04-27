import React, { useEffect, useState } from "react";

const CodeSystemModal = ({active, handleModal, token, id, setErrorMesssage}) => {
    const [version, setVersion] = useState("");
    const [system, setSystem] = useState("");
    const [name, setName] = useState("");

    useEffect(() => {
        const getCodeSystem = async () => {
            const requestOptions = {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
            };
            const response = await fetch(`/api/codesystems/${id}`, requestOptions);
            if(!response.ok) {
                setErrorMesssage("Something went wrong. Could not load lead.");
            } else {
                const data = await response.json();
                setVersion(data.version);
                setSystem(data.system);
                setName(data.name);
            }
        };
        if (id) {
            getCodeSystem();
        }
    }, [id, token]);

    const cleanFormData = () => {
        setVersion("");
        setSystem("");
        setName("");
    }

    const handleCreateCodeSystem = async (e) => {
        e.preventDefault();
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify({
                version: version,
                system: system,
                name: name
            }),
        };    
        
        const response = await fetch("/api/codesystems", requestOptions);
        if(!response.ok) {
            setErrorMesssage("Something went wrong when creating code system.");
        } else {
            cleanFormData();
            handleModal();
        }

    }

    const handleUpdateCodeSystem = async (e) => {
        e.preventDefault()
        const requestOptions = {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify({
                version: version,
                system: system,
                name: name
            }),
        };
        const response = await fetch(`/api/codesystems/${id}`, requestOptions);
        if(!response.ok) {
            setErrorMesssage("Something went wrong when updating lead.");
        } else {
            cleanFormData();
            handleModal();
        }
    }

    return (
        <div className={`modal ${active && "is-active"}`}>
            <div className="modal-background" onClick={handleModal}></div>
            <div className="modal-card">
                <header className="modal-card-head has-background-primary-light">
                    <h1 className="modal-card-title">
                        { id ? "Update Code System" : "Create Code System"}
                    </h1>
                </header>
                <section className="modal-card-body">
                    <form>
                        <div className="field">
                            <label className="label">Version</label>
                            <div className="control">
                                <input 
                                    type="text" 
                                    placeholder="Enter Version"
                                    value={version}
                                    onChange={(e) => setVersion(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">System</label>
                            <div className="control">
                                <input 
                                    type="text" 
                                    placeholder="Enter System URL"
                                    value={system}
                                    onChange={(e) => setSystem(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Name</label>
                            <div className="control">
                                <input 
                                    type="text" 
                                    placeholder="Enter Code System Name"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    className="input"
                                />
                            </div>
                        </div>
                    </form>
                </section>
                <footer className="modal-card-foot has-background-primary-ligth">
                    { id ? (
                        <button className="button is-info" onClick={handleUpdateCodeSystem}>Update</button>
                    ) : (
                        <button className="button is-primary" onClick={handleCreateCodeSystem}>
                            Create
                        </button>
                    )}
                    <button className="button" onClick={handleModal}>Cancel</button>
                </footer>
            </div>
        </div>
    );
};

export default CodeSystemModal;