import React, { useState, useContext, useEffect } from "react";
import moment from "moment";
import ErrorMessage from "./ErrorMessage";
import { UserContext } from "../context/UserContext";
import ConceptModal from "./CodeSystemModal";
import { useParams } from "react-router-dom";

const CodeSystemDetails = () => {
    const params = useParams();
    const codeSystemId = params.id;
    const [token] = useContext(UserContext);
    const [errorMessage, setErrorMessage] = useState("");
    const [concepts, setConcepts] = useState(null);
    const [activeModal, setActiveModal] = useState(false);
    const [loaded, setLoaded] = useState(false);
    const [id, setId] = useState(null);

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
        const response = await fetch(`/api/concepts/${codeSystemId}/${id}`, requestOptions);
        if (!response.ok) {
            setErrorMessage("Something went wrong when deleting concept.");
        }

        getConcepts();
    };
    
    const getConcepts = async () => {
        const requestOptions = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
        };

        const response = await fetch(`/api/concepts?code_system_id=${codeSystemId}`, requestOptions);
        const data = await response.json();

        if (!response.ok) {
            setErrorMessage("Something went wrong. Could not load concepts.");
        } else {
            setConcepts(data);
            setLoaded(true);
        }
    };

    useEffect(() => {
        getConcepts();
    }, []);

    const handleModal = () => {
        setActiveModal(!activeModal);
        getConcepts();
        setId(null);
    };

    return (
        <>
            <h1>{codeSystemId}</h1>
            <ConceptModal 
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
                Create Concept
            </button>
            <ErrorMessage message={errorMessage} />
            { loaded && concepts ? (
                <table className="table is-fullwidth">
                    <thead>
                        <tr>
                            <th>Code</th>
                            <th>Display</th>
                            <th>Last Updated</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {concepts.map((concept) => (
                            <tr key={concept.id}>
                                <td>{concept.code}</td>
                                <td>{concept.display}</td>
                                <td>{moment(concept.date_last_updated).format("MMMM Do YYYY")}</td>
                                <td>
                                    <button 
                                        className="button mr-2 is-info is-light"
                                        onClick={() => handleUpdate(concept.id)}
                                    >
                                        Update
                                    </button>
                                    <button 
                                        className="button mr-2 is-danger is-light"
                                        onClick={() => handleDelete(concept.id)}
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ): <p>Loading</p>}
        </>
    );
};

export default CodeSystemDetails;