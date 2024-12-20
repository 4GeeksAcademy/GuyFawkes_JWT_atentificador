import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";

const Login = () => {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [emptyFields, setEmptyFields] = useState("")
    const { actions } = useContext(Context);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        
        //setea emptyFields en caso de no completar con los campos
        if (!email || !password) {
            setEmptyFields("Email and password fields are required")
            return;
        }

        //emptyFields vuelve a su estado incial
        setEmptyFields("");

        //logged retorna true en caso de ser correctos los valores ingresados y 
        //se redirige a private
        let logged = await actions.login(email, password);
        console.log(logged);
        
        if (logged) {
            navigate('/private');
        }
    }

    return (
        <div className="w-50 mx-auto mt-5">
            {/* alerta en caso de hacer submit con campos vacíos */}
            {emptyFields && (<div className="alert alert-danger" role="alert">
                    {emptyFields}
            </div>)}

            <form onSubmit={handleLogin}>
                <div className="mb-3">
                    <label htmlFor="exampleInputEmail1" className="form-label">Email address</label>
                    <input type="email" className="form-control" id="exampleInputEmail1" onChange={(e) => setEmail(e.target.value)} aria-describedby="emailHelp"/>
                </div>
                <div className="mb-3">
                    <label htmlFor="exampleInputPassword1" className="form-label">Password</label>
                    <input type="password" className="form-control" id="exampleInputPassword1" onChange={(e) => setPassword(e.target.value)}/>
                </div>
                
                <div className="me-3">
                    <button type="submit" className="btn btn-outline-primary me-3">Submit</button>
                </div>
                    
                
                
                
                
            </form>
        </div>
    )
}

export default Login;