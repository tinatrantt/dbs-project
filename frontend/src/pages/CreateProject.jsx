import Form from "../components/ProjectForm"


function CreateProject() {
    return <Form route="/api/projects/" method="post" />
}

export default CreateProject