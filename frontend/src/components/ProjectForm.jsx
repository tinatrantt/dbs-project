import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import "../styles/Form.css"
import LoadingIndicator from "./LoadingIndicator";


function Form({ route }) {
    const [projectName, setProjectName] = useState("");
    const [description, setDescription] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();


    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();

        try {
            const res = await api.post(route, { projectName, description })
            localStorage.setItem(ACCESS_TOKEN, res.data.access);
            localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
            navigate("/")
        } catch (error) {
            alert(error)
        } finally {
            setLoading(false)
        }
    };


    return (
        <form onSubmit={handleSubmit} className="form-container">
            <fieldset>
                <legend>Create A New Project</legend>
                <label>Project Name</label>
                <input
                    className="form-input"
                    type="text"
                    value={projectName}
                    onChange={(e) => setProjectName(e.target.value)}
                    placeholder="Project Name"
                />
                <input
                    className="form-input"
                    type="text"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="Description (Limit: 200 characters)"
                />
                {loading && <LoadingIndicator />}
                <button className="form-button" type="submit">
                    Create Project
                </button>
            </fieldset>
        </form>
    );
}

export default Form