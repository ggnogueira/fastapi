import React, { useEffect, useState } from "react";

const ConceptModal = ({active, handleModal, token, id, setErrorMesssage}) => {
    const [code, setCode] = useState("");
    const [display, setDisplay] = useState("");
    const codeSystemId = 0;

    useEffect(() => {
        const getConcept = async () => {
            const requestOptions = {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
            };
            const response = await fetch(`/api/concepts/${id}/`, requestOptions);
            if(!response.ok) {
                setErrorMesssage("Something went wrong. Could not load lead.");
            } else {
                const data = await response.json();
                setCode(data.code);
                setDisplay(data.display);
            }
        };
        if (id) {
            getConcept();
        }
    }, [id, token]);

    const cleanFormData = () => {
        setVersion("");
        setSystem("");
        setName("");
    }

    const handleCreateConcept = async (e) => {
        e.preventDefault();
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify({
                code: code,
                display: display
            }),
        };    
        
        const response = await fetch(`/api/concepts/${id}/`, requestOptions);
        if(!response.ok) {
            setErrorMesssage("Something went wrong when creating concept.");
        } else {
            cleanFormData();
            handleModal();
        }

    }

    const handleUpdateConcept = async (e) => {
        e.preventDefault()
        const requestOptions = {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify({
                code: code,
                display: display
            }),
        };
        const response = await fetch(`/api/concept/${codeSystemId}/${id}`, requestOptions);
        if(!response.ok) {
            setErrorMesssage("Something went wrong when updating concept.");
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
                        { id ? "Update Concept" : "Create Concept"}
                    </h1>
                </header>
                <section className="modal-card-body">
                    <form>
                        <div className="field">
                            <label className="label">Code</label>
                            <div className="control">
                                <input 
                                    type="text" 
                                    placeholder="Enter the concept code"
                                    value={code}
                                    onChange={(e) => setVersion(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Display</label>
                            <div className="control">
                                <input 
                                    type="text" 
                                    placeholder="Enter display string."
                                    value={display}
                                    onChange={(e) => setSystem(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                    </form>
                </section>
                <footer className="modal-card-foot has-background-primary-ligth">
                    { id ? (
                        <button className="button is-info" onClick={handleUpdateConcept}>Update</button>
                    ) : (
                        <button className="button is-primary" onClick={handleCreateConcept}>
                            Create
                        </button>
                    )}
                    <button className="button" onClick={handleModal}>Cancel</button>
                </footer>
            </div>
        </div>
    );
};

export default ConceptModal;