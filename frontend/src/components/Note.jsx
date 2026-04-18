import React from "react";
import "../styles/Note.css"

function Note({ note, onDelete }) {
    const createdDate = new Date(note.created_at).toLocaleDateString("en-US")
    const modifiedDate = new Date(note.last_modified).toLocaleDateString("en-US")

    return (
        <div className="note-container">
            <p className="note-title">{note.title}</p>
            <p className="note-content">{note.content}</p>
            <p className="note-date">{createdDate}</p>
            <p className="note-date">{modifiedDate}</p>
            <button className="delete-button" onClick={() => onDelete(note.id)}>
                Delete
            </button>
        </div>
    );
}

export default Note